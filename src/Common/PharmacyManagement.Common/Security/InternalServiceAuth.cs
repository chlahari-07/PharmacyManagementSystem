using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using PharmacyManagement.Common.Models;

namespace PharmacyManagement.Common.Security;

/// <summary>
/// Constants and configuration for internal service-to-service communication.
/// </summary>
public static class InternalServiceConstants
{
    public const string HeaderName = "X-Internal-Service-Key";
    public const string ConfigSection = "InternalService";
    public const string SecretKeyConfig = "InternalService:SecretKey";
}

/// <summary>
/// Action filter that restricts access to internal microservice callers providing
/// a valid X-Internal-Service-Key header or authenticated Admin JWT users.
/// Anonymous or unauthorized calls are rejected with HTTP 401/403.
/// </summary>
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public class InternalOrAdminAuthorizeAttribute : Attribute, IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var httpContext = context.HttpContext;
        var configuration = httpContext.RequestServices.GetRequiredService<IConfiguration>();
        var configuredKey = configuration[InternalServiceConstants.SecretKeyConfig];

        // 1. Check for valid internal service key in request headers
        if (httpContext.Request.Headers.TryGetValue(InternalServiceConstants.HeaderName, out var providedKey))
        {
            if (!string.IsNullOrWhiteSpace(configuredKey) &&
                string.Equals(providedKey.ToString(), configuredKey, StringComparison.Ordinal))
            {
                // Authorized as trusted internal microservice
                await next();
                return;
            }
        }

        // 2. Check if the caller is an authenticated Admin user via JWT
        if (httpContext.User.Identity?.IsAuthenticated == true &&
            httpContext.User.IsInRole(UserRoles.Admin))
        {
            await next();
            return;
        }

        // If neither condition is met, deny access
        context.Result = new ObjectResult(new ApiResponse<bool>
        {
            Success = false,
            Message = "Access denied: This operation requires valid internal service authorization or an Admin role."
        })
        {
            StatusCode = StatusCodes.Status403Forbidden
        };
    }
}
