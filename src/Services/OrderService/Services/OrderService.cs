using OrderService.DTOs;
using OrderService.Models;
using OrderService.Repositories;
using PharmacyManagement.Common.Models;

namespace OrderService.Services;

public interface IOrderService
{
    Task<ApiResponse<OrderResponseDto>> CreateOrderAsync(int doctorId, CreateOrderDto dto);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetMyOrdersAsync(int doctorId);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetAllOrdersAsync();
    Task<ApiResponse<OrderResponseDto>> GetOrderByIdAsync(int orderId);
    Task<ApiResponse<OrderResponseDto>> VerifyOrderAsync(int orderId);
    Task<ApiResponse<OrderResponseDto>> MarkOrderAsPickedUpAsync(int orderId);
    Task<ApiResponse<IEnumerable<OrderResponseDto>>> GetPickedUpOrdersAsync();
    Task<ApiResponse<OrderResponseDto>> UpdateOrderStatusAsync(int orderId, string status);
    Task<ApiResponse<bool>> ValidateOrderAsync(int orderId);
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

        decimal totalAmount = dto.Items.Sum(i => i.Quantity * i.UnitPrice);

        var order = new Order
        {
            DoctorID = doctorId,
            OrderDate = DateTime.UtcNow,
            TotalAmount = totalAmount,
            Status = string.Equals(dto.Status, OrderStatuses.Cart, StringComparison.OrdinalIgnoreCase)
                ? OrderStatuses.Cart
                : OrderStatuses.Pending,
            OrderItems = dto.Items.Select(i => new OrderItem
            {
                DrugId = i.DrugId,
                DrugName = i.DrugName.Trim(),
                Quantity = i.Quantity,
                UnitPrice = i.UnitPrice
            }).ToList()
        };

        // If placing an active order (Pending), trigger inventory stock deduction
        if (order.Status == OrderStatuses.Pending)
        {
            var stockDeductRequest = new InterServiceDeductStockRequest
            {
                Items = dto.Items.Select(i => new InterServiceDeductStockItem
                {
                    DrugId = i.DrugId,
                    Quantity = i.Quantity
                }).ToList()
            };

            await _inventoryClient.DeductStockAsync(stockDeductRequest);
        }

        var created = await _orderRepository.CreateOrderAsync(order);
        return ApiResponse<OrderResponseDto>.SuccessResult(MapToDto(created), "Order placed successfully.");
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

    public async Task<ApiResponse<OrderResponseDto>> UpdateOrderStatusAsync(int orderId, string status)
    {
        if (!OrderStatuses.ValidStatuses.Contains(status))
        {
            return ApiResponse<OrderResponseDto>.FailureResult($"Invalid order status '{status}'. Valid: Cart, Pending, Verified, PickedUp.");
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

    public async Task<ApiResponse<bool>> ValidateOrderAsync(int orderId)
    {
        var order = await _orderRepository.GetOrderByIdAsync(orderId);
        if (order == null)
        {
            return ApiResponse<bool>.FailureResult($"Order {orderId} does not exist.");
        }

        bool isValid = order.TotalAmount > 0 && order.OrderItems.Any() && order.DoctorID > 0;
        return ApiResponse<bool>.SuccessResult(isValid, isValid ? "Order is valid." : "Order validation failed.");
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
