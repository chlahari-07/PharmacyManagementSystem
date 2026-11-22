using Microsoft.EntityFrameworkCore;
using NUnit.Framework;
using AuthService.Data;
using AuthService.Models;
using InventoryService.Data;
using InventoryService.Models;
using OrderService.Data;
using OrderService.Models;
using PaymentService.Data;
using PaymentService.Models;
using PharmacyManagement.Common.Models;

namespace PharmacyManagement.Tests;

/// <summary>
/// SQL Server Integration Tests using dedicated test databases.
/// Runs actual EF Core migrations against SQL Server Express.
/// To enable: set environment variable PHARMACY_TEST_SQLSERVER
/// Example: $env:PHARMACY_TEST_SQLSERVER = "Server=.\SQLEXPRESS;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=True;Encrypt=True"
/// </summary>
[TestFixture]
[Category("Integration")]
public class SqlServerIntegrationTests
{
    private string? _connectionStringBase;

    [SetUp]
    public void CheckConfiguration()
    {
        _connectionStringBase = Environment.GetEnvironmentVariable("PHARMACY_TEST_SQLSERVER");
        if (string.IsNullOrWhiteSpace(_connectionStringBase))
        {
            Assert.Ignore("SQL Server integration tests skipped: 'PHARMACY_TEST_SQLSERVER' environment variable is not configured. " +
                          "To enable against local SQL Server Express, set: " +
                          "$env:PHARMACY_TEST_SQLSERVER = 'Server=.\\SQLEXPRESS;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=True;Encrypt=True'");
        }
    }

    private string BuildConnectionString(string databaseName)
    {
        var builder = new Microsoft.Data.SqlClient.SqlConnectionStringBuilder(_connectionStringBase)
        {
            InitialCatalog = databaseName
        };
        return builder.ConnectionString;
    }

    [Test]
    public async Task Integration_AuthDb_AppliesMigrations_AndEnforcesUniqueEmailConstraint()
    {
        var connectionString = BuildConnectionString("Pharmacy_UserDB_IntegrationTests");
        var options = new DbContextOptionsBuilder<AuthDbContext>()
            .UseSqlServer(connectionString)
            .Options;

        await using var context = new AuthDbContext(options);

        // 1. Verify that actual migrations can be applied to the integration test database
        await context.Database.MigrateAsync();

        // Clean test email if already present
        var existing = await context.Users.Where(u => u.Email == "duplicate.test@pharmacy.com").ToListAsync();
        if (existing.Any())
        {
            context.Users.RemoveRange(existing);
            await context.SaveChangesAsync();
        }

        // 2. Insert first user
        var user1 = new User
        {
            Name = "User One",
            Email = "duplicate.test@pharmacy.com",
            PhoneNumber = "+1234567890",
            PasswordHash = "hash1",
            Role = UserRoles.Doctor,
            CreatedDate = DateTime.UtcNow,
            IsActive = true
        };
        await context.Users.AddAsync(user1);
        await context.SaveChangesAsync();

        // 3. Insert second user with duplicate email -> should fail SQL Server unique index
        var user2 = new User
        {
            Name = "User Two",
            Email = "duplicate.test@pharmacy.com",
            PhoneNumber = "+1987654321",
            PasswordHash = "hash2",
            Role = UserRoles.Doctor,
            CreatedDate = DateTime.UtcNow,
            IsActive = true
        };
        await context.Users.AddAsync(user2);

        Assert.ThrowsAsync<DbUpdateException>(async () =>
        {
            await context.SaveChangesAsync();
        });
    }

    [Test]
    public async Task Integration_InventoryDb_AppliesMigrations_AndEnforcesForeignKeyConstraint()
    {
        var connectionString = BuildConnectionString("Pharmacy_InventoryDB_IntegrationTests");
        var options = new DbContextOptionsBuilder<InventoryDbContext>()
            .UseSqlServer(connectionString)
            .Options;

        await using var context = new InventoryDbContext(options);

        // Apply migrations
        await context.Database.MigrateAsync();

        // Attempt to insert Inventory batch referencing non-existent Supplier ID 999999
        var invalidInventory = new Inventory
        {
            SupplierId = 999999, // Non-existent foreign key
            DrugId = 1,
            PurchasePrice = 10.00m,
            QuantitySupplied = 100,
            SupplyDate = DateTime.UtcNow,
            BatchNumber = "TEST-FK-BATCH"
        };

        await context.Inventory.AddAsync(invalidInventory);

        // SQL Server must throw foreign key constraint violation
        Assert.ThrowsAsync<DbUpdateException>(async () =>
        {
            await context.SaveChangesAsync();
        });
    }

    [Test]
    public async Task Integration_PaymentDb_AppliesMigrations_AndEnforcesOneToOneUniqueOrderIdConstraint()
    {
        var connectionString = BuildConnectionString("Pharmacy_PaymentDB_IntegrationTests");
        var options = new DbContextOptionsBuilder<PaymentDbContext>()
            .UseSqlServer(connectionString)
            .Options;

        await using var context = new PaymentDbContext(options);

        // Apply migrations
        await context.Database.MigrateAsync();

        int testOrderId = 88888;
        var existing = await context.Payments.Where(p => p.OrderId == testOrderId).ToListAsync();
        if (existing.Any())
        {
            context.Payments.RemoveRange(existing);
            await context.SaveChangesAsync();
        }

        // Insert first payment for OrderId 88888
        var payment1 = new Payment
        {
            OrderId = testOrderId,
            Amount = 100.00m,
            PaymentDate = DateTime.UtcNow,
            PaymentMethod = "UPI",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "INT-TXN-001"
        };
        await context.Payments.AddAsync(payment1);
        await context.SaveChangesAsync();

        // Insert second payment for same OrderId 88888 -> should violate unique index on OrderId (1:1)
        var payment2 = new Payment
        {
            OrderId = testOrderId,
            Amount = 100.00m,
            PaymentDate = DateTime.UtcNow,
            PaymentMethod = "CreditCard",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "INT-TXN-002"
        };
        await context.Payments.AddAsync(payment2);

        Assert.ThrowsAsync<DbUpdateException>(async () =>
        {
            await context.SaveChangesAsync();
        });
    }

    [Test]
    public async Task Integration_OrderDb_TransactionRollback_DiscardsChangesOnFailure()
    {
        var connectionString = BuildConnectionString("Pharmacy_OrderDB_IntegrationTests");
        var options = new DbContextOptionsBuilder<OrderDbContext>()
            .UseSqlServer(connectionString)
            .Options;

        await using var context = new OrderDbContext(options);

        // Apply migrations
        await context.Database.MigrateAsync();

        int initialCount = await context.Orders.CountAsync();

        // Begin explicit SQL transaction and roll back
        await using (var transaction = await context.Database.BeginTransactionAsync())
        {
            var tempOrder = new Order
            {
                DoctorID = 100,
                TotalAmount = 999.00m,
                Status = OrderStatuses.Pending,
                OrderDate = DateTime.UtcNow
            };
            await context.Orders.AddAsync(tempOrder);
            await context.SaveChangesAsync();

            // Explicit rollback
            await transaction.RollbackAsync();
        }

        int finalCount = await context.Orders.CountAsync();
        Assert.That(finalCount, Is.EqualTo(initialCount), "Transaction rollback must discard all pending entities.");
    }
}
