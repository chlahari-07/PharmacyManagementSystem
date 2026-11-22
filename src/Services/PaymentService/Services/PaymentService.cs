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

/// <summary>
/// Handles payment simulation and transaction recording.
/// IMPORTANT: Payment processing is strictly simulated. No actual financial transactions or external payment gateways are used.
/// </summary>
public class PaymentServiceClass : IPaymentService
{
    private readonly IPaymentRepository _paymentRepository;
    private readonly IOrderServiceClient _orderServiceClient;

    public PaymentServiceClass(
        IPaymentRepository paymentRepository,
        IOrderServiceClient orderServiceClient)
    {
        _paymentRepository = paymentRepository;
        _orderServiceClient = orderServiceClient;
    }

    private async Task<(bool Allowed, string? ErrorMessage)> ValidateOrderAsync(int orderId, decimal amount)
    {
        // Inter-service call to verify order status and total with OrderService
        var order = await _orderServiceClient.GetOrderForValidationAsync(orderId);
        if (order == null)
        {
            return (false, $"Order {orderId} does not exist or OrderService could not be contacted.");
        }

        if (string.Equals(order.Status, OrderStatuses.Cancelled, StringComparison.OrdinalIgnoreCase))
        {
            return (false, "Cannot process payment for a cancelled order.");
        }

        if (string.Equals(order.Status, OrderStatuses.PickedUp, StringComparison.OrdinalIgnoreCase))
        {
            return (false, "Cannot process payment for an order that has already been picked up.");
        }

        // Amount verification: payment amount must match order total
        if (order.TotalAmount > 0 && Math.Abs(order.TotalAmount - amount) > 0.01m)
        {
            return (false, $"Payment amount (${amount:F2}) does not match the actual order total (${order.TotalAmount:F2}).");
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

        // 1:1 check: ensure payment doesn't already exist and completed for this order
        var existing = await _paymentRepository.GetByOrderIdAsync(dto.OrderId);
        if (existing != null)
        {
            if (existing.PaymentStatus == PaymentStatuses.Completed)
            {
                return ApiResponse<PaymentResponseDto>.FailureResult(
                    $"Payment for Order {dto.OrderId} has already been completed.",
                    new List<string> { "Order is already paid." });
            }

            // Retry previously failed payment
            existing.Amount = dto.Amount;
            existing.PaymentMethod = dto.PaymentMethod;
            existing.PaymentStatus = PaymentStatuses.Completed;
            existing.PaymentDate = DateTime.UtcNow;
            existing.TransactionReference = "SIM-TXN-" + Guid.NewGuid().ToString("N")[..12].ToUpper();
            await _paymentRepository.UpdateAsync(existing);

            // Notify OrderService that payment succeeded -> verify order
            await _orderServiceClient.UpdateOrderStatusToVerifiedAsync(dto.OrderId);

            return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(existing), "Payment re-processed successfully (Simulated).");
        }

        var payment = new Payment
        {
            OrderId = dto.OrderId,
            Amount = dto.Amount,
            PaymentDate = DateTime.UtcNow,
            PaymentMethod = dto.PaymentMethod,
            PaymentStatus = PaymentStatuses.Completed, // Simulating successful gateway completion
            TransactionReference = "SIM-TXN-" + Guid.NewGuid().ToString("N")[..12].ToUpper()
        };

        var created = await _paymentRepository.AddAsync(payment);

        // Notify OrderService that payment succeeded -> verify order
        await _orderServiceClient.UpdateOrderStatusToVerifiedAsync(dto.OrderId);

        return ApiResponse<PaymentResponseDto>.SuccessResult(MapToDto(created), "Payment processed successfully (Simulated).");
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
        string txnRef = (dto.SimulateFailure ? "SIM-FAILED-" : "SIM-TXN-") + Guid.NewGuid().ToString("N")[..10].ToUpper();

        if (existing != null)
        {
            existing.Amount = dto.Amount;
            existing.PaymentMethod = dto.PaymentMethod ?? "UPI";
            existing.PaymentStatus = status;
            existing.PaymentDate = DateTime.UtcNow;
            existing.TransactionReference = txnRef;
            await _paymentRepository.UpdateAsync(existing);

            if (!dto.SimulateFailure)
            {
                await _orderServiceClient.UpdateOrderStatusToVerifiedAsync(dto.OrderId);
            }

            return ApiResponse<PaymentResponseDto>.SuccessResult(
                MapToDto(existing),
                dto.SimulateFailure
                    ? "Payment simulation resulted in: FAILED (Simulated)"
                    : "Payment simulation successful: COMPLETED (Simulated). No real money was transferred.");
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

        if (!dto.SimulateFailure)
        {
            await _orderServiceClient.UpdateOrderStatusToVerifiedAsync(dto.OrderId);
        }

        return ApiResponse<PaymentResponseDto>.SuccessResult(
            MapToDto(created),
            dto.SimulateFailure
                ? "Payment simulation resulted in: FAILED (Simulated)"
                : "Payment simulation successful: COMPLETED (Simulated). No real money was transferred.");
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
