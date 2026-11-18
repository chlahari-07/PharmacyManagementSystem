using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PharmacyManagement.Common.Models;
using SaleReportService.DTOs;
using SaleReportService.Services;

namespace SaleReportService.Controllers;

[ApiController]
[Route("api/[controller]")]
public class SaleReportsController : ControllerBase
{
    private readonly ISaleReportService _saleReportService;

    public SaleReportsController(ISaleReportService saleReportService)
    {
        _saleReportService = saleReportService;
    }

    /// <summary>
    /// View all generated sales reports (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<SaleReportDto>>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAllReports()
    {
        var result = await _saleReportService.GetAllReportsAsync();
        return Ok(result);
    }

    /// <summary>
    /// View sales report details by ID (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<SaleReportDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetReportById(int id)
    {
        var result = await _saleReportService.GetReportByIdAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }

    /// <summary>
    /// Generate a new sales report: Daily, Weekly, Monthly, or Yearly (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpPost("generate")]
    [ProducesResponseType(typeof(ApiResponse<SaleReportDto>), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> GenerateReport([FromBody] GenerateSaleReportRequestDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage).ToList();
            return BadRequest(ApiResponse<SaleReportDto>.FailureResult("Validation error", errors));
        }

        var result = await _saleReportService.GenerateReportAsync(dto);
        return CreatedAtAction(nameof(GetReportById), new { id = result.Data!.SaleReportId }, result);
    }

    /// <summary>
    /// Download sales report as a CSV file (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("{id:int}/download")]
    [ProducesResponseType(typeof(FileContentResult), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DownloadReport(int id)
    {
        var export = await _saleReportService.ExportCsvAsync(id);
        if (export == null)
        {
            return NotFound(ApiResponse<string>.FailureResult($"Sale report ID {id} not found."));
        }

        return File(export.Value.FileBytes, export.Value.ContentType, export.Value.FileName);
    }

    /// <summary>
    /// Print sales report - retrieves formatted printable report layout (Admin only)
    /// </summary>
    [Authorize(Roles = UserRoles.Admin)]
    [HttpGet("{id:int}/print")]
    [ProducesResponseType(typeof(ApiResponse<PrintableReportDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> PrintReport(int id)
    {
        var result = await _saleReportService.GetPrintableReportAsync(id);
        if (!result.Success) return NotFound(result);
        return Ok(result);
    }
}
