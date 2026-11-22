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

        int doctorId = ExtractDoctorId(dto.DoctorId);
        if (doctorId <= 0)
        {
            return BadRequest(ApiResponse<OrderResponseDto>.FailureResult("Doctor ID could not be identified from authentication token."));
        }

        var result = await _orderService.CreateOrderAsync(doctorId, dto);
        if (!result.Success) return BadRequest(result);

        return CreatedAtAction(nameof(GetOrderById), new { id = result.Data!.OrderId }, result);
    }

    /// <summary>
    /// Add drugs to cart (Doctor user)
    /// </summary>
    [Authorize(Roles = UserRoles.Doctor)]
    [HttpPost("cart")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> AddToCart([FromBody] AddToCartDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<OrderResponseDto>.FailureResult("Validation error", errors));
        }

        int doctorId = ExtractDoctorId(dto.DoctorId);
        if (doctorId <= 0)
        {
            return BadRequest(ApiResponse<OrderResponseDto>.FailureResult("Doctor ID could not be identified from authentication token."));
        }

        var result = await _orderService.AddToCartAsync(doctorId, dto);
        if (!result.Success) return BadRequest(result);

        return Ok(result);
    }

    /// <summary>
    /// View active cart for doctor (Doctor user)
    /// </summary>
    [Authorize(Roles = UserRoles.Doctor)]
    [HttpGet("cart")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<OrderResponseDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetCart()
    {
        int doctorId = ExtractDoctorId(null);
        if (doctorId <= 0)
        {
            return Unauthorized(ApiResponse<IEnumerable<OrderResponseDto>>.FailureResult("Unauthorized doctor token."));
        }

        var result = await _orderService.GetCartAsync(doctorId);
        return Ok(result);
    }

    /// <summary>
    /// View order history placed by the current Doctor (Doctor user)
    /// </summary>
    [Authorize(Roles = UserRoles.Doctor)]
    [HttpGet("my-orders")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<OrderResponseDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetMyOrders()
    {
        int doctorId = ExtractDoctorId(null);
        if (doctorId <= 0)
        {
            return Unauthorized(ApiResponse<IEnumerable<OrderResponseDto>>.FailureResult("Unauthorized doctor token."));
        }

        var result = await _orderService.GetMyOrdersAsync(doctorId);
        return Ok(result);
    }

    /// <summary>
    /// Track order status and details by Order ID (Doctor can view own order, Admin can view any)
    /// </summary>
    [Authorize]
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetOrderById(int id)
    {
        var result = await _orderService.GetOrderByIdAsync(id);
        if (!result.Success || result.Data == null) return NotFound(result);

        // Ownership check: Doctor can only access their own order
        var userRole = User.FindFirstValue(ClaimTypes.Role);
        int currentUserId = ExtractDoctorId(null);

        if (string.Equals(userRole, UserRoles.Doctor, StringComparison.OrdinalIgnoreCase) &&
            result.Data.DoctorID != currentUserId)
        {
            return StatusCode(StatusCodes.Status403Forbidden,
                ApiResponse<OrderResponseDto>.FailureResult("Access denied: You can only view orders placed by yourself."));
        }

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
    /// Check if order is valid before verification (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("{id:int}/validate")]
    [ProducesResponseType(typeof(ApiResponse<ValidateOrderResultDto>), StatusCodes.Status200OK)]
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
    /// View all PickedUp orders in the pickedUp section (Admin only)
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
    /// Cancel an order (Doctor can cancel own order before pickup, Admin can cancel any)
    /// </summary>
    [Authorize]
    [HttpPut("{id:int}/cancel")]
    [ProducesResponseType(typeof(ApiResponse<OrderResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> CancelOrder(int id)
    {
        var orderResult = await _orderService.GetOrderByIdAsync(id);
        if (!orderResult.Success || orderResult.Data == null) return NotFound(orderResult);

        // Ownership check: Doctor can only cancel their own order
        var userRole = User.FindFirstValue(ClaimTypes.Role);
        int currentUserId = ExtractDoctorId(null);

        if (string.Equals(userRole, UserRoles.Doctor, StringComparison.OrdinalIgnoreCase) &&
            orderResult.Data.DoctorID != currentUserId)
        {
            return StatusCode(StatusCodes.Status403Forbidden,
                ApiResponse<OrderResponseDto>.FailureResult("Access denied: You can only cancel your own orders."));
        }

        var result = await _orderService.CancelOrderAsync(id);
        if (!result.Success) return BadRequest(result);
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

    private int ExtractDoctorId(int? fallbackId)
    {
        var userIdClaim = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (!string.IsNullOrEmpty(userIdClaim) && int.TryParse(userIdClaim, out int parsedId))
        {
            return parsedId;
        }
        return fallbackId ?? 0;
    }
}
