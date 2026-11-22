using AuthService.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace AuthService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(
        AuthDbContext context,
        ILogger logger,
        IHostEnvironment environment)
    {
        // 1. Relational database migration: execute EF Core migrations
        if (context.Database.IsRelational())
        {
            try
            {
                logger.LogInformation("Applying EF Core migrations to SQL Server for AuthService (Pharmacy_UserDB)...");
                await context.Database.MigrateAsync();
                logger.LogInformation("EF Core migrations applied successfully for AuthService.");
            }
            catch (Exception ex)
            {
                logger.LogCritical(ex, "FATAL: Database migration failed for AuthService! Application startup aborted.");
                // Strictly re-throw to stop application startup. Never fall back to EnsureCreatedAsync on SQL Server.
                throw;
            }
        }
        else
        {
            // InMemory testing database only
            await context.Database.EnsureCreatedAsync();
        }

        // 2. Prevent duplicate seeding
        if (await context.Users.AnyAsync())
        {
            logger.LogInformation("AuthService database already contains user records. Skipping seed data.");
            return;
        }

        // 3. Pre-seed default development credentials (Admin and Doctor)
        logger.LogInformation("Seeding initial Admin and Doctor credentials...");

        var admin = new User
        {
            Name = "System Administrator",
            Email = "admin@pharmacy.com",
            PhoneNumber = "+1234567890",
            PasswordHash = PasswordHasher.HashPassword("Admin@123"),
            Role = UserRoles.Admin,
            IsActive = true,
            CreatedDate = DateTime.UtcNow
        };

        var doctor = new User
        {
            Name = "Dr. Robert Smith",
            Email = "doctor@pharmacy.com",
            PhoneNumber = "+1987654321",
            PasswordHash = PasswordHasher.HashPassword("Doctor@123"),
            Role = UserRoles.Doctor,
            IsActive = true,
            CreatedDate = DateTime.UtcNow
        };

        context.Users.AddRange(admin, doctor);
        await context.SaveChangesAsync();
        logger.LogInformation("Initial users seeded successfully.");
    }
}
