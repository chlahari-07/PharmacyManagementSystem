using Microsoft.EntityFrameworkCore;
using OrderService.Models;

namespace OrderService.Data;

public class OrderDbContext : DbContext
{
    public OrderDbContext(DbContextOptions<OrderDbContext> options) : base(options)
    {
    }

    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Order configuration
        modelBuilder.Entity<Order>(entity =>
        {
            entity.HasKey(o => o.OrderId);
            entity.Property(o => o.DoctorID).IsRequired();
            entity.Property(o => o.TotalAmount).HasPrecision(18, 2);
            entity.Property(o => o.Status).IsRequired().HasMaxLength(20);
            entity.Property(o => o.OrderDate).HasDefaultValueSql("GETUTCDATE()");

            // Order to OrderItem has (1:M)
            entity.HasMany(o => o.OrderItems)
                  .WithOne(oi => oi.Order)
                  .HasForeignKey(oi => oi.OrderId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

        // OrderItem configuration
        modelBuilder.Entity<OrderItem>(entity =>
        {
            entity.HasKey(oi => oi.OrderItemId);
            entity.Property(oi => oi.UnitPrice).HasPrecision(18, 2);
            entity.Property(oi => oi.Quantity).IsRequired();
            entity.Property(oi => oi.DrugId).IsRequired();
        });
    }
}
