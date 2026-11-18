using InventoryService.Models;
using Microsoft.EntityFrameworkCore;

namespace InventoryService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(InventoryDbContext context)
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

        if (await context.Drugs.AnyAsync())
        {
            return;
        }

        // Seed Suppliers
        var supplier1 = new Supplier
        {
            SupplierName = "Apex Pharma Logistics",
            Email = "contact@apexpharma.com",
            PhoneNumber = "+1555123456",
            Address = "100 Medical Boulevard, Suite 400, Chicago, IL"
        };

        var supplier2 = new Supplier
        {
            SupplierName = "BioCare Health Supplies",
            Email = "sales@biocare.com",
            PhoneNumber = "+1555987654",
            Address = "742 Healthcare Parkway, Boston, MA"
        };

        context.Suppliers.AddRange(supplier1, supplier2);
        await context.SaveChangesAsync();

        // Seed Drugs
        var drug1 = new Drug
        {
            Name = "Paracetamol 500mg",
            Description = "Pain reliever and a fever reducer (Acetaminophen)",
            Price = 9.99m,
            ExpiryDate = DateTime.UtcNow.AddYears(2),
            Quantity = 200,
            IsAvailable = true
        };

        var drug2 = new Drug
        {
            Name = "Amoxicillin 250mg",
            Description = "Broad-spectrum penicillin antibiotic",
            Price = 18.50m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 150,
            IsAvailable = true
        };

        var drug3 = new Drug
        {
            Name = "Ibuprofen 400mg",
            Description = "Nonsteroidal anti-inflammatory drug (NSAID)",
            Price = 12.00m,
            ExpiryDate = DateTime.UtcNow.AddMonths(18),
            Quantity = 300,
            IsAvailable = true
        };

        var drug4 = new Drug
        {
            Name = "Metformin 500mg",
            Description = "Oral diabetes medicine for blood sugar control",
            Price = 15.75m,
            ExpiryDate = DateTime.UtcNow.AddYears(2),
            Quantity = 120,
            IsAvailable = true
        };

        context.Drugs.AddRange(drug1, drug2, drug3, drug4);
        await context.SaveChangesAsync();

        // Seed Inventory records
        var inv1 = new Inventory
        {
            SupplierId = supplier1.SupplierId,
            DrugId = drug1.DrugId,
            PurchasePrice = 5.50m,
            QuantityAdded = 200,
            StockReceivedDate = DateTime.UtcNow.AddDays(-30)
        };

        var inv2 = new Inventory
        {
            SupplierId = supplier1.SupplierId,
            DrugId = drug2.DrugId,
            PurchasePrice = 11.00m,
            QuantityAdded = 150,
            StockReceivedDate = DateTime.UtcNow.AddDays(-20)
        };

        var inv3 = new Inventory
        {
            SupplierId = supplier2.SupplierId,
            DrugId = drug3.DrugId,
            PurchasePrice = 7.00m,
            QuantityAdded = 300,
            StockReceivedDate = DateTime.UtcNow.AddDays(-15)
        };

        var inv4 = new Inventory
        {
            SupplierId = supplier2.SupplierId,
            DrugId = drug4.DrugId,
            PurchasePrice = 9.20m,
            QuantityAdded = 120,
            StockReceivedDate = DateTime.UtcNow.AddDays(-10)
        };

        context.Inventories.AddRange(inv1, inv2, inv3, inv4);
        await context.SaveChangesAsync();
    }
}
