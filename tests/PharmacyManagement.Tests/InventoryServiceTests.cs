using InventoryService.Data;
using InventoryService.DTOs;
using InventoryService.Models;
using InventoryService.Repositories;
using InventoryService.Services;
using Microsoft.EntityFrameworkCore;
using NUnit.Framework;

namespace PharmacyManagement.Tests;

[TestFixture]
public class InventoryServiceTests
{
    private InventoryDbContext _context = null!;
    private IDrugRepository _drugRepository = null!;
    private ISupplierRepository _supplierRepository = null!;
    private IInventoryRepository _inventoryRepository = null!;
    private IDrugService _drugService = null!;
    private IInventoryService _inventoryService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<InventoryDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new InventoryDbContext(options);
        _drugRepository = new DrugRepository(_context);
        _supplierRepository = new SupplierRepository(_context);
        _inventoryRepository = new InventoryRepository(_context);

        _drugService = new DrugService(_drugRepository);
        _inventoryService = new InventoryServiceClass(_inventoryRepository, _drugRepository, _supplierRepository);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC05_CreateDrug_WithValidAttributes_ReturnsSuccess()
    {
        // Arrange
        var createDto = new CreateDrugDto
        {
            DrugName = "Amoxicillin 500mg",
            Description = "Broad spectrum antibiotic",
            Category = "Antibiotics",
            Price = 14.50m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 100,
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        // Act
        var result = await _drugService.CreateDrugAsync(createDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.DrugName, Is.EqualTo("Amoxicillin 500mg"));
        Assert.That(result.Data.MinimumStockQuantity, Is.EqualTo(20));
        Assert.That(result.Data.Quantity, Is.EqualTo(100));
        Assert.That(result.Data.IsLowStock, Is.False);
    }

    [Test]
    public async Task TC07_LowStockMonitoring_ReturnsOnlyDrugsAtOrBelowThreshold()
    {
        // Arrange
        var normalDrug = new Drug
        {
            DrugName = "Paracetamol 500mg",
            Price = 8.50m,
            ExpiryDate = DateTime.UtcNow.AddYears(2),
            Quantity = 100,
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        var lowStockDrug = new Drug
        {
            DrugName = "Azithromycin 500mg",
            Price = 25.00m,
            ExpiryDate = DateTime.UtcNow.AddMonths(6),
            Quantity = 10, // 10 <= 20 (Low stock)
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        await _context.Drugs.AddRangeAsync(normalDrug, lowStockDrug);
        await _context.SaveChangesAsync();

        // Act
        var result = await _drugService.GetLowStockDrugsAsync();

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        var list = result.Data!.ToList();
        Assert.That(list.Count, Is.EqualTo(1));
        Assert.That(list[0].DrugName, Is.EqualTo("Azithromycin 500mg"));
        Assert.That(list[0].IsLowStock, Is.True);
    }

    [Test]
    public async Task TC08_ExpiredDrugReport_ReturnsOnlyExpiredMedicines()
    {
        // Arrange
        var freshDrug = new Drug
        {
            DrugName = "Ibuprofen 400mg",
            Price = 12.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 50,
            MinimumStockQuantity = 15,
            IsAvailable = true
        };

        var expiredDrug = new Drug
        {
            DrugName = "Cough Syrup Dx",
            Price = 7.50m,
            ExpiryDate = DateTime.UtcNow.AddDays(-10), // Expired
            Quantity = 25,
            MinimumStockQuantity = 10,
            IsAvailable = false
        };

        await _context.Drugs.AddRangeAsync(freshDrug, expiredDrug);
        await _context.SaveChangesAsync();

        // Act
        var result = await _drugService.GetExpiredDrugsAsync();

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        var list = result.Data!.ToList();
        Assert.That(list.Count, Is.EqualTo(1));
        Assert.That(list[0].DrugName, Is.EqualTo("Cough Syrup Dx"));
        Assert.That(list[0].IsExpired, Is.True);
    }

    [Test]
    public async Task TC09_DeductStock_WhenSufficientQuantity_ReducesInventoryQuantity()
    {
        // Arrange
        var drug = new Drug
        {
            DrugName = "Metformin 500mg",
            Price = 15.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 50,
            MinimumStockQuantity = 10,
            IsAvailable = true
        };
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();

        var deductRequest = new DeductStockRequestDto
        {
            Items = new List<DeductStockItemDto>
            {
                new() { DrugId = drug.DrugId, Quantity = 15 }
            }
        };

        // Act
        var result = await _drugService.DeductStockAsync(deductRequest);

        // Assert
        Assert.That(result.Success, Is.True);
        var updatedDrug = await _context.Drugs.FindAsync(drug.DrugId);
        Assert.That(updatedDrug!.Quantity, Is.EqualTo(35));
    }

    [Test]
    public async Task TC10_DeductStock_WhenInsufficientQuantity_RejectsDeduction()
    {
        // Arrange
        var drug = new Drug
        {
            DrugName = "Rare Antibiotic",
            Price = 45.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 5,
            MinimumStockQuantity = 10,
            IsAvailable = true
        };
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();

        var deductRequest = new DeductStockRequestDto
        {
            Items = new List<DeductStockItemDto>
            {
                new() { DrugId = drug.DrugId, Quantity = 10 } // Requesting 10, only 5 in stock
            }
        };

        // Act
        var result = await _drugService.DeductStockAsync(deductRequest);

        // Assert
        Assert.That(result.Success, Is.False);
        var currentDrug = await _context.Drugs.FindAsync(drug.DrugId);
        Assert.That(currentDrug!.Quantity, Is.EqualTo(5)); // Remains untouched
    }
}
