using InventoryService.DTOs;
using InventoryService.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PharmacyManagement.Common.Models;

namespace InventoryService.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DrugsController : ControllerBase
{
    private readonly IDrugService _drugService;

    public DrugsController(IDrugService drugService)
    {
        _drugService = drugService;
    }

    /// <summary>
    /// View all drugs (Available to both Admin and Doctor users)
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<DrugDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAllDrugs([FromQuery] bool availableOnly = false)
    {
        var result = await _drugService.GetAllDrugsAsync(availableOnly);
        return Ok(result);
    }

    /// <summary>
    /// View details of a specific drug by ID (Admin and Doctor)
    /// </summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<DrugDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetDrugById(int id)
    {
        var result = await _drugService.GetDrugByIdAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Low Stock Monitoring: View medicines whose stock is below the minimum stock level (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("low-stock")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<DrugDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetLowStockDrugs()
    {
        var result = await _drugService.GetLowStockDrugsAsync();
        return Ok(result);
    }

    /// <summary>
    /// Expired Drug Report: View medicines that have passed their expiry date (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("expired")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<DrugDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetExpiredDrugs()
    {
        var result = await _drugService.GetExpiredDrugsAsync();
        return Ok(result);
    }

    /// <summary>
    /// Search drugs by name or category (Admin and Doctor)
    /// </summary>
    [HttpGet("search")]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<DrugDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> SearchDrugs([FromQuery] string? query, [FromQuery] string? category)
    {
        var result = await _drugService.SearchDrugsAsync(query, category);
        return Ok(result);
    }

    /// <summary>
    /// Add a new drug (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<DrugDto>), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> CreateDrug([FromBody] CreateDrugDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<DrugDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _drugService.CreateDrugAsync(dto);
        return CreatedAtAction(nameof(GetDrugById), new { id = result.Data!.DrugId }, result);
    }

    /// <summary>
    /// Edit an existing drug (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPut("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<DrugDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateDrug(int id, [FromBody] UpdateDrugDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<DrugDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _drugService.UpdateDrugAsync(id, dto);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Delete a drug (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpDelete("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<bool>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteDrug(int id)
    {
        var result = await _drugService.DeleteDrugAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Check stock availability for multiple drug items (Inter-service / OrderService)
    /// </summary>
    [HttpPost("check-availability")]
    [ProducesResponseType(typeof(ApiResponse<StockCheckResultDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> CheckAvailability([FromBody] DeductStockRequestDto request)
    {
        var result = await _drugService.CheckAvailabilityAsync(request);
        return Ok(result);
    }

    /// <summary>
    /// Deduct stock for ordered items (Inter-service / OrderService)
    /// </summary>
    [HttpPost("deduct-stock")]
    [ProducesResponseType(typeof(ApiResponse<bool>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> DeductStock([FromBody] DeductStockRequestDto request)
    {
        var result = await _drugService.DeductStockAsync(request);
        if (!result.Success) return BadRequest(result);
        return Ok(result);
    }
}

[ApiController]
[Route("api/[controller]")]
public class SuppliersController : ControllerBase
{
    private readonly ISupplierService _supplierService;

    public SuppliersController(ISupplierService supplierService)
    {
        _supplierService = supplierService;
    }

    /// <summary>
    /// View all suppliers (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<SupplierDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAllSuppliers()
    {
        var result = await _supplierService.GetAllSuppliersAsync();
        return Ok(result);
    }

    /// <summary>
    /// View details of a specific supplier by ID (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<SupplierDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetSupplierById(int id)
    {
        var result = await _supplierService.GetSupplierByIdAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Add a new supplier (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<SupplierDto>), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> CreateSupplier([FromBody] CreateSupplierDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<SupplierDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _supplierService.CreateSupplierAsync(dto);
        return CreatedAtAction(nameof(GetSupplierById), new { id = result.Data!.SupplierId }, result);
    }

    /// <summary>
    /// Edit an existing supplier (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPut("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<SupplierDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateSupplier(int id, [FromBody] UpdateSupplierDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<SupplierDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _supplierService.UpdateSupplierAsync(id, dto);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Delete a supplier (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpDelete("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<bool>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteSupplier(int id)
    {
        var result = await _supplierService.DeleteSupplierAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }
}

[ApiController]
[Route("api/[controller]")]
public class InventoryController : ControllerBase
{
    private readonly IInventoryService _inventoryService;

    public InventoryController(IInventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }

    /// <summary>
    /// View all inventory stock records with Drug and Supplier details (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<InventoryDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAllInventory()
    {
        var result = await _inventoryService.GetAllInventoryAsync();
        return Ok(result);
    }

    /// <summary>
    /// Add stock to inventory linking Supplier and Drug with purchase price (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<InventoryDto>), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> AddInventoryStock([FromBody] CreateInventoryStockDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<InventoryDto>.FailureResult("Validation failed.", errors));
        }

        var result = await _inventoryService.AddInventoryStockAsync(dto);
        if (!result.Success) return BadRequest(result);
        return Ok(result);
    }
}
