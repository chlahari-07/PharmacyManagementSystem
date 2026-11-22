using InventoryService.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace InventoryService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(
        InventoryDbContext context,
        ILogger logger,
        IHostEnvironment environment)
    {
        if (context.Database.IsRelational())
        {
            try
            {
                logger.LogInformation("Applying EF Core migrations to SQL Server for InventoryService (Pharmacy_InventoryDB)...");
                await context.Database.MigrateAsync();
                logger.LogInformation("EF Core migrations applied successfully for InventoryService.");
            }
            catch (Exception ex)
            {
                logger.LogCritical(ex, "FATAL: Database migration failed for InventoryService! Application startup aborted.");
                throw;
            }
        }
        else
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.Drugs.AnyAsync())
        {
            logger.LogInformation("Inventory database already contains drug records. Skipping seed data.");
            return;
        }

        logger.LogInformation("Seeding initial inventory, suppliers, and drugs...");

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
            Description = "Macrolide antibiotic for respiratory tract infections",
            Category = "Antibiotics",
            Price = 24.50m,
            ExpiryDate = DateTime.UtcNow.AddMonths(8),
            Quantity = 10, // Below minimum 20 - low stock trigger
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        // Seed an expired drug for monitoring testing
        var drug6 = new Drug
        {
            DrugName = "Expired Aspirin 100mg",
            Description = "Aspirin batch past expiry date for QA testing",
            Category = "Analgesics",
            Price = 5.00m,
            ExpiryDate = DateTime.UtcNow.AddMonths(-3), // Expired 3 months ago
            Quantity = 50,
            MinimumStockQuantity = 15,
            IsAvailable = false
        };

        context.Drugs.AddRange(drug1, drug2, drug3, drug4, drug5, drug6);
        await context.SaveChangesAsync();

        // Seed initial Inventory stock inward batches
        var inventory1 = new Inventory
        {
            SupplierId = supplier1.SupplierId,
            DrugId = drug1.DrugId,
            PurchasePrice = 5.50m,
            QuantitySupplied = 200,
            SupplyDate = DateTime.UtcNow.AddDays(-30),
            BatchNumber = "BATCH-PARA-2026-01",
            Notes = "Initial wholesale delivery of Paracetamol 500mg"
        };

        var inventory2 = new Inventory
        {
            SupplierId = supplier2.SupplierId,
            DrugId = drug2.DrugId,
            PurchasePrice = 11.00m,
            QuantitySupplied = 150,
            SupplyDate = DateTime.UtcNow.AddDays(-20),
            BatchNumber = "BATCH-AMOX-2026-02",
            Notes = "Initial wholesale delivery of Amoxicillin 250mg"
        };

        var inventory3 = new Inventory
        {
            SupplierId = supplier1.SupplierId,
            DrugId = drug3.DrugId,
            PurchasePrice = 7.00m,
            QuantitySupplied = 300,
            SupplyDate = DateTime.UtcNow.AddDays(-15),
            BatchNumber = "BATCH-IBU-2026-03",
            Notes = "Initial wholesale delivery of Ibuprofen 400mg"
        };

        context.Inventory.AddRange(inventory1, inventory2, inventory3);
        await context.SaveChangesAsync();
        logger.LogInformation("Inventory records seeded successfully.");
    }
}
