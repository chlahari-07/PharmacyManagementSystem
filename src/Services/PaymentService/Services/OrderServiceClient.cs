using System.Net.Http.Json;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using PaymentService.DTOs;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace PaymentService.Services;

public interface IOrderServiceClient
{
    Task<OrderValidationResultDto?> GetOrderForValidationAsync(int orderId, CancellationToken cancellationToken = default);
    Task<bool> UpdateOrderStatusToVerifiedAsync(int orderId, CancellationToken cancellationToken = default);
}

public class OrderServiceClient : IOrderServiceClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<OrderServiceClient> _logger;
    private readonly string _internalKey;

    public OrderServiceClient(
        HttpClient httpClient,
        IConfiguration configuration,
        ILogger<OrderServiceClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
        _internalKey = configuration[InternalServiceConstants.SecretKeyConfig] ?? string.Empty;

        if (!string.IsNullOrEmpty(_internalKey) && !_httpClient.DefaultRequestHeaders.Contains(InternalServiceConstants.HeaderName))
        {
            _httpClient.DefaultRequestHeaders.Add(InternalServiceConstants.HeaderName, _internalKey);
        }
    }

    public async Task<OrderValidationResultDto?> GetOrderForValidationAsync(int orderId, CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.GetAsync($"/api/orders/{orderId}", cancellationToken);
            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning("OrderService returned unsuccessful status code {StatusCode} for order {OrderId}.",
                    response.StatusCode, orderId);
                return null;
            }

            var apiResult = await response.Content.ReadFromJsonAsync<ApiResponse<OrderValidationResultDto>>(cancellationToken: cancellationToken);
            return apiResult?.Data;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to contact OrderService to validate order {OrderId}.", orderId);
            return null;
        }
    }

    public async Task<bool> UpdateOrderStatusToVerifiedAsync(int orderId, CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.HttpPutAsync($"/api/orders/{orderId}/verify", null, cancellationToken);
            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning("OrderService verify order {OrderId} returned {StatusCode}.", response.StatusCode, orderId);
                return false;
            }
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to notify OrderService of verified order {OrderId}.", orderId);
            return false;
        }
    }
}
