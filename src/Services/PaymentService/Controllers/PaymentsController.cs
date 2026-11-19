using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PaymentService.DTOs;
using PaymentService.Services;
using PharmacyManagement.Common.Models;

namespace PaymentService.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PaymentsController : ControllerBase
{
    private readonly IPaymentService _paymentService;

    public PaymentsController(IPaymentService paymentService)
    {
        _paymentService = paymentService;
    }

    /// <summary>
    /// Process payment for an order (Doctor checkout process)
    /// </summary>
    [Authorize]
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<PaymentResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> ProcessPayment([FromBody] ProcessPaymentDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<PaymentResponseDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _paymentService.ProcessPaymentAsync(dto);
        if (!result.Success) return BadRequest(result);

        return Ok(result);
    }

    /// <summary>
    /// Payment Simulation: Simulates payment gateway processing (Doctor user)
    /// </summary>
    [Authorize]
    [HttpPost("simulate")]
    [ProducesResponseType(typeof(ApiResponse<PaymentResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> SimulatePayment([FromBody] SimulatePaymentDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<PaymentResponseDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _paymentService.SimulatePaymentAsync(dto);
        if (!result.Success) return BadRequest(result);

        return Ok(result);
    }

    /// <summary>
    /// Get payment details for a specific Order ID (1:1 relationship)
    /// </summary>
    [Authorize]
    [HttpGet("order/{orderId:int}")]
    [ProducesResponseType(typeof(ApiResponse<PaymentResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetPaymentByOrderId(int orderId)
    {
        var result = await _paymentService.GetPaymentByOrderIdAsync(orderId);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Get payment details by Payment ID
    /// </summary>
    [Authorize]
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<PaymentResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetPaymentById(int id)
    {
        var result = await _paymentService.GetPaymentByIdAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// View all payment transactions (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<PaymentResponseDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAllPayments()
    {
        var result = await _paymentService.GetAllPaymentsAsync();
        return Ok(result);
    }

    /// <summary>
    /// Manually update payment status (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPut("{id:int}/status")]
    [ProducesResponseType(typeof(ApiResponse<PaymentResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> UpdatePaymentStatus(int id, [FromBody] UpdatePaymentStatusDto dto)
    {
        var result = await _paymentService.UpdatePaymentStatusAsync(id, dto.PaymentStatus);
        if (!result.Success) return BadRequest(result);
        return Ok(result);
    }
}
