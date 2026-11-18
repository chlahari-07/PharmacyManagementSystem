using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PaymentService.Models;

[Table("Payments")]
public class Payment
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int PaymentId { get; set; }

    [Required]
    public int OrderId { get; set; } // Logical FK from Order table in OrderService (1:1 Order to Payment)

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal Amount { get; set; }

    public DateTime PaymentDate { get; set; } = DateTime.UtcNow;

    [Required]
    [MaxLength(50)]
    public string PaymentMethod { get; set; } = "CreditCard"; // CreditCard, DebitCard, UPI, NetBanking, Cash

    [Required]
    [MaxLength(20)]
    public string PaymentStatus { get; set; } = "Pending"; // Pending, Completed, Failed

    [MaxLength(100)]
    public string? TransactionReference { get; set; }
}
