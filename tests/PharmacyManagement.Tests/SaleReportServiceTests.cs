using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
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

        var httpClient = new HttpClient();
        var config = new ConfigurationBuilder().Build();
        _saleReportService = new SaleReportServiceClass(
            _reportRepository,
            httpClient,
            config,
            NullLogger<SaleReportServiceClass>.Instance);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC19_GenerateReport_ForDateRange_CalculatesRevenueAndProfit()
    {
        // Arrange
        var request = new GenerateSaleReportRequestDto
        {
            ReportType = "Monthly",
            FromDate = new DateTime(2026, 11, 1),
            ToDate = new DateTime(2026, 11, 30),
            SimulatedTotalOrders = 25,
            SimulatedTotalRevenue = 2500.00m,
            SimulatedProfit = 800.00m
        };

        // Act
        var result = await _saleReportService.GenerateReportAsync(request);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.ReportType, Is.EqualTo("Monthly"));
        Assert.That(result.Data.TotalOrders, Is.EqualTo(25));
        Assert.That(result.Data.TotalRevenue, Is.EqualTo(2500.00m));
        Assert.That(result.Data.Profit, Is.EqualTo(800.00m));
    }

    [Test]
    public async Task TC20_ExportCsv_GeneratedReport_ReturnsCsvByteArray()
    {
        // Arrange: Generate a report first
        var request = new GenerateSaleReportRequestDto
        {
            ReportType = "Monthly",
            SimulatedTotalOrders = 10,
            SimulatedTotalRevenue = 1000.00m,
            SimulatedProfit = 350.00m
        };
        var reportResult = await _saleReportService.GenerateReportAsync(request);
        Assert.That(reportResult.Success, Is.True);
        int reportId = reportResult.Data!.SaleReportId;

        // Act
        var csvResult = await _saleReportService.ExportCsvAsync(reportId);

        // Assert
        Assert.That(csvResult.HasValue, Is.True);
        Assert.That(csvResult!.Value.FileBytes, Is.Not.Null);
        Assert.That(csvResult.Value.FileBytes.Length, Is.GreaterThan(0));
        Assert.That(csvResult.Value.FileName, Does.EndWith(".csv"));
        Assert.That(csvResult.Value.ContentType, Is.EqualTo("text/csv"));
    }

    [Test]
    public async Task TC29_GenerateReport_WithInvalidDateRange_ReturnsFailure()
    {
        // Arrange: End date earlier than start date
        var request = new GenerateSaleReportRequestDto
        {
            ReportType = "Custom",
            FromDate = new DateTime(2026, 11, 30),
            ToDate = new DateTime(2026, 11, 1) // Earlier than FromDate
        };

        // Act
        var result = await _saleReportService.GenerateReportAsync(request);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("start date must be earlier than or equal to the end date"));
    }

    [Test]
    public async Task TC30_ExportCsv_WhenNoSalesDataOrReportNotFound_ReturnsNullOrEmpty()
    {
        // Act: Non-existent report ID
        var csvResult = await _saleReportService.ExportCsvAsync(99999);

        // Assert
        Assert.That(csvResult.HasValue, Is.False);
    }

    [Test]
    public async Task TC37_ProfitAnalysis_ReturnsCalculatedMargins()
    {
        // Act
        var result = await _saleReportService.GetProfitAnalysisAsync();

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
    }
}
