using Microsoft.EntityFrameworkCore;
using OrderService.Models;
using PharmacyManagement.Common.Models;

namespace OrderService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(OrderDbContext context)
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

        if (await context.Orders.AnyAsync())
        {
            return;
        }

        // Seed sample orders for doctor testing
        var order1 = new Order
        {
            DoctorID = 2, // Dr. Robert Smith
            OrderDate = DateTime.UtcNow.AddDays(-2),
            TotalAmount = 48.49m,
            Status = OrderStatuses.Verified,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 1, DrugName = "Paracetamol 500mg", Quantity = 3, UnitPrice = 9.99m },
                new() { DrugId = 2, DrugName = "Amoxicillin 250mg", Quantity = 1, UnitPrice = 18.50m }
            }
        };

        var order2 = new Order
        {
            DoctorID = 2,
            OrderDate = DateTime.UtcNow.AddDays(-1),
            TotalAmount = 24.00m,
            Status = OrderStatuses.Pending,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 3, DrugName = "Ibuprofen 400mg", Quantity = 2, UnitPrice = 12.00m }
            }
        };

        var order3 = new Order
        {
            DoctorID = 2,
            OrderDate = DateTime.UtcNow.AddDays(-5),
            TotalAmount = 31.50m,
            Status = OrderStatuses.PickedUp,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 4, DrugName = "Metformin 500mg", Quantity = 2, UnitPrice = 15.75m }
            }
        };

        context.Orders.AddRange(order1, order2, order3);
        await context.SaveChangesAsync();
    }
}
