using OrderService.DTOs;
using OrderService.Models;
using OrderService.Repositories;
using PharmacyManagement.Common.Models;

namespace OrderService.Services;

public interface IOrderService
{
    Task<ApiResponse<OrderResponseDto>> CreateOrderAsync(int doctorId, CreateOrderDto dto);
    Task<ApiResponse<OrderResponseDto>> AddToCartAsync(int doctorId, AddToCartDto dto);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetCartAsync(int doctorId);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetMyOrdersAsync(int doctorId);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetAllOrdersAsync();
    Task<ApiResponse<OrderResponseDto>> GetOrderByIdAsync(int orderId);
    Task<ApiResponse<OrderResponseDto>> VerifyOrderAsync(int orderId);
    Task<ApiResponse<OrderResponseDto>> MarkOrderAsPickedUpAsync(int orderId);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetPickedUpOrdersAsync();
    Task<ApiResponse<OrderResponseDto>> CancelOrderAsync(int orderId);
    Task<ApiResponse<OrderResponseDto>> UpdateOrderStatusAsync(int orderId, string status);
    Task<ApiResponse<ValidateOrderResultDto>> ValidateOrderAsync(int orderId);
}

public class OrderServiceClass : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IInventoryServiceClient _inventoryClient;

    public OrderServiceClass(IOrderRepository orderRepository, IInventoryServiceClient inventoryClient)
    {
        _orderRepository = orderRepository;
        _inventoryClient = inventoryClient;
    }

    public async Task<ApiResponse<OrderResponseDto>> CreateOrderAsync(int doctorId, CreateOrderDto dto)
    {
        if (dto.Items == null || !dto.Items.Any())
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Order must contain at least one item.");
        }

        // Validate quantities are strictly positive
        if (dto.Items.Any(i => i.Quantity <= 0))
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Order item quantity must be strictly greater than zero.");
        }

        // Server-side price calculation: fetch verified drug details from InventoryService
        var validatedItems = new List<OrderItem>();
        foreach (var item in dto.Items)
        {
            var drug = await _inventoryClient.GetDrugDetailsAsync(item.DrugId);
            if (drug == null)
            {
                return ApiResponse<OrderResponseDto>.FailureResult(
                    $"Drug with ID {item.DrugId} ('{item.DrugName}') does not exist in Inventory.");
            }

            if (drug.ExpiryDate < DateTime.UtcNow)
            {
                return ApiResponse<OrderResponseDto>.FailureResult(
                    $"Drug '{drug.DrugName}' has expired ({drug.ExpiryDate:yyyy-MM-dd}) and cannot be ordered.");
            }

            if (!drug.IsAvailable || drug.Quantity < item.Quantity)
            {
                return ApiResponse<OrderResponseDto>.FailureResult(
                    $"Insufficient stock for '{drug.DrugName}'. Requested: {item.Quantity}, Available in inventory: {drug.Quantity}.");
            }

            // Always use trusted server-side price and medicine name from InventoryService
            validatedItems.Add(new OrderItem
            {
                DrugId = drug.DrugId,
                DrugName = drug.DrugName,
                Quantity = item.Quantity,
                UnitPrice = drug.Price
            });
        }

        decimal totalAmount = validatedItems.Sum(i => i.Quantity * i.UnitPrice);

        var order = new Order
        {
            DoctorID = doctorId,
            OrderDate = DateTime.UtcNow,
            TotalAmount = totalAmount,
            Status = string.Equals(dto.Status, OrderStatuses.Cart, StringComparison.OrdinalIgnoreCase)
                ? OrderStatuses.Cart
                : OrderStatuses.Pending,
            OrderItems = validatedItems
        };

        // If placing an active order (Pending), trigger inventory stock deduction
        if (order.Status == OrderStatuses.Pending)
        {
            var stockDeductRequest = new InterServiceDeductStockRequest
            {
                Items = validatedItems.Select(i => new InterServiceDeductStockItem
                {
                    DrugId = i.DrugId,
                    Quantity = i.Quantity
                }).ToList()
            };

            var stockDeducted = await _inventoryClient.DeductStockAsync(stockDeductRequest);
            if (!stockDeducted)
            {
                return ApiResponse<OrderResponseDto>.FailureResult(
                    "Cannot place order. Inventory stock deduction failed or medicine is out of stock.",
                    new List<string> { "Inventory stock deduction failed or medicine is expired/unavailable." });
            }
        }

        var created = await _orderRepository.CreateOrderAsync(order);
        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(created), "Order placed successfully.");
    }

    public async Task<ApiResponse<OrderResponseDto>> AddToCartAsync(int doctorId, AddToCartDto dto)
    {
        if (dto.Items == null || !dto.Items.Any())
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Cart must contain at least one drug item.");
        }

        if (dto.Items.Any(i => i.Quantity <= 0))
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Item quantity must be strictly greater than zero.");
        }

        // Validate items and retrieve server prices
        var validatedItems = new List<OrderItem>();
        foreach (var item in dto.Items)
        {
            var drug = await _inventoryClient.GetDrugDetailsAsync(item.DrugId);
            if (drug == null)
            {
                return ApiResponse<OrderResponseDto>.FailureResult($"Drug with ID {item.DrugId} was not found in Inventory.");
            }

            if (drug.ExpiryDate < DateTime.UtcNow)
            {
                return ApiResponse<OrderResponseDto>.FailureResult($"Drug '{drug.DrugName}' has expired and cannot be added to cart.");
            }

            validatedItems.Add(new OrderItem
            {
                DrugId = drug.DrugId,
                DrugName = drug.DrugName,
                Quantity = item.Quantity,
                UnitPrice = drug.Price
            });
        }

        // Check if there is an existing Cart order for this doctor
        var doctorOrders = await _orderRepository.GetOrdersByDoctorIdAsync(doctorId);
        var existingCart = doctorOrders.FirstOrDefault(o => o.Status == OrderStatuses.Cart);

        if (existingCart != null)
        {
            foreach (var item in validatedItems)
            {
                var existingItem = existingCart.OrderItems.FirstOrDefault(oi => oi.DrugId == item.DrugId);
                if (existingItem != null)
                {
                    existingItem.Quantity += item.Quantity;
                }
                else
                {
                    existingCart.OrderItems.Add(new OrderItem
                    {
                        OrderId = existingCart.OrderId,
                        DrugId = item.DrugId,
                        DrugName = item.DrugName,
                        Quantity = item.Quantity,
                        UnitPrice = item.UnitPrice
                    });
                }
            }

            existingCart.TotalAmount = existingCart.OrderItems.Sum(i => i.Quantity * i.UnitPrice);
            await _orderRepository.UpdateOrderAsync(existingCart);
            return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(existingCart), "Drug added to existing cart.");
        }

        // Create new Cart order
        var cartOrder = new Order
        {
            DoctorID = doctorId,
            OrderDate = DateTime.UtcNow,
            TotalAmount = validatedItems.Sum(i => i.Quantity * i.UnitPrice),
            Status = OrderStatuses.Cart,
            OrderItems = validatedItems
        };

        var created = await _orderRepository.CreateOrderAsync(cartOrder);
        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(created), "Drug added to new cart.");
    }

    public async Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetCartAsync(int doctorId)
    {
        var orders = await _orderRepository.GetOrdersByDoctorIdAsync(doctorId);
        var cartOrders = orders.Where(o => o.Status == OrderStatuses.Cart).Select(MapToDto);
        return ApiResponse<IEnumerable<OrderResponseDto>>.SuccessResult(cartOrders, "Doctor cart items retrieved.");
    }

    public async Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetMyOrdersAsync(int doctorId)
    {
        var orders = await _orderRepository.GetOrdersByDoctorIdAsync(doctorId);
        var dtos = orders.Select(MapToDto);
        return ApiResponse<IEnumerable<OrderResponseDto>>.SuccessResult(dtos, "Orders retrieved successfully.");
    }

    public async Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetAllOrdersAsync()
    {
        var orders = await _orderRepository.GetAllOrdersAsync();
        var dtos = orders.Select(MapToDto);
        return ApiResponse<IEnumerable<OrderResponseDto>>.SuccessResult(dtos, "All orders retrieved successfully.");
    }

    public async Task<ApiResponse<OrderResponseDto>> GetOrderByIdAsync(int orderId)
    {
        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Order with ID {orderId} not found.");
        }
        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(order));
    }

    public async Task<ApiResponse<OrderResponseDto>> VerifyOrderAsync(int orderId)
    {
        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Order with ID {orderId} not found.");
        }

        if (order.Status == OrderStatuses.PickedUp)
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Order has already been picked up and cannot be reverified.");
        }

        if (order.Status == OrderStatuses.Cancelled)
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Cancelled orders cannot be verified.");
        }

        order.Status = OrderStatuses.Verified;
        await _orderRepository.UpdateOrderAsync(order);

        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(order), "Order verified successfully by Admin.");
    }

    public async Task<ApiResponse<OrderResponseDto>> MarkOrderAsPickedUpAsync(int orderId)
    {
        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Order with ID {orderId} not found.");
        }

        if (order.Status != OrderStatuses.Verified)
        {
            return ApiResponse<OrderResponseDto>.FailureResult(
                $"Order must be verified before marking as picked up. Current status: '{order.Status}'.");
        }

        order.Status = OrderStatuses.PickedUp;
        await _orderRepository.UpdateOrderAsync(order);

        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(order), "Order moved to PickedUp section.");
    }

    public async Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetPickedUpOrdersAsync()
    {
        var orders = await _orderRepository.GetOrdersByStatusAsync(OrderStatuses.PickedUp);
        var dtos = orders.Select(MapToDto);
        return ApiResponse<IEnumerable<OrderResponseDto>>.SuccessResult(dtos, "Picked up orders retrieved successfully.");
    }

    public async Task<ApiResponse<OrderResponseDto>> CancelOrderAsync(int orderId)
    {
        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Order with ID {orderId} not found.");
        }

        if (order.Status == OrderStatuses.PickedUp)
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Cannot cancel an order that has already been picked up.");
        }

        if (order.Status == OrderStatuses.Cancelled)
        {
            return ApiResponse<OrderResponseDto>.FailureResult("Order has already been cancelled.");
        }

        // Release / restore reserved medicine stock back to inventory for active pending or verified orders
        if (order.Status == OrderStatuses.Pending || order.Status == OrderStatuses.Verified)
        {
            if (order.OrderItems.Any())
            {
                var releaseRequest = new InterServiceDeductStockRequest
                {
                    Items = order.OrderItems.Select(oi => new InterServiceDeductStockItem
                    {
                        DrugId = oi.DrugId,
                        Quantity = oi.Quantity
                    }).ToList()
                };

                var restored = await _inventoryClient.ReleaseStockAsync(releaseRequest);
                if (!restored)
                {
                    // If stock restoration fails, do NOT report successful cancellation!
                    return ApiResponse<OrderResponseDto>.FailureResult(
                        "Cannot cancel order. Stock restoration to inventory failed. Please try again.",
                        new List<string> { "InventoryService was unable to restore reserved drug quantities." });
                }
            }
        }

        order.Status = OrderStatuses.Cancelled;
        await _orderRepository.UpdateOrderAsync(order);

        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(order), "Order cancelled successfully and reserved stock was released back to inventory.");
    }

    public async Task<ApiResponse<OrderResponseDto>> UpdateOrderStatusAsync(int orderId, string status)
    {
        if (!OrderStatuses.ValidStatuses.Contains(status))
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Invalid order status '{status}'. Valid: Cart, Pending, Verified, PickedUp, Cancelled.");
        }

        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Order with ID {orderId} not found.");
        }

        order.Status = status;
        await _orderRepository.UpdateOrderAsync(order);

        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(order), $"Order status updated to {status}.");
    }

    public async Task<ApiResponse<ValidateOrderResultDto>> ValidateOrderAsync(int orderId)
    {
        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<ValidateOrderResultDto>.FailureResult($"Order {orderId} does not exist.");
        }

        bool hasItems = order.OrderItems.Any();
        bool hasValidAmount = order.TotalAmount > 0;
        bool hasValidDoctor = order.DoctorID > 0;
        bool notCancelled = order.Status != OrderStatuses.Cancelled;
        bool isValid = hasItems && hasValidAmount && hasValidDoctor && notCancelled;

        var result = new ValidateOrderResultDto
        {
            OrderId = order.OrderId,
            IsValid = isValid,
            CurrentStatus = order.Status,
            TotalAmount = order.TotalAmount,
            ItemCount = order.OrderItems.Count,
            Message = isValid
                ? "Order is valid and ready for admin verification."
                : "Order validation failed: missing items, non-positive amount, or invalid doctor reference."
        };

        return ApiResponse<ValidateOrderResultDto>.SuccessResult(result, result.Message);
    }

    private static OrderResponseDto MapToDto(Order order) => new()
    {
        OrderId = order.OrderId,
        DoctorID = order.DoctorID,
        OrderDate = order.OrderDate,
        TotalAmount = order.TotalAmount,
        Status = order.Status,
        OrderItems = order.OrderItems.Select(oi => new OrderItemResponseDto
        {
            OrderItemId = oi.OrderItemId,
            OrderId = oi.OrderId,
            DrugId = oi.DrugId,
            DrugName = oi.DrugName,
            Quantity = oi.Quantity,
            UnitPrice = oi.UnitPrice
        }).ToList()
    };
}
