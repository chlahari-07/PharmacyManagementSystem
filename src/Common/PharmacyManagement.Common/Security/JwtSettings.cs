namespace PharmacyManagement.Common.Security;

public class JwtSettings
{
    public const string SectionName = "JwtSettings";
    public string SecretKey { get; set; } = "PharmacyManagementSuperSecretKey2026!@#$%^&*()_+";
    public string Issuer { get; set; } = "PharmacyManagementAuthService";
    public string Audience { get; set; } = "PharmacyManagementMicroservices";
    public int ExpiryMinutes { get; set; } = 1440; // 24 hours
}
