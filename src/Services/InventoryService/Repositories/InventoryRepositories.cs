using InventoryService.Data;
using InventoryService.Models;
using Microsoft.EntityFrameworkCore;

namespace InventoryService.Repositories;

public interface IDrugRepository
{
    Task<IEnumerable<Drug>> GetAllAsync(bool availableOnly = false);
    Task<Drug?> GetByIdAsync(int drugId);
    Task<Drug> AddAsync(Drug drug);
    Task UpdateAsync(Drug drug);
    Task<bool> DeleteAsync(int drugId);
    Task<bool> ExistsAsync(int drugId);
}

public class DrugRepository : IDrugRepository
{
    private readonly InventoryDbContext _context;

    public DrugRepository(InventoryDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Drug>> GetAllAsync(bool availableOnly = false)
    {
        IQueryable<Drug> query = _context.Drugs.AsNoTracking();
        if (availableOnly)
        {
            query = query.Where(d => d.IsAvailable && d.Quantity > 0 && d.ExpiryDate > DateTime.UtcNow);
        }
        return await query.OrderBy(d => d.Name).ToListAsync();
    }

    public async Task<Drug?> GetByIdAsync(int drugId)
    {
        return await _context.Drugs.FirstOrDefaultAsync(d => d.DrugId == drugId);
    }

    public async Task<Drug> AddAsync(Drug drug)
    {
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();
        return drug;
    }

    public async Task UpdateAsync(Drug drug)
    {
        _context.Drugs.Update(drug);
        await _context.SaveChangesAsync();
    }

    public async Task<bool> DeleteAsync(int drugId)
    {
        var drug = await _context.Drugs.FindAsync(drugId);
        if (drug == null) return false;

        _context.Drugs.Remove(drug);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> ExistsAsync(int drugId)
    {
        return await _context.Drugs.AnyAsync(d => d.DrugId == drugId);
    }
}

public interface ISupplierRepository
{
    Task<IEnumerable<Supplier>> GetAllAsync();
    Task<Supplier?> GetByIdAsync(int supplierId);
    Task<Supplier> AddAsync(Supplier supplier);
    Task UpdateAsync(Supplier supplier);
    Task<bool> DeleteAsync(int supplierId);
    Task<bool> ExistsAsync(int supplierId);
}

public class SupplierRepository : ISupplierRepository
{
    private readonly InventoryDbContext _context;

    public SupplierRepository(InventoryDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Supplier>> GetAllAsync()
    {
        return await _context.Suppliers.AsNoTracking().OrderBy(s => s.SupplierName).ToListAsync();
    }

    public async Task<Supplier?> GetByIdAsync(int supplierId)
    {
        return await _context.Suppliers.FirstOrDefaultAsync(s => s.SupplierId == supplierId);
    }

    public async Task<Supplier> AddAsync(Supplier supplier)
    {
        await _context.Suppliers.AddAsync(supplier);
        await _context.SaveChangesAsync();
        return supplier;
    }

    public async Task UpdateAsync(Supplier supplier)
    {
        _context.Suppliers.Update(supplier);
        await _context.SaveChangesAsync();
    }

    public async Task<bool> DeleteAsync(int supplierId)
    {
        var supplier = await _context.Suppliers.FindAsync(supplierId);
        if (supplier == null) return false;

        _context.Suppliers.Remove(supplier);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> ExistsAsync(int supplierId)
    {
        return await _context.Suppliers.AnyAsync(s => s.SupplierId == supplierId);
    }
}

public interface IInventoryRepository
{
    Task<IEnumerable<Inventory>> GetAllWithDetailsAsync();
    Task<Inventory?> GetByIdAsync(int inventoryId);
    Task<Inventory> AddAsync(Inventory inventory);
}

public class InventoryRepository : IInventoryRepository
{
    private readonly InventoryDbContext _context;

    public InventoryRepository(InventoryDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Inventory>> GetAllWithDetailsAsync()
    {
        return await _context.Inventories
            .Include(i => i.Supplier)
            .Include(i => i.Drug)
            .AsNoTracking()
            .OrderByDescending(i => i.StockReceivedDate)
            .ToListAsync();
    }

    public async Task<Inventory?> GetByIdAsync(int inventoryId)
    {
        return await _context.Inventories
            .Include(i => i.Supplier)
            .Include(i => i.Drug)
            .FirstOrDefaultAsync(i => i.InventoryId == inventoryId);
    }

    public async Task<Inventory> AddAsync(Inventory inventory)
    {
        await _context.Inventories.AddAsync(inventory);
        await _context.SaveChangesAsync();
        return inventory;
    }
}
