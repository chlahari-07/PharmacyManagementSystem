using System.ComponentModel.DataAnnotations;
using AuthService.Data;
using AuthService.DTOs;
using AuthService.Models;
using AuthService.Repositories;
using AuthService.Services;
using Microsoft.EntityFrameworkCore;
using NUnit.Framework;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace PharmacyManagement.Tests;

[TestFixture]
public class AuthServiceTests
{
    private AuthDbContext _context = null!;
    private IUserRepository _userRepository = null!;
    private JwtSettings _jwtSettings = null!;
    private IAuthService _authService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<AuthDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new AuthDbContext(options);
        _userRepository = new UserRepository(_context);
        _jwtSettings = new JwtSettings();

        _authService = new AuthServiceClass(_userRepository, _jwtSettings);
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
            Name = "Doctor1",
            Email = "doctor@test.com",
            PhoneNumber = "+1234567890",
            Password = "Test@123",
            Role = UserRoles.Doctor
        };

        // Act
        var result = await _authService.RegisterAsync(registerDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Email, Is.EqualTo("doctor@test.com"));
        Assert.That(result.Data.Role, Is.EqualTo(UserRoles.Doctor));
        Assert.That(result.Data.Token, Is.Not.Null.And.Not.Empty);
    }

    [Test]
    public async Task TC02_Register_DuplicateEmail_ReturnsFailure()
    {
        // Arrange
        var existingUser = new User
        {
            Name = "Doctor1",
            Email = "doctor@test.com",
            PhoneNumber = "+1234567890",
            PasswordHash = PasswordHasher.HashPassword("Test@123"),
            Role = UserRoles.Doctor,
            IsActive = true
        };
        await _context.Users.AddAsync(existingUser);
        await _context.SaveChangesAsync();

        var duplicateDto = new RegisterDto
        {
            Name = "Doctor Impostor",
            Email = "doctor@test.com",
            PhoneNumber = "+9998887777",
            Password = "Test@123",
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
        var password = "Test@123";
        var user = new User
        {
            Name = "Doctor1",
            Email = "doctor@test.com",
            PhoneNumber = "+1234567890",
            PasswordHash = PasswordHasher.HashPassword(password),
            Role = UserRoles.Doctor,
            IsActive = true
        };
        await _context.Users.AddAsync(user);
        await _context.SaveChangesAsync();

        var loginDto = new LoginDto
        {
            Email = "doctor@test.com",
            Password = password
        };

        // Act
        var result = await _authService.LoginAsync(loginDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Role, Is.EqualTo(UserRoles.Doctor));
        Assert.That(result.Data.Token, Is.Not.Empty);
    }

    [Test]
    public async Task TC04_Login_InvalidPassword_ReturnsUnauthorizedFailure()
    {
        // Arrange
        var user = new User
        {
            Name = "Doctor1",
            Email = "doctor@test.com",
            PhoneNumber = "+1234567890",
            PasswordHash = PasswordHasher.HashPassword("Test@123"),
            Role = UserRoles.Doctor,
            IsActive = true
        };
        await _context.Users.AddAsync(user);
        await _context.SaveChangesAsync();

        var loginDto = new LoginDto
        {
            Email = "doctor@test.com",
            Password = "Wrong123"
        };

        // Act
        var result = await _authService.LoginAsync(loginDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("Invalid email or password"));
    }

    [Test]
    public async Task TC_AdminCannotRegister_AdminRegistrationRejected_AdminCanOnlyLogin()
    {
        // Arrange
        var adminRegisterDto = new RegisterDto
        {
            Name = "New Admin",
            Email = "newadmin@pharmacy.com",
            PhoneNumber = "+1122334455",
            Password = "AdminPassword@123",
            Role = UserRoles.Admin
        };

        // Act
        var result = await _authService.RegisterAsync(adminRegisterDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("Admin registration is not allowed"));
        Assert.That(result.Errors, Does.Contain("Only Doctor accounts can be registered. Administrators cannot register."));
    }

    [Test]
    public void TC21_Register_InvalidEmailFormat_FailsDataAnnotationValidation()
    {
        // Arrange
        var dto = new RegisterDto
        {
            Name = "Doctor1",
            Email = "doctortest.com", // Invalid email format
            PhoneNumber = "+1234567890",
            Password = "Test@123",
            Role = UserRoles.Doctor
        };

        var validationResults = new List<ValidationResult>();
        var context = new ValidationContext(dto);

        // Act
        bool isValid = Validator.TryValidateObject(dto, context, validationResults, true);

        // Assert
        Assert.That(isValid, Is.False);
        Assert.That(validationResults.Any(r => r.ErrorMessage!.Contains("email", StringComparison.OrdinalIgnoreCase)), Is.True);
    }

    [Test]
    public void TC22_Register_MissingRequiredFields_FailsValidation()
    {
        // Arrange: Missing Name
        var dto = new RegisterDto
        {
            Name = "", // Empty name
            Email = "doctor@test.com",
            PhoneNumber = "+1234567890",
            Password = "Test@123",
            Role = UserRoles.Doctor
        };

        var validationResults = new List<ValidationResult>();
        var context = new ValidationContext(dto);

        // Act
        bool isValid = Validator.TryValidateObject(dto, context, validationResults, true);

        // Assert
        Assert.That(isValid, Is.False);
        Assert.That(validationResults.Any(r => r.ErrorMessage!.Contains("Name is required")), Is.True);
    }
}
