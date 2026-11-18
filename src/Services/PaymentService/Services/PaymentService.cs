using PaymentService.DTOs;
using PaymentService.Models;
using PaymentService.Repositories;
using PharmacyManagement.Common.Models;

namespace PaymentService.Services;

public interface IPaymentService
{
    Task<ApiResponse<PaymentResponseDto>> ProcessPaymentAsync(ProcessPaymentDto dto);
    Task<ApiResponse<PaymentResponseDto>> GetPaymentByOrderIdAsync(int orderId);
    Task<ApiResponse<PaymentResponseDto>> GetPaymentByIdAsync(int paymentId);
    Task<ApiResponse<IEnumerable<PaymentResponseDto>>> GetAllPaymentsAsync();
    Task<ApiResponse<PaymentResponseDto>> UpdatePaymentStatusAsync(int paymentId, string newStatus);
}

public class PaymentServiceClass : IPaymentService
{
    private readonly IPaymentRepository _paymentRepository;

    public PaymentServiceClass(IPaymentRepository paymentRepository)
    {
        _paymentRepository = paymentRepository;
    }

    public async Task<ApiResponse<PaymentResponseDto>> ProcessPaymentAsync(ProcessPaymentDto dto)
    {
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
