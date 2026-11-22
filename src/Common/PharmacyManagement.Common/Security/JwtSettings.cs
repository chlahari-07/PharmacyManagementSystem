namespace PharmacyManagement.Common.Security;

/// <summary>
/// Configuration settings for JWT Bearer Authentication.
/// In production and local development, SecretKey must be set via User Secrets or Environment Variables.
/// </summary>
public class JwtSettings
{
    public const string SectionName = "JwtSettings";

    /// <summary>
    /// Secret symmetric key for signing tokens. Must be at least 32 characters (256 bits).
    /// Configure via: dotnet user-secrets set "JwtSettings:SecretKey" "<your-secure-key>"
    /// </summary>
    public string SecretKey { get; set; } = string.Empty;

    public string Issuer { get; set; } = "PharmacyManagementAuthService";
    public string Audience { get; set; } = "PharmacyManagementMicroservices";
    public int ExpiryMinutes { get; set; } = 1440; // 24 hours
}
