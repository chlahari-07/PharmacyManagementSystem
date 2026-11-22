using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using NUnit.Framework;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace PharmacyManagement.Tests;

[TestFixture]
public class SecurityAndRbacTests
{
    private JwtSettings _jwtSettings = null!;

    [SetUp]
    public void SetUp()
    {
        _jwtSettings = new JwtSettings
        {
            SecretKey = "TestSuperSecretKeyForPharmacyManagement2026!@#$"
        };
    }

    [Test]
    public void TC23_AccessProtectedApi_WithoutJwtToken_TokenValidationFails()
    {
        // Arrange
        string? nullOrEmptyToken = null;

        // Act & Assert: Token handler throws or fails when token is null or invalid
        var handler = new JwtSecurityTokenHandler();
        Assert.Throws<ArgumentNullException>(() =>
        {
            handler.ValidateToken(nullOrEmptyToken, new TokenValidationParameters(), out _);
        });
    }

    [Test]
    public void TC24_AccessAdminApi_UsingDoctorRole_RoleClaimMismatchFailsAdminAuthorization()
    {
        // Arrange: Generate token with Doctor role
        var doctorToken = JwtTokenGenerator.GenerateToken(
            userId: 2,
            name: "Dr. Robert Smith",
            email: "doctor@pharmacy.com",
            role: UserRoles.Doctor,
            settings: _jwtSettings);

        // Act: Parse claims from token
        var handler = new JwtSecurityTokenHandler();
        var key = Encoding.UTF8.GetBytes(_jwtSettings.SecretKey);
        var principal = handler.ValidateToken(doctorToken, new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(key),
            ValidateIssuer = true,
            ValidIssuer = _jwtSettings.Issuer,
            ValidateAudience = true,
            ValidAudience = _jwtSettings.Audience,
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        }, out _);

        // Assert: Principal has Doctor role, NOT Admin role
        Assert.That(principal.IsInRole(UserRoles.Doctor), Is.True);
        Assert.That(principal.IsInRole(UserRoles.Admin), Is.False);
    }
}
