using Microsoft.EntityFrameworkCore;
using SaleReportService.Models;

namespace SaleReportService.Data;

public class SaleReportDbContext : DbContext
{
    public SaleReportDbContext(DbContextOptions<SaleReportDbContext> options) : base(options)
    {
    }

    public DbSet<SaleReport> SaleReports => Set<SaleReport>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<SaleReport>(entity =>
        {
            entity.HasKey(r => r.SaleReportId);
            entity.Property(r => r.ReportType).IsRequired().HasMaxLength(20);
            entity.Property(r => r.TotalRevenue).HasPrecision(18, 2);
            entity.Property(r => r.Profit).HasPrecision(18, 2);
            entity.Property(r => r.GeneratedDate).HasDefaultValueSql("GETUTCDATE()");
        });
    }
}
