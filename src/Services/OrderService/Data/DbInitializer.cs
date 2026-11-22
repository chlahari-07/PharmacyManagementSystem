using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using OrderService.Models;
using PharmacyManagement.Common.Models;

namespace OrderService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(
        OrderDbContext context,
        ILogger logger,
        IHostEnvironment environment)
    {
        if (context.Database.IsRelational())
        {
            try
            {
                logger.LogInformation("Applying EF Core migrations to SQL Server for OrderService (Pharmacy_OrderDB)...");
                await context.Database.MigrateAsync();
                logger.LogInformation("EF Core migrations applied successfully for OrderService.");
            }
            catch (Exception ex)
            {
                logger.LogCritical(ex, "FATAL: Database migration failed for OrderService! Application startup aborted.");
                throw;
            }
        }
        else
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.Orders.AnyAsync())
        {
            logger.LogInformation("Order database already contains orders. Skipping seed data.");
            return;
        }

        logger.LogInformation("Seeding initial doctor sample orders...");

        // Seed sample orders for doctor ID 2 (Dr. Robert Smith)
        var order1 = new Order
        {
            DoctorID = 2,
            OrderDate = DateTime.UtcNow.AddDays(-5),
            TotalAmount = 56.98m,
            Status = OrderStatuses.Verified,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 1, DrugName = "Paracetamol 500mg", Quantity = 2, UnitPrice = 9.99m },
                new() { DrugId = 2, DrugName = "Amoxicillin 250mg", Quantity = 2, UnitPrice = 18.50m }
            }
        };

        var order2 = new Order
        {
            DoctorID = 2,
            OrderDate = DateTime.UtcNow.AddDays(-2),
            TotalAmount = 24.00m,
            Status = OrderStatuses.PickedUp,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 3, DrugName = "Ibuprofen 400mg", Quantity = 2, UnitPrice = 12.00m }
            }
        };

        var order3 = new Order
        {
            DoctorID = 2,
            OrderDate = DateTime.UtcNow.AddHours(-3),
            TotalAmount = 31.50m,
            Status = OrderStatuses.Pending,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 4, DrugName = "Metformin 500mg", Quantity = 2, UnitPrice = 15.75m }
            }
        };

        context.Orders.AddRange(order1, order2, order3);
        await context.SaveChangesAsync();
        logger.LogInformation("Sample orders seeded successfully.");
    }
}
