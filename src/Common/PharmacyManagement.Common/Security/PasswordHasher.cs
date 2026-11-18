using System.Security.Cryptography;

namespace PharmacyManagement.Common.Security;

public static class PasswordHasher
{
    private const int SaltSize = 16; // 128-bit
    private const int HashSize = 32; // 256-bit
    private const int Iterations = 100000;

    public static string HashPassword(string password)
    {
        byte[] salt = RandomNumberGenerator.GetBytes(SaltSize);
        byte[] hash = Rfc2898DeriveBytes.Pbkdf2(
            password,
            salt,
            Iterations,
            HashAlgorithmName.SHA256,
            HashSize);

        byte[] hashBytes = new byte[SaltSize + HashSize];
        Array.Copy(salt, 0, hashBytes, 0, SaltSize);
        Array.Copy(hash, 0, hashBytes, SaltSize, HashSize);

        return Convert.ToBase64String(hashBytes);
    }

    public static bool VerifyPassword(string password, string passwordHash)
    {
        try
        {
            byte[] hashBytes = Convert.FromBase64String(passwordHash);
            if (hashBytes.Length != SaltSize + HashSize)
            {
                return false;
            }

            byte[] salt = new byte[SaltSize];
            Array.Copy(hashBytes, 0, salt, 0, SaltSize);

            byte[] expectedHash = new byte[HashSize];
            Array.Copy(hashBytes, SaltSize, expectedHash, 0, HashSize);

            byte[] actualHash = Rfc2898DeriveBytes.Pbkdf2(
                password,
                salt,
                Iterations,
                HashAlgorithmName.SHA256,
                HashSize);

            return CryptographicOperations.FixedTimeEquals(actualHash, expectedHash);
        }
        catch
        {
            return false;
        }
    }
}
