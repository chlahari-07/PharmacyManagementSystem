using System.Net.Http.Json;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using OrderService.DTOs;
using PharmacyManagement.Common.Models;
using PharmacyManagement.Common.Security;

namespace OrderService.Services;

public interface IInventoryServiceClient
{
    Task<bool> DeductStockAsync(InterServiceDeductStockRequest request, CancellationToken cancellationToken = default);
    Task<bool> ReleaseStockAsync(InterServiceDeductStockRequest request, CancellationToken cancellationToken = default);
    Task<DrugValidationDto?> GetDrugDetailsAsync(int drugId, CancellationToken cancellationToken = default);
}

public class InventoryServiceClient : IInventoryServiceClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<InventoryServiceClient> _logger;
    private readonly string _internalKey;

    public InventoryServiceClient(
        HttpClient httpClient,
        IConfiguration configuration,
        ILogger<InventoryServiceClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
        _internalKey = configuration[InternalServiceConstants.SecretKeyConfig] ?? string.Empty;

        // Ensure internal service key header is included if configured
        if (!string.IsNullOrEmpty(_internalKey) && !_httpClient.DefaultRequestHeaders.Contains(InternalServiceConstants.HeaderName))
        {
            _httpClient.DefaultRequestHeaders.Add(InternalServiceConstants.HeaderName, _internalKey);
        }
    }

    public async Task<bool> DeductStockAsync(InterServiceDeductStockRequest request, CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync("/api/drugs/deduct-stock", request, cancellationToken);
            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync(cancellationToken);
                _logger.LogWarning("Failed to deduct stock from InventoryService. StatusCode: {StatusCode}, Body: {Body}",
                    response.StatusCode, content);
                return false;
            }

            var apiResult = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>(cancellationToken: cancellationToken);
            return apiResult?.Success == true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error communicating with InventoryService during stock deduction. Request rejected.");
            // Do NOT return true! Stock deduction failure must reject the order.
            return false;
        }
    }

    public async Task<bool> ReleaseStockAsync(InterServiceDeductStockRequest request, CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync("/api/drugs/restore-stock", request, cancellationToken);
            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync(cancellationToken);
                _logger.LogWarning("Failed to restore stock in InventoryService. StatusCode: {StatusCode}, Body: {Body}",
                    response.StatusCode, content);
                return false;
            }

            var apiResult = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>(cancellationToken: cancellationToken);
            return apiResult?.Success == true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error communicating with InventoryService during stock restoration. Restoration failed.");
            // Stock restoration failed
            return false;
        }
    }

    public async Task<DrugValidationDto?> GetDrugDetailsAsync(int drugId, CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.GetAsync($"/api/drugs/{drugId}", cancellationToken);
            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning("InventoryService returned {StatusCode} for drug ID {DrugId}.", response.StatusCode, drugId);
                return null;
            }

            var apiResult = await response.Content.ReadFromJsonAsync<ApiResponse<DrugValidationDto>>(cancellationToken: cancellationToken);
            return apiResult?.Data;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to retrieve drug {DrugId} details from InventoryService.", drugId);
            return null;
        }
    }
}
