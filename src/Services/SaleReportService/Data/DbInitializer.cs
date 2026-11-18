using Microsoft.EntityFrameworkCore;
using PharmacyManagement.Common.Models;
using SaleReportService.Models;

namespace SaleReportService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(SaleReportDbContext context)
    {
        try
        {
            if (context.Database.IsRelational())
            {
                await context.Database.EnsureCreatedAsync();
            }
        }
        catch
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.SaleReports.AnyAsync())
        {
            return;
        }

        var now = DateTime.UtcNow;

        var dailyReport = new SaleReport
        {
            ReportType = ReportTypes.Daily,
            FromDate = now.Date,
            ToDate = now.Date.AddDays(1).AddTicks(-1),
            TotalOrders = 12,
            TotalRevenue = 1540.00m,
            GeneratedDate = now,
            Profit = 462.00m // ~30% net profit
        };

        var weeklyReport = new SaleReport
        {
            ReportType = ReportTypes.Weekly,
            FromDate = now.AddDays(-7).Date,
            ToDate = now.Date.AddDays(1).AddTicks(-1),
            TotalOrders = 84,
            TotalRevenue = 10850.50m,
            GeneratedDate = now,
            Profit = 3255.15m
        };

        var monthlyReport = new SaleReport
        {
            ReportType = ReportTypes.Monthly,
            FromDate = new DateTime(now.Year, now.Month, 1),
            ToDate = now,
            TotalOrders = 340,
            TotalRevenue = 45200.00m,
            GeneratedDate = now,
            Profit = 14464.00m
        };

        context.SaleReports.AddRange(dailyReport, weeklyReport, monthlyReport);
        await context.SaveChangesAsync();
    }
}
