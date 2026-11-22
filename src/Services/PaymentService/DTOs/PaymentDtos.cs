using System.ComponentModel.DataAnnotations;

namespace PaymentService.DTOs;

public class ProcessPaymentDto
{
    [Required]
    public int OrderId { get; set; }

    [Required]
    [Range(0.01, 1000000.00, ErrorMessage = "Payment amount must be greater than zero.")]
    public decimal Amount { get; set; }

    [Required]
    [StringLength(50)]
    public string PaymentMethod { get; set; } = "CreditCard"; // CreditCard, DebitCard, UPI, NetBanking, Cash
}

public class SimulatePaymentDto
{
    [Required]
    public int OrderId { get; set; }

    [Required]
    [Range(0.01, 1000000.00, ErrorMessage = "Payment amount must be greater than zero.")]
    public decimal Amount { get; set; }

    [StringLength(50)]
    public string PaymentMethod { get; set; } = "UPI"; // CreditCard, DebitCard, UPI, NetBanking, Cash

    public bool SimulateFailure { get; set; } = false; // Toggle to test failed payment handling
}

public class PaymentResponseDto
{
    public int PaymentId { get; set; }
    public int OrderId { get; set; }
    public decimal Amount { get; set; }
    public DateTime PaymentDate { get; set; }
    public string PaymentMethod { get; set; } = string.Empty;
    public string PaymentStatus { get; set; } = string.Empty;
    public string? TransactionReference { get; set; }
}

public class UpdatePaymentStatusDto
{
    [Required]
    [RegularExpression("^(Pending|Completed|Failed)$", ErrorMessage = "Status must be Pending, Completed, or Failed.")]
    public string PaymentStatus { get; set; } = string.Empty;
}

public class OrderValidationResultDto
{
    public int OrderId { get; set; }
    public int DoctorID { get; set; }
    public decimal TotalAmount { get; set; }
    public string Status { get; set; } = string.Empty;
}
