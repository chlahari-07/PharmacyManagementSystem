using AuthService.DTOs;
using AuthService.Models;
using AuthService.Repositories;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace AuthService.Services;

public interface IAuthService
{
    Task<ApiResponse<AuthResponseDto>> RegisterAsync(RegisterDto dto);
    Task<ApiResponse<AuthResponseDto>> LoginAsync(LoginDto dto);
    Task<ApiResponse<UserDto>> GetUserByIdAsync(int userId);
    Task<ApiResponse<IEnumerable<UserDto>>> GetAllUsersAsync();
    Task<ApiResponse<bool>> ValidateUserRoleAsync(int userId, string expectedRole);
}

public class AuthService : IAuthService
{
    private readonly IUserRepository _userRepository;
    private readonly JwtSettings _jwtSettings;

    public AuthService(IUserRepository userRepository, JwtSettings jwtSettings)
    {
        _userRepository = userRepository;
        _jwtSettings = jwtSettings;
    }

    public async Task<ApiResponse<AuthResponseDto>> RegisterAsync(RegisterDto dto)
    {
        // Admin registration is prohibited - Admin accounts are pre-seeded
        if (string.Equals(dto.Role, UserRoles.Admin, StringComparison.OrdinalIgnoreCase))
        {
            return ApiResponse<AuthResponseDto>.FailureResult(
                "Admin registration is not allowed. Admin credentials are pre-seeded in the database.",
                new List<string> { "Only Doctor accounts can be registered. Administrators cannot register." });
        }

        if (await _userRepository.EmailExistsAsync(dto.Email))
        {
            return ApiResponse<AuthResponseDto>.FailureResult(
                "A user with this email address already exists.",
                new List<string> { "Email is already registered." });
        }

        var user = new User
        {
            Name = dto.Name.Trim(),
            Email = dto.Email.Trim().ToLower(),
            PhoneNumber = dto.PhoneNumber.Trim(),
            PasswordHash = PasswordHasher.HashPassword(dto.Password),
            Role = UserRoles.Doctor,
            IsActive = true,
            CreatedDate = DateTime.UtcNow
        };

        var createdUser = await _userRepository.AddAsync(user);

        var token = JwtTokenGenerator.GenerateToken(
            createdUser.UserId,
            createdUser.Name,
            createdUser.Email,
            createdUser.Role,
            _jwtSettings);

        var response = new AuthResponseDto
        {
            UserId = createdUser.UserId,
            Name = createdUser.Name,
            Email = createdUser.Email,
            Role = createdUser.Role,
            Token = token,
            ExpiryDate = DateTime.UtcNow.AddMinutes(_jwtSettings.ExpiryMinutes)
        };

        return ApiResponse<AuthResponseDto>.SuccessResult(response, "User registered successfully.");
    }

    public async Task<ApiResponse<AuthResponseDto>> LoginAsync(LoginDto dto)
    {
        var user = await _userRepository.GetByEmailAsync(dto.Email);
        if (user == null || !PasswordHasher.VerifyPassword(dto.Password, user.PasswordHash))
        {
            return ApiResponse<AuthResponseDto>.FailureResult(
                "Invalid email or password.",
                new List<string> { "Authentication failed." });
        }

        if (!user.IsActive)
        {
            return ApiResponse<AuthResponseDto>.FailureResult(
                "Account is deactivated. Please contact support.",
                new List<string> { "User account inactive." });
        }

        var token = JwtTokenGenerator.GenerateToken(
            user.UserId,
            user.Name,
            user.Email,
            user.Role,
            _jwtSettings);

        var response = new AuthResponseDto
        {
            UserId = user.UserId,
            Name = user.Name,
            Email = user.Email,
            Role = user.Role,
            Token = token,
            ExpiryDate = DateTime.UtcNow.AddMinutes(_jwtSettings.ExpiryMinutes)
        };

        return ApiResponse<AuthResponseDto>.SuccessResult(response, "Login successful.");
    }

    public async Task<ApiResponse<UserDto>> GetUserByIdAsync(int userId)
    {
        var user = await _userRepository.GetByIdAsync(userId);
        if (user == null)
        {
            return ApiResponse<UserDto>.FailureResult("User not found.");
        }

        var dto = new UserDto
        {
            UserId = user.UserId,
            Name = user.Name,
            Email = user.Email,
            PhoneNumber = user.PhoneNumber,
            Role = user.Role,
            IsActive = user.IsActive,
            CreatedDate = user.CreatedDate
        };

        return ApiResponse<UserDto>.SuccessResult(dto);
    }

    public async Task<ApiResponse<IEnumerable<UserDto>>> GetAllUsersAsync()
    {
        var users = await _userRepository.GetAllUsersAsync();
        var dtos = users.Select(u => new UserDto
        {
            UserId = u.UserId,
            Name = u.Name,
            Email = u.Email,
            PhoneNumber = u.PhoneNumber,
            Role = u.Role,
            IsActive = u.IsActive,
            CreatedDate = u.CreatedDate
        });

        return ApiResponse<IEnumerable<UserDto>>.SuccessResult(dtos, "Users retrieved successfully.");
    }

    public async Task<ApiResponse<bool>> ValidateUserRoleAsync(int userId, string expectedRole)
    {
        var user = await _userRepository.GetByIdAsync(userId);
        if (user == null || !user.IsActive)
        {
            return ApiResponse<bool>.FailureResult("User not found or inactive.");
        }

        bool isValid = user.Role.Equals(expectedRole, StringComparison.OrdinalIgnoreCase);
        return ApiResponse<bool>.SuccessResult(isValid, isValid ? "User role verified." : "Role mismatch.");
    }
}

public class AuthServiceClass : AuthService
{
    public AuthServiceClass(IUserRepository userRepository, JwtSettings jwtSettings) : base(userRepository, jwtSettings) { }
}
