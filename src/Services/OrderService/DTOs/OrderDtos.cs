using System.ComponentModel.DataAnnotations;

namespace OrderService.DTOs;

public class CreateOrderItemDto
{
    [Required]
    public int DrugId { get; set; }

    [Required]
    [StringLength(150)]
    public string DrugName { get; set; } = string.Empty;

    [Required]
    [Range(1, 1000, ErrorMessage = "Quantity must be at least 1.")]
    public int Quantity { get; set; }

    [Required]
    [Range(0.01, 100000.00, ErrorMessage = "Unit price must be positive.")]
    public decimal UnitPrice { get; set; }
}

public class CreateOrderDto
{
    public int? DoctorId { get; set; } // If authenticated, extracted from JWT token

    [Required]
    [MinLength(1, ErrorMessage = "At least one order item is required.")]
    public List<CreateOrderItemDto> Items { get; set; } = new();

    public string Status { get; set; } = "Pending"; // "Cart" or "Pending"
}

public class AddToCartDto
{
    public int? DoctorId { get; set; }

    [Required]
    [MinLength(1, ErrorMessage = "At least one drug item must be added to cart.")]
    public List<CreateOrderItemDto> Items { get; set; } = new();
}

public class OrderItemResponseDto
{
    public int OrderItemId { get; set; }
    public int OrderId { get; set; }
    public int DrugId { get; set; }
    public string DrugName { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal SubTotal => Quantity * UnitPrice;
}

public class OrderResponseDto
{
    public int OrderId { get; set; }
    public int DoctorID { get; set; }
    public DateTime OrderDate { get; set; }
    public decimal TotalAmount { get; set; }
    public string Status { get; set; } = string.Empty;
    public List<OrderItemResponseDto> OrderItems { get; set; } = new();
}

public class UpdateOrderStatusDto
{
    [Required]
    [RegularExpression("^(Cart|Pending|Verified|PickedUp|Cancelled)$", ErrorMessage = "Status must be Cart, Pending, Verified, PickedUp, or Cancelled.")]
    public string Status { get; set; } = string.Empty;
}

public class ValidateOrderResultDto
{
    public int OrderId { get; set; }
    public bool IsValid { get; set; }
    public string CurrentStatus { get; set; } = string.Empty;
    public decimal TotalAmount { get; set; }
    public int ItemCount { get; set; }
    public string Message { get; set; } = string.Empty;
}

public class InterServiceDeductStockItem
{
    public int DrugId { get; set; }
    public int Quantity { get; set; }
}

public class InterServiceDeductStockRequest
{
    public List<InterServiceDeductStockItem> Items { get; set; } = new();
}

public class DrugValidationDto
{
    public int DrugId { get; set; }
    public string DrugName { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public int Quantity { get; set; }
    public bool IsAvailable { get; set; }
    public DateTime ExpiryDate { get; set; }
}
