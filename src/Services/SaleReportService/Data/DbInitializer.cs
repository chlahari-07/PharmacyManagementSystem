using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using PharmacyManagement.Common.Models;
using SaleReportService.Models;

namespace SaleReportService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(
        SaleReportDbContext context,
        ILogger logger,
        IHostEnvironment environment)
    {
        if (context.Database.IsRelational())
        {
            try
            {
                logger.LogInformation("Applying EF Core migrations to SQL Server for SaleReportService (Pharmacy_SaleReportDB)...");
                await context.Database.MigrateAsync();
                logger.LogInformation("EF Core migrations applied successfully for SaleReportService.");
            }
            catch (Exception ex)
            {
                logger.LogCritical(ex, "FATAL: Database migration failed for SaleReportService! Application startup aborted.");
                throw;
            }
        }
        else
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.SaleReports.AnyAsync())
        {
            logger.LogInformation("SaleReport database already contains historical reports. Skipping seed data.");
            return;
        }

        logger.LogInformation("Seeding initial historical sales reports...");

        var report1 = new SaleReport
        {
            ReportType = ReportTypes.Monthly,
            FromDate = new DateTime(DateTime.UtcNow.Year, DateTime.UtcNow.Month, 1).AddMonths(-1),
            ToDate = new DateTime(DateTime.UtcNow.Year, DateTime.UtcNow.Month, 1).AddDays(-1),
            TotalOrders = 142,
            TotalRevenue = 28450.00m,
            Profit = 9957.50m,
            GeneratedDate = DateTime.UtcNow.AddDays(-1)
        };

        var report2 = new SaleReport
        {
            ReportType = ReportTypes.Weekly,
            FromDate = DateTime.UtcNow.AddDays(-7).Date,
            ToDate = DateTime.UtcNow.Date,
            TotalOrders = 38,
            TotalRevenue = 7450.00m,
            Profit = 2607.50m,
            GeneratedDate = DateTime.UtcNow
        };

        context.SaleReports.AddRange(report1, report2);
        await context.SaveChangesAsync();
        logger.LogInformation("Initial sales reports seeded successfully.");
    }
}
