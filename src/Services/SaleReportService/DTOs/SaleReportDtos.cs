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

public class DashboardAnalyticsDto
{
    public int TotalOrders { get; set; }
    public decimal TotalRevenue { get; set; }
    public decimal TotalProfit { get; set; }
    public decimal ProfitMarginPercentage => TotalRevenue > 0 ? Math.Round((TotalProfit / TotalRevenue) * 100, 2) : 0;
    public decimal AverageOrderValue => TotalOrders > 0 ? Math.Round(TotalRevenue / TotalOrders, 2) : 0;
    public int VerifiedOrdersCount { get; set; }
    public int PickedUpOrdersCount { get; set; }
    public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;
}

public class ProfitItemDto
{
    public int DrugId { get; set; }
    public string DrugName { get; set; } = string.Empty;
    public decimal SellingPrice { get; set; }
    public decimal PurchasePrice { get; set; }
    public decimal UnitProfit => SellingPrice - PurchasePrice;
    public int QuantitySold { get; set; }
    public decimal TotalRevenue => QuantitySold * SellingPrice;
    public decimal TotalCost => QuantitySold * PurchasePrice;
    public decimal TotalProfit => QuantitySold * UnitProfit;
    public decimal MarginPercentage => SellingPrice > 0 ? Math.Round(((SellingPrice - PurchasePrice) / SellingPrice) * 100, 2) : 0;
}

public class ProfitAnalysisDto
{
    public decimal TotalRevenue { get; set; }
    public decimal TotalCostOfGoods { get; set; }
    public decimal NetProfit { get; set; }
    public decimal OverallMarginPercentage => TotalRevenue > 0 ? Math.Round((NetProfit / TotalRevenue) * 100, 2) : 0;
    public string Period { get; set; } = "All-Time";
    public List<ProfitItemDto> DrugBreakdown { get; set; } = new();
}

public class TopSellingDrugDto
{
    public int Rank { get; set; }
    public int DrugId { get; set; }
    public string DrugName { get; set; } = string.Empty;
    public int UnitsSold { get; set; }
    public decimal TotalRevenue { get; set; }
    public decimal TotalProfit { get; set; }
}

public class InterServiceOrderItemDto
{
    public int DrugId { get; set; }
    public string DrugName { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
}

public class InterServiceOrderDetailsDto
{
    public int OrderId { get; set; }
    public int DoctorID { get; set; }
    public DateTime OrderDate { get; set; }
    public decimal TotalAmount { get; set; }
    public string Status { get; set; } = string.Empty;
    public List<InterServiceOrderItemDto> OrderItems { get; set; } = new();
}
