using AuthService.Models;
using Microsoft.EntityFrameworkCore;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace AuthService.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(AuthDbContext context)
    {
        // Try migrations or ensure created for testing flexibility
        try
        {
            if (context.Database.IsRelational())
            {
                await context.Database.EnsureCreatedAsync();
            }
        }
        catch
        {
            await context.Database.EnsureCreatedAsync();
        }

        if (await context.Users.AnyAsync())
        {
            return; // DB has already been seeded
        }

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
    }
}
