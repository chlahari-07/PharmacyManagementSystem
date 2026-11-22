using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using PaymentService.Models;
using PharmacyManagement.Common.Models;

namespace PaymentService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(
        PaymentDbContext context,
        ILogger logger,
        IHostEnvironment environment)
    {
        if (context.Database.IsRelational())
        {
            try
            {
                logger.LogInformation("Applying EF Core migrations to SQL Server for PaymentService (Pharmacy_PaymentDB)...");
                await context.Database.MigrateAsync();
                logger.LogInformation("EF Core migrations applied successfully for PaymentService.");
            }
            catch (Exception ex)
            {
                logger.LogCritical(ex, "FATAL: Database migration failed for PaymentService! Application startup aborted.");
                throw;
            }
        }
        else
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.Payments.AnyAsync())
        {
            logger.LogInformation("Payment database already contains payments. Skipping seed data.");
            return;
        }

        logger.LogInformation("Seeding initial simulated payments...");

        // Pre-seed sample simulated payments corresponding to initial verified and picked-up orders
        var payment1 = new Payment
        {
            OrderId = 1,
            Amount = 56.98m,
            PaymentDate = DateTime.UtcNow.AddDays(-5),
            PaymentMethod = "CreditCard",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "SIM-TXN-INIT-001"
        };

        var payment2 = new Payment
        {
            OrderId = 2,
            Amount = 24.00m,
            PaymentDate = DateTime.UtcNow.AddDays(-2),
            PaymentMethod = "UPI",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "SIM-TXN-INIT-002"
        };

        context.Payments.AddRange(payment1, payment2);
        await context.SaveChangesAsync();
        logger.LogInformation("Initial simulated payments seeded successfully.");
    }
}
