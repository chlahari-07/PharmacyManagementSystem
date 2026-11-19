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
    public string DrugName { get; set; } = string.Empty;

    // Alias property for backward compatibility with Name
    [NotMapped]
    public string Name
    {
        get => DrugName;
        set => DrugName = value;
    }

    [MaxLength(500)]
    public string? Description { get; set; }

    [MaxLength(100)]
    public string? Category { get; set; }

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; } // Selling Price

    [NotMapped]
    public decimal DrugPrice
    {
        get => Price;
        set => Price = value;
    }

    [Required]
    public DateTime ExpiryDate { get; set; }

    [Required]
    public int Quantity { get; set; }

    [Required]
    public int MinimumStockQuantity { get; set; } = 20; // Default minimum stock alert threshold

    public bool IsAvailable { get; set; } = true;

    public DateTime CreatedDate { get; set; } = DateTime.UtcNow;

    public DateTime? UpdatedDate { get; set; }

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

    [Required]
    public int QuantitySupplied { get; set; }

    // Alias for backward compatibility
    [NotMapped]
    public int QuantityAdded
    {
        get => QuantitySupplied;
        set => QuantitySupplied = value;
    }

    [Required]
    public DateTime SupplyDate { get; set; } = DateTime.UtcNow;

    // Alias for backward compatibility
    [NotMapped]
    public DateTime StockReceivedDate
    {
        get => SupplyDate;
        set => SupplyDate = value;
    }

    [MaxLength(100)]
    public string? BatchNumber { get; set; }

    [MaxLength(500)]
    public string? Notes { get; set; }

    // Navigation properties
    public Supplier? Supplier { get; set; }
    public Drug? Drug { get; set; }
}
