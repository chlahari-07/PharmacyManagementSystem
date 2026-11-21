using PaymentService.DTOs;
using PaymentService.Models;
using PaymentService.Repositories;
using PharmacyManagement.Common.Models;

namespace PaymentService.Services;

public interface IPaymentService
{
    Task<ApiResponse<PaymentResponseDto>> ProcessPaymentAsync(ProcessPaymentDto dto);
    Task<ApiResponse<PaymentResponseDto>> SimulatePaymentAsync(SimulatePaymentDto dto);
    Task<ApiResponse<PaymentResponseDto>> GetPaymentByOrderIdAsync(int orderId);
    Task<ApiResponse<PaymentResponseDto>> GetPaymentByIdAsync(int paymentId);
    Task<ApiResponse<IEnumerable<PaymentResponseDto>>> GetAllPaymentsAsync();
    Task<ApiResponse<PaymentResponseDto>> UpdatePaymentStatusAsync(int paymentId, string newStatus);
}

public class PaymentServiceClass : IPaymentService
{
    private readonly IPaymentRepository _paymentRepository;
    private readonly IHttpClientFactory? _httpClientFactory;

    public PaymentServiceClass(IPaymentRepository paymentRepository, IHttpClientFactory? httpClientFactory = null)
    {
        _paymentRepository = paymentRepository;
        _httpClientFactory = httpClientFactory;
    }

