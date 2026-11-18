using System.ComponentModel.DataAnnotations;

namespace SaleReportService.DTOs;

public class GenerateSaleReportRequestDto
{
    [Required]
    [RegularExpression("^(Daily|Weekly|Monthly|Yearly)$", ErrorMessage = "ReportType must be Daily, Weekly, Monthly, or Yearly.")]
    public string ReportType { get; set; } = "Daily";

    public DateTime? FromDate { get; set; }
    public DateTime? ToDate { get; set; }

    // Optional manual simulation inputs for testing in isolated Swagger mode
    public int? SimulatedTotalOrders { get; set; }
    public decimal? SimulatedTotalRevenue { get; set; }
    public decimal? SimulatedProfit { get; set; }
}

public class SaleReportDto
{
    public int SaleReportId { get; set; }
    public string ReportType { get; set; } = string.Empty;
    public DateTime FromDate { get; set; }
    public DateTime ToDate { get; set; }
    public int TotalOrders { get; set; }
    public decimal TotalRevenue { get; set; }
    public DateTime GeneratedDate { get; set; }
    public decimal Profit { get; set; }
    public decimal ProfitMarginPercentage => TotalRevenue > 0 ? Math.Round((Profit / TotalRevenue) * 100, 2) : 0;
}

public class PrintableReportDto
{
    public int SaleReportId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string ReportType { get; set; } = string.Empty;
    public string DateRange { get; set; } = string.Empty;
    public string GeneratedAt { get; set; } = string.Empty;
    public int TotalOrders { get; set; }
    public string TotalRevenueFormatted { get; set; } = string.Empty;
    public string ProfitFormatted { get; set; } = string.Empty;
    public string ProfitMarginFormatted { get; set; } = string.Empty;
    public string FormattedPrintView { get; set; } = string.Empty;
}

public class InterServiceOrderSummaryDto
{
    public int OrderId { get; set; }
    public DateTime OrderDate { get; set; }
    public decimal TotalAmount { get; set; }
    public string Status { get; set; } = string.Empty;
}
