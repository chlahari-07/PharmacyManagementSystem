using Microsoft.EntityFrameworkCore;
using PaymentService.Models;
using PharmacyManagement.Common.Models;

namespace PaymentService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(PaymentDbContext context)
    {
        try
        {
            if (context.Database.IsRelational())
            {
                await context.Database.MigrateAsync();
            }
            else
            {
                await context.Database.EnsureCreatedAsync();
            }
        }
        catch
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.Payments.AnyAsync())
        {
            return;
        }

        var payment1 = new Payment
        {
            OrderId = 1,
            Amount = 48.49m,
            PaymentDate = DateTime.UtcNow.AddDays(-2),
            PaymentMethod = "CreditCard",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "TXN-" + Guid.NewGuid().ToString("N")[..12].ToUpper()
        };

        var payment3 = new Payment
        {
            OrderId = 3,
            Amount = 31.50m,
            PaymentDate = DateTime.UtcNow.AddDays(-5),
            PaymentMethod = "UPI",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "TXN-" + Guid.NewGuid().ToString("N")[..12].ToUpper()
        };

        context.Payments.AddRange(payment1, payment3);
        await context.SaveChangesAsync();
    }
}