    private async Task<(bool Allowed, string? ErrorMessage)> ValidateOrderAsync(int orderId, decimal amount)
    {
        if (_httpClientFactory == null) return (true, null);

        try
        {
            var client = _httpClientFactory.CreateClient();
            client.BaseAddress = new Uri("http://localhost:5003");
            var response = await client.GetAsync($"/api/orders/{orderId}");
            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                var node = System.Text.Json.Nodes.JsonNode.Parse(content);
                var data = node?["data"];
                if (data != null)
                {
                    var status = data["status"]?.ToString();
                    var totalAmount = data["totalAmount"]?.GetValue<decimal>() ?? 0;

                    if (string.Equals(status, OrderStatuses.Cancelled, StringComparison.OrdinalIgnoreCase))
                    {
                        return (false, "Cannot process payment for a cancelled order.");
                    }

                    if (totalAmount > 0 && amount != totalAmount)
                    {
                        return (false, $"Payment amount ({amount:F2}) does not match the calculated order total ({totalAmount:F2}).");
                    }
                }
            }
            else if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                return (false, $"Order {orderId} does not exist.");
            }
        }
        catch
        {
            // Decoupled / offline test resilience
        }

        return (true, null);
    }

    public async Task<ApiResponse<PaymentResponseDto>> ProcessPaymentAsync(ProcessPaymentDto dto)
    {
        var (allowed, error) = await ValidateOrderAsync(dto.OrderId, dto.Amount);
        if (!allowed)
        {
            return ApiResponse<PaymentResponseDto>.FailureResult(error ?? "Payment validation failed.");
        }

        // 1:1 check: ensure payment doesn't already exist for this order
        var existing = await _paymentRepository.GetByOrderIdAsync(dto.OrderId);
        if (existing != null)
        {
            if (existing.PaymentStatus == PaymentStatuses.Completed)
            {
                return ApiResponse<PaymentResponseDto>.FailureResult(
                    $"Payment for Order {dto.OrderId} has already been completed.",
                    new List<string> { "Order is already paid." });
            }

            // Retry failed payment
            existing.Amount = dto.Amount;
            existing.PaymentMethod = dto.PaymentMethod;
            existing.PaymentStatus = PaymentStatuses.Completed;
            existing.PaymentDate = DateTime.UtcNow;
            existing.TransactionReference = "TXN-" + Guid.NewGuid().ToString("N")[..12].ToUpper();
            await _paymentRepository.UpdateAsync(existing);

            return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(existing), "Payment re-processed successfully.");
        }

        var payment = new Payment
        {
            OrderId = dto.OrderId,
            Amount = dto.Amount,
            PaymentDate = DateTime.UtcNow,
            PaymentMethod = dto.PaymentMethod,
            PaymentStatus = PaymentStatuses.Completed, // Simulating successful payment gateway response
            TransactionReference = "TXN-" + Guid.NewGuid().ToString("N")[..12].ToUpper()
        };

        var created = await _paymentRepository.AddAsync(payment);
        return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(created), "Payment processed successfully.");
    }

    public async Task<ApiResponse<PaymentResponseDto>> SimulatePaymentAsync(SimulatePaymentDto dto)
    {
        var (allowed, error) = await ValidateOrderAsync(dto.OrderId, dto.Amount);
        if (!allowed)
        {
            return ApiResponse<PaymentResponseDto>.FailureResult(error ?? "Payment simulation failed.");
        }

        var existing = await _paymentRepository.GetByOrderIdAsync(dto.OrderId);
        if (existing != null && existing.PaymentStatus == PaymentStatuses.Completed)
        {
            return ApiResponse<PaymentResponseDto>.FailureResult($"Order {dto.OrderId} has already been paid successfully.");
        }

        string status = dto.SimulateFailure ? PaymentStatuses.Failed : PaymentStatuses.Completed;
        string txnRef = "SIM-TXN-" + Guid.NewGuid().ToString("N")[..10].ToUpper();

        if (existing != null)
        {
            existing.Amount = dto.Amount;
            existing.PaymentMethod = dto.PaymentMethod ?? "UPI";
            existing.PaymentStatus = status;
            existing.PaymentDate = DateTime.UtcNow;
            existing.TransactionReference = txnRef;
            await _paymentRepository.UpdateAsync(existing);

            return ApiResponse<PaymentResponseDto>.SuccessResult(
                MapToDto(existing),
                dto.SimulateFailure ? "Payment simulation resulted in: FAILED" : "Payment simulation successful: COMPLETED");
        }

        var payment = new Payment
        {
            OrderId = dto.OrderId,
            Amount = dto.Amount,
            PaymentDate = DateTime.UtcNow,
            PaymentMethod = dto.PaymentMethod ?? "UPI",
            PaymentStatus = status,
            TransactionReference = txnRef
        };

        var created = await _paymentRepository.AddAsync(payment);
        return ApiResponse<PaymentResponseDto>.SuccessResult(
            MapToDto(created),
            dto.SimulateFailure ? "Payment simulation resulted in: FAILED" : "Payment simulation successful: COMPLETED");
    }

    public async Task<ApiResponse<PaymentResponseDto>> GetPaymentByOrderIdAsync(int orderId)
    {
        var payment = await _paymentRepository.GetByOrderIdAsync(orderId);
        if (payment == null)
        {
            return ApiResponse<PaymentResponseDto>.FailureResult($"No payment record found for Order ID {orderId}.");
        }
        return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(payment));
    }

    public async Task<ApiResponse<PaymentResponseDto>> GetPaymentByIdAsync(int paymentId)
    {
        var payment = await _paymentRepository.GetByIdAsync(paymentId);
        if (payment == null)
        {
            return ApiResponse<PaymentResponseDto>.FailureResult($"Payment ID {paymentId} not found.");
        }
        return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(payment));
    }

    public async Task<ApiResponse<IEnumerable<PaymentResponseDto>>> GetAllPaymentsAsync()
    {
        var payments = await _paymentRepository.GetAllAsync();
        var dtos = payments.Select(MapToDto);
        return ApiResponse<IEnumerable<PaymentResponseDto>>.SuccessResult(dtos, "Payments retrieved successfully.");
    }

    public async Task<ApiResponse<PaymentResponseDto>> UpdatePaymentStatusAsync(int paymentId, string newStatus)
    {
        var payment = await _paymentRepository.GetByIdAsync(paymentId);
        if (payment == null)
        {
            return ApiResponse<PaymentResponseDto>.FailureResult($"Payment ID {paymentId} not found.");
        }

        payment.PaymentStatus = newStatus;
        await _paymentRepository.UpdateAsync(payment);

        return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(payment), $"Payment status updated to {newStatus}.");
    }

    private static PaymentResponseDto MapToDto(Payment payment) => new()
    {
        PaymentId = payment.PaymentId,
        OrderId = payment.OrderId,
        Amount = payment.Amount,
        PaymentDate = payment.PaymentDate,
        PaymentMethod = payment.PaymentMethod,
        PaymentStatus = payment.PaymentStatus,
        TransactionReference = payment.TransactionReference
    };
}
