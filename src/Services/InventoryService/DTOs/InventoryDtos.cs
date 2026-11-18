using System.ComponentModel.DataAnnotations;

namespace InventoryService.DTOs;

public class DrugDto
{
    public int DrugId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public DateTime ExpiryDate { get; set; }
    public int Quantity { get; set; }
    public bool IsAvailable { get; set; }
}

public class CreateDrugDto
{
    [Required(ErrorMessage = "Drug name is required.")]
    [StringLength(150, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;

    [MaxLength(500)]
    public string? Description { get; set; }

    [Required]
    [Range(0.01, 100000.00, ErrorMessage = "Price must be greater than zero.")]
    public decimal Price { get; set; }

    [Required]
    public DateTime ExpiryDate { get; set; }

    [Required]
    [Range(0, 1000000, ErrorMessage = "Quantity cannot be negative.")]
    public int Quantity { get; set; }

    public bool IsAvailable { get; set; } = true;
}

public class UpdateDrugDto
{
    [Required]
    [StringLength(150, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;

    [MaxLength(500)]
    public string? Description { get; set; }

    [Required]
    [Range(0.01, 100000.00)]
    public decimal Price { get; set; }

    [Required]
    public DateTime ExpiryDate { get; set; }

    [Required]
    [Range(0, 1000000)]
    public int Quantity { get; set; }

    public bool IsAvailable { get; set; }
}

public class SupplierDto
{
    public int SupplierId { get; set; }
    public string SupplierName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PhoneNumber { get; set; } = string.Empty;
    public string Address { get; set; } = string.Empty;
}

public class CreateSupplierDto
{
    [Required(ErrorMessage = "Supplier name is required.")]
    [StringLength(150, MinimumLength = 2)]
    public string SupplierName { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    [StringLength(150)]
    public string Email { get; set; } = string.Empty;

    [Required]
    [Phone]
    [StringLength(20)]
    public string PhoneNumber { get; set; } = string.Empty;

    [Required]
    [StringLength(300)]
    public string Address { get; set; } = string.Empty;
}

public class UpdateSupplierDto : CreateSupplierDto
{
}

public class InventoryDto
{
    public int InventoryId { get; set; }
    public int SupplierId { get; set; }
    public string SupplierName { get; set; } = string.Empty;
    public int DrugId { get; set; }
    public string DrugName { get; set; } = string.Empty;
    public decimal PurchasePrice { get; set; }
    public int QuantityAdded { get; set; }
    public DateTime StockReceivedDate { get; set; }
}

public class CreateInventoryStockDto
{
    [Required]
    public int SupplierId { get; set; }

    [Required]
    public int DrugId { get; set; }

    [Required]
    [Range(0.01, 100000.00, ErrorMessage = "Purchase price must be positive.")]
    public decimal PurchasePrice { get; set; }

    [Required]
    [Range(1, 100000, ErrorMessage = "Quantity added must be at least 1.")]
    public int QuantityAdded { get; set; }
}

public class DeductStockItemDto
{
    public int DrugId { get; set; }
    public int Quantity { get; set; }
}

public class DeductStockRequestDto
{
    public List<DeductStockItemDto> Items { get; set; } = new();
}

public class StockCheckResultDto
{
    public bool IsAvailable { get; set; }
    public List<string> OutOfStockItems { get; set; } = new();
}
