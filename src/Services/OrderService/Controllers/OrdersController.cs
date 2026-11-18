using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OrderService.DTOs;
using OrderService.Services;
using PharmacyManagement.Common.Models;

namespace OrderService.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrdersController(IOrderService orderService)
    {
        _orderService = orderService;
    }

    /// <summary>
    /// Buy drugs / Place order (Doctor user)
    /// </summary>
    [Authorize(Roles = UserRoles.Doctor)]
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> PlaceOrder([FromBody] CreateOrderDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<OrderResponseDto>.FailureResult("Validation error", errors));
        }

        // Extract Doctor ID from JWT claims
        int doctorId = 0;
        var userIdClaim = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (!string.IsNullOrEmpty(userIdClaim) && int.TryParse(userIdClaim, out int parsedId))
        {
            doctorId = parsedId;
        }
        else if (dto.DoctorId.HasValue)
        {
            doctorId = dto.DoctorId.Value;
        }

        if (doctorId <= 0)
        {
            return BadRequest(ApiResponse<OrderResponseDto>.FailureResult("Doctor ID could not be identified from authentication token."));
        }

        var result = await _orderService.CreateOrderAsync(doctorId, dto);
        if (!result.Success) return BadRequest(result);

        return CreatedAtAction(nameof(GetOrderById), new { id = result.Data!.OrderId }, result);
    }

    /// <summary>
    /// View orders placed by the current Doctor
    /// </summary>
    [Authorize(Roles = UserRoles.Doctor)]
    [HttpGet("my-orders")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<OrderResponseDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetMyOrders()
    {
        var userIdClaim = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (string.IsNullOrEmpty(userIdClaim) || !int.TryParse(userIdClaim, out int doctorId))
        {
            return Unauthorized(ApiResponse<IEnumerable<OrderResponseDto>>.FailureResult("Unauthorized doctor token."));
        }

        var result = await _orderService.GetMyOrdersAsync(doctorId);
        return Ok(result);
    }

    /// <summary>
    /// View doctor orders placed by all doctors (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<OrderResponseDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAllOrders()
    {
        var result = await _orderService.GetAllOrdersAsync();
        return Ok(result);
    }

    /// <summary>
    /// View order details by Order ID (Admin or Doctor)
    /// </summary>
    [Authorize]
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetOrderById(int id)
    {
        var result = await _orderService.GetOrderByIdAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Check if order is valid (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("{id:int}/validate")]
    [ProducesResponseType(typeof(ApiResponse<bool>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> ValidateOrder(int id)
    {
        var result = await _orderService.ValidateOrderAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Verify an order after validating it (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPut("{id:int}/verify")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> VerifyOrder(int id)
    {
        var result = await _orderService.VerifyOrderAsync(id);
        if (!result.Success) return BadRequest(result);
        return Ok(result);
    }

    /// <summary>
    /// Add order to pickedUp section (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPut("{id:int}/pickup")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> MarkOrderAsPickedUp(int id)
    {
        var result = await _orderService.MarkOrderAsPickedUpAsync(id);
        if (!result.Success) return BadRequest(result);
        return Ok(result);
    }

    /// <summary>
    /// View all PickedUp orders (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("picked-up")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<OrderResponseDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetPickedUpOrders()
    {
        var result = await _orderService.GetPickedUpOrdersAsync();
        return Ok(result);
    }

    /// <summary>
    /// Update order status manually (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPut("{id:int}/status")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> UpdateOrderStatus(int id, [FromBody] UpdateOrderStatusDto dto)
    {
        var result = await _orderService.UpdateOrderStatusAsync(id, dto.Status);
        if (!result.Success) return BadRequest(result);
        return Ok(result);
    }
}
