using Microsoft.EntityFrameworkCore;
using SaleReportService.Data;
using SaleReportService.Models;

namespace SaleReportService.Repositories;

public interface ISaleReportRepository
{
    Task<IEnumerable<SaleReport>> GetAllAsync();
    Task<SaleReport?> GetByIdAsync(int reportId);
    Task<IEnumerable<SaleReport>> GetByTypeAsync(string reportType);
    Task<SaleReport> AddAsync(SaleReport report);
}

public class SaleReportRepository : ISaleReportRepository
{
    private readonly SaleReportDbContext _context;

    public SaleReportRepository(SaleReportDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<SaleReport>> GetAllAsync()
    {
        return await _context.SaleReports
            .AsNoTracking()
            .OrderByDescending(r => r.GeneratedDate)
            .ToListAsync();
    }

    public async Task<SaleReport?> GetByIdAsync(int reportId)
    {
        return await _context.SaleReports.FirstOrDefaultAsync(r => r.SaleReportId == reportId);
    }

    public async Task<IEnumerable<SaleReport>> GetByTypeAsync(string reportType)
    {
        return await _context.SaleReports
            .AsNoTracking()
            .Where(r => r.ReportType.ToLower() == reportType.Trim().ToLower())
            .OrderByDescending(r => r.GeneratedDate)
            .ToListAsync();
    }

    public async Task<SaleReport> AddAsync(SaleReport report)
    {
        await _context.SaleReports.AddAsync(report);
        await _context.SaveChangesAsync();
        return report;
    }
}
