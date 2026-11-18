using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace OrderService.Models;

[Table("Orders")]
public class Order
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int OrderId { get; set; }

    [Required]
    public int DoctorID { get; set; } // Logical FK from User table in AuthService (1:M User to Order)

    public DateTime OrderDate { get; set; } = DateTime.UtcNow;

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal TotalAmount { get; set; }

    [Required]
    [MaxLength(20)]
    public string Status { get; set; } = "Pending"; // Cart / Pending / Verified / PickedUp

    // Navigation property for 1:M relationship: Order to OrderItem
    public ICollection<OrderItem> OrderItems { get; set; } = new List<OrderItem>();
}

[Table("OrderItems")]
public class OrderItem
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int OrderItemId { get; set; }

    [Required]
    [ForeignKey("Order")]
    public int OrderId { get; set; } // FK from Order table

    [Required]
    public int DrugId { get; set; } // Logical FK from Drug table in InventoryService (1:M Drug to OrderItem)

    [MaxLength(150)]
    public string DrugName { get; set; } = string.Empty;

    [Required]
    public int Quantity { get; set; }

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal UnitPrice { get; set; }

    // Navigation property
    [JsonIgnore]
    public Order? Order { get; set; }
}
