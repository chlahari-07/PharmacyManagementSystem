using AuthService.Data;
using AuthService.DTOs;
using AuthService.Models;
using AuthService.Repositories;
using AuthService.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using NUnit.Framework;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace PharmacyManagement.Tests;

[TestFixture]
public class AuthServiceTests
{
    private AuthDbContext _context = null!;
    private IUserRepository _userRepository = null!;
    private IJwtTokenGenerator _tokenGenerator = null!;
    private IAuthService _authService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<AuthDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new AuthDbContext(options);
        _userRepository = new UserRepository(_context);

        var configValues = new Dictionary<string, string?>
        {
            {"Jwt:Key", "SuperSecretKeyForPharmacyManagementSystem2026SecureJwtToken!"},
            {"Jwt:Issuer", "PharmacyAuthService"},
            {"Jwt:Audience", "PharmacyManagementApp"},
            {"Jwt:ExpiryHours", "8"}
        };
        var configuration = new ConfigurationBuilder().AddInMemoryCollection(configValues).Build();
        _tokenGenerator = new JwtTokenGenerator(configuration);

        _authService = new AuthServiceClass(_userRepository, _tokenGenerator);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC01_Register_ValidDoctor_ReturnsSuccessWithJwtToken()
    {
        // Arrange
        var registerDto = new RegisterDto
        {
            Name = "Dr. John Watson",
            Email = "john.watson@pharmacy.com",
            PhoneNumber = "+1234567890",
            Password = "SecurePassword123!",
            Role = UserRoles.Doctor
        };

        // Act
        var result = await _authService.RegisterAsync(registerDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Email, Is.EqualTo("john.watson@pharmacy.com"));
        Assert.That(result.Data.Role, Is.EqualTo(UserRoles.Doctor));
        Assert.That(result.Data.Token, Is.Not.Null.And.Not.Empty);
    }

    [Test]
    public async Task TC02_Register_DuplicateEmail_ReturnsFailure()
    {
        // Arrange
        var existingUser = new User
        {
            Name = "Dr. Existing",
            Email = "duplicate@pharmacy.com",
            PhoneNumber = "+1112223333",
            PasswordHash = PasswordHasher.HashPassword("Password123!"),
            Role = UserRoles.Doctor
        };
        await _context.Users.AddAsync(existingUser);
        await _context.SaveChangesAsync();

        var duplicateDto = new RegisterDto
        {
            Name = "Dr. Impostor",
            Email = "duplicate@pharmacy.com",
            PhoneNumber = "+9998887777",
            Password = "NewPassword123!",
            Role = UserRoles.Doctor
        };

        // Act
        var result = await _authService.RegisterAsync(duplicateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("already exists"));
    }

    [Test]
    public async Task TC03_Login_ValidCredentials_ReturnsSuccessAndJwtToken()
    {
        // Arrange
        var password = "AdminPassword2026!";
        var adminUser = new User
        {
            Name = "Admin User",
            Email = "admin@pharmacy.com",
            PhoneNumber = "+1999888777",
            PasswordHash = PasswordHasher.HashPassword(password),
            Role = UserRoles.Admin
        };
        await _context.Users.AddAsync(adminUser);
        await _context.SaveChangesAsync();

        var loginDto = new LoginDto
        {
            Email = "admin@pharmacy.com",
            Password = password
        };

        // Act
        var result = await _authService.LoginAsync(loginDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Role, Is.EqualTo(UserRoles.Admin));
        Assert.That(result.Data.Token, Is.Not.Empty);
    }

    [Test]
    public async Task TC04_Login_InvalidPassword_ReturnsUnauthorizedFailure()
    {
        // Arrange
        var user = new User
        {
            Name = "Dr. Valid",
            Email = "doctor@pharmacy.com",
            PhoneNumber = "+1234567890",
            PasswordHash = PasswordHasher.HashPassword("CorrectPassword123!"),
            Role = UserRoles.Doctor
        };
        await _context.Users.AddAsync(user);
        await _context.SaveChangesAsync();

        var loginDto = new LoginDto
        {
            Email = "doctor@pharmacy.com",
            Password = "WrongPassword999!"
        };

        // Act
        var result = await _authService.LoginAsync(loginDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("Invalid email or password"));
    }
}
