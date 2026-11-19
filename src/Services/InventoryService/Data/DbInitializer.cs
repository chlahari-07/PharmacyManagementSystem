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
            DrugName = "Paracetamol 500mg",
            Description = "Pain reliever and a fever reducer (Acetaminophen)",
            Category = "Analgesics",
            Price = 9.99m,
            ExpiryDate = DateTime.UtcNow.AddYears(2),
            Quantity = 200,
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        var drug2 = new Drug
        {
            DrugName = "Amoxicillin 250mg",
            Description = "Broad-spectrum penicillin antibiotic",
            Category = "Antibiotics",
            Price = 18.50m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 150,
            MinimumStockQuantity = 25,
            IsAvailable = true
        };

        var drug3 = new Drug
        {
            DrugName = "Ibuprofen 400mg",
            Description = "Nonsteroidal anti-inflammatory drug (NSAID)",
            Category = "Analgesics",
            Price = 12.00m,
            ExpiryDate = DateTime.UtcNow.AddMonths(18),
            Quantity = 300,
            MinimumStockQuantity = 30,
            IsAvailable = true
        };

        var drug4 = new Drug
        {
            DrugName = "Metformin 500mg",
            Description = "Oral diabetes medicine for blood sugar control",
            Category = "Antidiabetic",
            Price = 15.75m,
            ExpiryDate = DateTime.UtcNow.AddYears(2),
            Quantity = 120,
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        // Seed a low-stock drug for monitoring testing
        var drug5 = new Drug
        {
            DrugName = "Azithromycin 500mg",
            Description = "Macrolide antibiotic for bacterial infections",
            Category = "Antibiotics",
            Price = 24.50m,
            ExpiryDate = DateTime.UtcNow.AddMonths(8),
            Quantity = 8, // Low stock: 8 < MinimumStockQuantity (20)
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        // Seed an expired drug for expired report testing
        var drug6 = new Drug
        {
            DrugName = "Cough Syrup Dx 100ml",
            Description = "Antitussive cough suppressant",
            Category = "Cough & Cold",
            Price = 8.25m,
            ExpiryDate = DateTime.UtcNow.AddDays(-15), // Expired 15 days ago
            Quantity = 15,
            MinimumStockQuantity = 10,
            IsAvailable = false
        };

        context.Drugs.AddRange(drug1, drug2, drug3, drug4, drug5, drug6);
        await context.SaveChangesAsync();

        // Seed Inventory records
        var inv1 = new Inventory
        {
            SupplierId = supplier1.SupplierId,
            DrugId = drug1.DrugId,
            PurchasePrice = 5.50m,
            QuantitySupplied = 200,
            SupplyDate = DateTime.UtcNow.AddDays(-30),
            BatchNumber = "BATCH-PCM-2026",
            Notes = "Standard replenishment shipment"
        };

        var inv2 = new Inventory
        {
            SupplierId = supplier1.SupplierId,
            DrugId = drug2.DrugId,
            PurchasePrice = 11.00m,
            QuantitySupplied = 150,
            SupplyDate = DateTime.UtcNow.AddDays(-20),
            BatchNumber = "BATCH-AMX-2026",
            Notes = "Antibiotic restocking"
        };

        var inv3 = new Inventory
        {
            SupplierId = supplier2.SupplierId,
            DrugId = drug3.DrugId,
            PurchasePrice = 7.00m,
            QuantitySupplied = 300,
            SupplyDate = DateTime.UtcNow.AddDays(-15),
            BatchNumber = "BATCH-IBU-2026",
            Notes = "Anti-inflammatory stock"
        };

        var inv4 = new Inventory
        {
            SupplierId = supplier2.SupplierId,
            DrugId = drug4.DrugId,
            PurchasePrice = 9.20m,
            QuantitySupplied = 120,
            SupplyDate = DateTime.UtcNow.AddDays(-10),
            BatchNumber = "BATCH-MET-2026",
            Notes = "Diabetes care shipment"
        };

        context.Inventories.AddRange(inv1, inv2, inv3, inv4);
        await context.SaveChangesAsync();
    }
}
