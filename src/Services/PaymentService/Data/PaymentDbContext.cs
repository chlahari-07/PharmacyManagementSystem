using Microsoft.EntityFrameworkCore;
using PaymentService.Models;

namespace PaymentService.Data;

public class PaymentDbContext : DbContext
{
    public PaymentDbContext(DbContextOptions<PaymentDbContext> options) : base(options)
    {
    }

    public DbSet<Payment> Payments => Set<Payment>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Payment>(entity =>
        {
            entity.HasKey(p => p.PaymentId);
            // 1:1 relationship constraint: Order to Payment has 1:1
            entity.HasIndex(p => p.OrderId).IsUnique();
            entity.Property(p => p.Amount).HasPrecision(18, 2);
            entity.Property(p => p.PaymentMethod).IsRequired().HasMaxLength(50);
            entity.Property(p => p.PaymentStatus).IsRequired().HasMaxLength(20);
            entity.Property(p => p.PaymentDate).HasDefaultValueSql("GETUTCDATE()");
        });
    }
}
