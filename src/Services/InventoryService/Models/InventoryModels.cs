using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace InventoryService.Models;

[Table("Drugs")]
public class Drug
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int DrugId { get; set; }

    [Required]
    [MaxLength(150)]
    public string Name { get; set; } = string.Empty;

    [MaxLength(500)]
    public string? Description { get; set; }

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; } // Selling Price

    [Required]
    public DateTime ExpiryDate { get; set; }

    [Required]
    public int Quantity { get; set; }

    public bool IsAvailable { get; set; } = true;

    // Navigation property for 1:M relationship: Drug to Inventory
    [JsonIgnore]
    public ICollection<Inventory> Inventories { get; set; } = new List<Inventory>();
}

[Table("Suppliers")]
public class Supplier
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int SupplierId { get; set; }

    [Required]
    [MaxLength(150)]
    public string SupplierName { get; set; } = string.Empty;

    [Required]
    [MaxLength(150)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required]
    [MaxLength(20)]
    [Phone]
    public string PhoneNumber { get; set; } = string.Empty;

    [Required]
    [MaxLength(300)]
    public string Address { get; set; } = string.Empty;

    // Navigation property for 1:M relationship: Supplier to Inventory
    [JsonIgnore]
    public ICollection<Inventory> Inventories { get; set; } = new List<Inventory>();
}

[Table("Inventory")]
public class Inventory
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int InventoryId { get; set; }

    [Required]
    [ForeignKey("Supplier")]
    public int SupplierId { get; set; }

    [Required]
    [ForeignKey("Drug")]
    public int DrugId { get; set; }

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal PurchasePrice { get; set; }

    public int QuantityAdded { get; set; }

    public DateTime StockReceivedDate { get; set; } = DateTime.UtcNow;

    // Navigation properties
    public Supplier? Supplier { get; set; }
    public Drug? Drug { get; set; }
}
