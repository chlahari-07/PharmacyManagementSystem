using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging.Abstractions;
using NUnit.Framework;
using SaleReportService.Data;
using SaleReportService.DTOs;
using SaleReportService.Repositories;
using SaleReportService.Services;

namespace PharmacyManagement.Tests;

[TestFixture]
public class SaleReportServiceTests
{
    private SaleReportDbContext _context = null!;
    private ISaleReportRepository _reportRepository = null!;
    private ISaleReportService _saleReportService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<SaleReportDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new SaleReportDbContext(options);
        _reportRepository = new SaleReportRepository(_context);

        var httpClient = new HttpClient(); // Fallback mode
        _saleReportService = new SaleReportServiceClass(
            _reportRepository,
            httpClient,
            NullLogger<SaleReportServiceClass>.Instance);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC19_GenerateReport_Daily_CreatesReportWithCorrectProfitCalculation()
    {
        // Arrange
        var request = new GenerateSaleReportRequestDto
        {
            ReportType = "Daily",
            SimulatedTotalOrders = 15,
            SimulatedTotalRevenue = 1500.00m,
            SimulatedProfit = 525.00m // ~35%
        };

        // Act
        var result = await _saleReportService.GenerateReportAsync(request);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.ReportType, Is.EqualTo("Daily"));
        Assert.That(result.Data.TotalOrders, Is.EqualTo(15));
        Assert.That(result.Data.TotalRevenue, Is.EqualTo(1500.00m));
        Assert.That(result.Data.Profit, Is.EqualTo(525.00m));
        Assert.That(result.Data.ProfitMarginPercentage, Is.EqualTo(35.00m));
    }

    [Test]
    public async Task TC20_DashboardAnalytics_ReturnsAggregatedStatistics()
    {
        // Act
        var result = await _saleReportService.GetDashboardAnalyticsAsync();

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.TotalOrders, Is.GreaterThan(0));
        Assert.That(result.Data.TotalRevenue, Is.GreaterThan(0));
        Assert.That(result.Data.TotalProfit, Is.GreaterThan(0));
        Assert.That(result.Data.ProfitMarginPercentage, Is.GreaterThan(0));
    }

    [Test]
    public async Task TC21_ProfitAnalysis_CalculatesProfitBasedOnPurchaseAndSellingPrices()
    {
        // Act
        var result = await _saleReportService.GetProfitAnalysisAsync();

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.DrugBreakdown, Is.Not.Empty);

        foreach (var item in result.Data.DrugBreakdown)
        {
            Assert.That(item.SellingPrice, Is.GreaterThan(item.PurchasePrice));
            Assert.That(item.UnitProfit, Is.EqualTo(item.SellingPrice - item.PurchasePrice));
            Assert.That(item.TotalProfit, Is.EqualTo(item.QuantitySold * item.UnitProfit));
        }
    }

    [Test]
    public async Task TC22_TopSellingDrugs_ReturnsRankedMedicinesByQuantity()
    {
        // Act
        var result = await _saleReportService.GetTopSellingDrugsAsync(top: 3);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        var list = result.Data!.ToList();
        Assert.That(list.Count, Is.EqualTo(3));
        Assert.That(list[0].Rank, Is.EqualTo(1));
        Assert.That(list[0].UnitsSold, Is.GreaterThanOrEqualTo(list[1].UnitsSold));
    }
}
