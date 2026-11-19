using InventoryService.Models;
using Microsoft.EntityFrameworkCore;

namespace InventoryService.Data;

public class InventoryDbContext : DbContext
{
    public InventoryDbContext(DbContextOptions<InventoryDbContext> options) : base(options)
    {
    }

    public DbSet<Drug> Drugs => Set<Drug>();
    public DbSet<Supplier> Suppliers => Set<Supplier>();
    public DbSet<Inventory> Inventories => Set<Inventory>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Drug entity configuration
        modelBuilder.Entity<Drug>(entity =>
        {
            entity.HasKey(d => d.DrugId);
            entity.Property(d => d.DrugName).IsRequired().HasMaxLength(150);
            entity.Property(d => d.Price).HasPrecision(18, 2);
            entity.Property(d => d.MinimumStockQuantity).HasDefaultValue(20);
            entity.Property(d => d.IsAvailable).HasDefaultValue(true);
            entity.Ignore(d => d.Name);
            entity.Ignore(d => d.DrugPrice);
        });

        // Supplier entity configuration
        modelBuilder.Entity<Supplier>(entity =>
        {
            entity.HasKey(s => s.SupplierId);
            entity.Property(s => s.SupplierName).IsRequired().HasMaxLength(150);
            entity.Property(s => s.Email).IsRequired().HasMaxLength(150);
            entity.Property(s => s.PhoneNumber).IsRequired().HasMaxLength(20);
            entity.Property(s => s.Address).IsRequired().HasMaxLength(300);
        });

        // Inventory entity configuration and 1:M relationships
        modelBuilder.Entity<Inventory>(entity =>
        {
            entity.HasKey(i => i.InventoryId);
            entity.Property(i => i.PurchasePrice).HasPrecision(18, 2);
            entity.Ignore(i => i.QuantityAdded);
            entity.Ignore(i => i.StockReceivedDate);

            // Supplier to Inventory (1:M)
            entity.HasOne(i => i.Supplier)
                  .WithMany(s => s.Inventories)
                  .HasForeignKey(i => i.SupplierId)
                  .OnDelete(DeleteBehavior.Restrict);

            // Drug to Inventory (1:M)
            entity.HasOne(i => i.Drug)
                  .WithMany(d => d.Inventories)
                  .HasForeignKey(i => i.DrugId)
                  .OnDelete(DeleteBehavior.Restrict);
        });
    }
}
