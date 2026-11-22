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
    public async Task TC05_AddMedicine_WithValidDetails_ReturnsSuccess()
    {
        // Arrange
        var createDto = new CreateDrugDto
        {
            DrugName = "Paracetamol",
            Description = "Analgesic and antipyretic",
            Category = "Pain Relief",
            Price = 10.00m,
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
        Assert.That(result.Data!.DrugName, Is.EqualTo("Paracetamol"));
        Assert.That(result.Data.Price, Is.EqualTo(10.00m));
        Assert.That(result.Data.Quantity, Is.EqualTo(100));
    }

    [Test]
    public async Task TC06_AddMedicine_WithNegativePrice_ReturnsFailure()
    {
        // Arrange
        var createDto = new CreateDrugDto
        {
            DrugName = "Invalid Drug",
            Description = "Negative price test",
            Category = "Test",
            Price = -10.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 50,
            MinimumStockQuantity = 10,
            IsAvailable = true
        };

        // Act
        var result = await _drugService.CreateDrugAsync(createDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("greater than zero"));
    }

    [Test]
    public async Task TC07_UpdateMedicine_PriceAndStock_UpdatesSuccessfully()
    {
        // Arrange
        var drug = new Drug
        {
            DrugName = "Paracetamol",
            Price = 10.00m,
            Quantity = 100,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            MinimumStockQuantity = 20,
            IsAvailable = true,
            CreatedDate = DateTime.UtcNow
        };
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();

        var updateDto = new UpdateDrugDto
        {
            DrugName = "Paracetamol",
            Price = 15.00m,
            Quantity = 120,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            MinimumStockQuantity = 20,
            IsAvailable = true
        };

        // Act
        var result = await _drugService.UpdateDrugAsync(drug.DrugId, updateDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.Price, Is.EqualTo(15.00m));
        Assert.That(result.Data.Quantity, Is.EqualTo(120));
    }

    [Test]
    public async Task TC08_QueryMedicines_BelowMinimumStock_ReturnsLowStockItems()
    {
        // Arrange
        var normalDrug = new Drug
        {
            DrugName = "Amoxicillin 500mg",
            Price = 8.50m,
            ExpiryDate = DateTime.UtcNow.AddYears(2),
            Quantity = 100,
            MinimumStockQuantity = 20,
            IsAvailable = true,
            CreatedDate = DateTime.UtcNow
        };

        var lowStockDrug = new Drug
        {
            DrugName = "Azithromycin 500mg",
            Price = 25.00m,
            ExpiryDate = DateTime.UtcNow.AddMonths(6),
            Quantity = 5, // 5 <= 10 (Low stock)
            MinimumStockQuantity = 10,
            IsAvailable = true,
            CreatedDate = DateTime.UtcNow
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
    public async Task TC09_DeductStock_WhenSufficientQuantityExists_ReducesInventoryQuantity()
    {
        // Arrange
        var drug = new Drug
        {
            DrugName = "Paracetamol 500mg",
            Price = 10.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 100,
            MinimumStockQuantity = 10,
            IsAvailable = true,
            CreatedDate = DateTime.UtcNow
        };
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();

        var deductRequest = new DeductStockRequestDto
        {
            Items = new List<DeductStockItemDto>
            {
                new() { DrugId = drug.DrugId, Quantity = 20 }
            }
        };

        // Act
        var result = await _drugService.DeductStockAsync(deductRequest);

        // Assert
        Assert.That(result.Success, Is.True);
        var updatedDrug = await _context.Drugs.FindAsync(drug.DrugId);
        Assert.That(updatedDrug!.Quantity, Is.EqualTo(80));
    }

    [Test]
    public async Task TC10_DeductStock_WhenInsufficientQuantityExists_RejectsDeduction()
    {
        // Arrange
        var drug = new Drug
        {
            DrugName = "Special Medicine",
            Price = 45.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 10,
            MinimumStockQuantity = 10,
            IsAvailable = true,
            CreatedDate = DateTime.UtcNow
        };
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();

        var deductRequest = new DeductStockRequestDto
        {
            Items = new List<DeductStockItemDto>
            {
                new() { DrugId = drug.DrugId, Quantity = 20 } // Requesting 20, only 10 in stock
            }
        };

        // Act
        var result = await _drugService.DeductStockAsync(deductRequest);

        // Assert
        Assert.That(result.Success, Is.False);
        var currentDrug = await _context.Drugs.FindAsync(drug.DrugId);
        Assert.That(currentDrug!.Quantity, Is.EqualTo(10)); // Remains untouched
    }

    [Test]
    public async Task TC25_AddInventoryInward_IncreasesDrugQuantity()
    {
        // Arrange
        var supplier = new Supplier
        {
            SupplierName = "Apex Pharma",
            Email = "contact@apex.com",
            PhoneNumber = "+123456789",
            Address = "100 Medical Blvd"
        };
        await _context.Suppliers.AddAsync(supplier);

        var drug = new Drug
        {
            DrugName = "Paracetamol 500mg",
            Price = 10.00m,
            ExpiryDate = DateTime.UtcNow.AddYears(1),
            Quantity = 50,
            MinimumStockQuantity = 10,
            IsAvailable = true,
            CreatedDate = DateTime.UtcNow
        };
        await _context.Drugs.AddAsync(drug);
        await _context.SaveChangesAsync();

        var inwardDto = new InwardStockDto
        {
            SupplierId = supplier.SupplierId,
            DrugId = drug.DrugId,
            QuantitySupplied = 50,
            PurchasePrice = 6.50m
        };

        // Act
        var result = await _inventoryService.InwardStockAsync(inwardDto);

        // Assert
        Assert.That(result.Success, Is.True);
        var updatedDrug = await _context.Drugs.FindAsync(drug.DrugId);
        Assert.That(updatedDrug!.Quantity, Is.EqualTo(100)); // 50 + 50
    }

    [Test]
    public async Task TC38_DeductStock_WithNegativeOrZeroQuantity_ReturnsFailure()
    {
        // Arrange
        var deductRequest = new DeductStockRequestDto
        {
            Items = new List<DeductStockItemDto>
            {
                new() { DrugId = 1, Quantity = -5 } // Invalid negative quantity
            }
        };

        // Act
        var result = await _drugService.DeductStockAsync(deductRequest);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("greater than zero"));
    }

    [Test]
    public async Task TC39_DeductStock_WithNonExistentDrugId_ReturnsFailure()
    {
        // Arrange
        var deductRequest = new DeductStockRequestDto
        {
            Items = new List<DeductStockItemDto>
            {
                new() { DrugId = 99999, Quantity = 2 }
            }
        };

        // Act
        var result = await _drugService.DeductStockAsync(deductRequest);

        // Assert
        Assert.That(result.Success, Is.False);
    }
}
