using InventoryService.DTOs;
using InventoryService.Models;
using InventoryService.Repositories;
using PharmacyManagement.Common.Models;

namespace InventoryService.Services;

public interface IDrugService
{
    Task<ApiResponse<IEnumerable<DrugDto>>> GetAllDrugsAsync(bool availableOnly = false);
    Task<ApiResponse<DrugDto>> GetDrugByIdAsync(int drugId);
    Task<ApiResponse<IEnumerable<DrugDto>>> GetLowStockDrugsAsync();
    Task<ApiResponse<IEnumerable<DrugDto>>> GetExpiredDrugsAsync();
    Task<ApiResponse<IEnumerable<DrugDto>>> SearchDrugsAsync(string? query, string? category);
    Task<ApiResponse<DrugDto>> CreateDrugAsync(CreateDrugDto dto);
    Task<ApiResponse<DrugDto>> UpdateDrugAsync(int drugId, UpdateDrugDto dto);
    Task<ApiResponse<bool>> DeleteDrugAsync(int drugId);
    Task<ApiResponse<StockCheckResultDto>> CheckAvailabilityAsync(DeductStockRequestDto request);
    Task<ApiResponse<bool>> DeductStockAsync(DeductStockRequestDto request);
    Task<ApiResponse<bool>> RestoreStockAsync(DeductStockRequestDto request);
}

public class DrugService : IDrugService
{
    private readonly IDrugRepository _drugRepository;

    public DrugService(IDrugRepository drugRepository)
    {
        _drugRepository = drugRepository;
    }

    public async Task<ApiResponse<IEnumerable<DrugDto>>> GetAllDrugsAsync(bool availableOnly = false)
    {
        var drugs = await _drugRepository.GetAllAsync(availableOnly);
        var dtos = drugs.Select(MapToDto);
        return ApiResponse<IEnumerable<DrugDto>>.SuccessResult(dtos, "Drugs retrieved successfully.");
    }

    public async Task<ApiResponse<DrugDto>> GetDrugByIdAsync(int drugId)
    {
        var drug = await _drugRepository.GetByIdAsync(drugId);
        if (drug == null)
        {
            return ApiResponse<DrugDto>.FailureResult($"Drug with ID {drugId} was not found.");
        }
        return ApiResponse<DrugDto>.SuccessResult(MapToDto(drug));
    }

    public async Task<ApiResponse<IEnumerable<DrugDto>>> GetLowStockDrugsAsync()
    {
        var drugs = await _drugRepository.GetLowStockAsync();
        var dtos = drugs.Select(MapToDto);
        return ApiResponse<IEnumerable<DrugDto>>.SuccessResult(dtos, "Low stock medicines retrieved successfully.");
    }

    public async Task<ApiResponse<IEnumerable<DrugDto>>> GetExpiredDrugsAsync()
    {
        var drugs = await _drugRepository.GetExpiredAsync();
        var dtos = drugs.Select(MapToDto);
        return ApiResponse<IEnumerable<DrugDto>>.SuccessResult(dtos, "Expired medicines retrieved successfully.");
    }

    public async Task<ApiResponse<IEnumerable<DrugDto>>> SearchDrugsAsync(string? query, string? category)
    {
        var drugs = await _drugRepository.SearchAsync(query, category);
        var dtos = drugs.Select(MapToDto);
        return ApiResponse<IEnumerable<DrugDto>>.SuccessResult(dtos, "Matching drugs retrieved successfully.");
    }

    public async Task<ApiResponse<DrugDto>> CreateDrugAsync(CreateDrugDto dto)
    {
        if (dto.Price <= 0)
        {
            return ApiResponse<DrugDto>.FailureResult("Medicine price must be greater than zero.");
        }
        if (dto.Quantity < 0)
        {
            return ApiResponse<DrugDto>.FailureResult("Stock quantity cannot be negative.");
        }

        var drugName = !string.IsNullOrWhiteSpace(dto.DrugName) ? dto.DrugName.Trim() : dto.Name?.Trim() ?? string.Empty;

        var drug = new Drug
        {
            DrugName = drugName,
            Description = dto.Description?.Trim(),
            Category = dto.Category?.Trim(),
            Price = dto.Price,
            ExpiryDate = dto.ExpiryDate,
            Quantity = dto.Quantity,
            MinimumStockQuantity = dto.MinimumStockQuantity > 0 ? dto.MinimumStockQuantity : 20,
            IsAvailable = dto.IsAvailable && dto.Quantity > 0,
            CreatedDate = DateTime.UtcNow
        };

        var created = await _drugRepository.AddAsync(drug);
        return ApiResponse<DrugDto>.SuccessResult(MapToDto(created), "Drug added successfully.");
    }

    public async Task<ApiResponse<DrugDto>> UpdateDrugAsync(int drugId, UpdateDrugDto dto)
    {
        var drug = await _drugRepository.GetByIdAsync(drugId);
        if (drug == null)
        {
            return ApiResponse<DrugDto>.FailureResult($"Drug with ID {drugId} was not found.");
        }

        var drugName = !string.IsNullOrWhiteSpace(dto.DrugName) ? dto.DrugName.Trim() : dto.Name?.Trim() ?? drug.DrugName;

        drug.DrugName = drugName;
        drug.Description = dto.Description?.Trim();
        drug.Category = dto.Category?.Trim();
        drug.Price = dto.Price;
        drug.ExpiryDate = dto.ExpiryDate;
        drug.Quantity = dto.Quantity;
        drug.MinimumStockQuantity = dto.MinimumStockQuantity > 0 ? dto.MinimumStockQuantity : drug.MinimumStockQuantity;
        drug.IsAvailable = dto.IsAvailable && dto.Quantity > 0;
        drug.UpdatedDate = DateTime.UtcNow;

        await _drugRepository.UpdateAsync(drug);
        return ApiResponse<DrugDto>.SuccessResult(MapToDto(drug), "Drug updated successfully.");
    }

    public async Task<ApiResponse<bool>> DeleteDrugAsync(int drugId)
    {
        var deleted = await _drugRepository.DeleteAsync(drugId);
        if (!deleted)
        {
            return ApiResponse<bool>.FailureResult($"Drug with ID {drugId} was not found.");
        }
        return ApiResponse<bool>.SuccessResult(true, "Drug deleted successfully.");
    }

    public async Task<ApiResponse<StockCheckResultDto>> CheckAvailabilityAsync(DeductStockRequestDto request)
    {
        var result = new StockCheckResultDto { IsAvailable = true };

        foreach (var item in request.Items)
        {
            var drug = await _drugRepository.GetByIdAsync(item.DrugId);
            if (drug == null || !drug.IsAvailable || drug.Quantity < item.Quantity || drug.ExpiryDate <= DateTime.UtcNow)
            {
                result.IsAvailable = false;
                result.OutOfStockItems.Add(
                    drug == null
                        ? $"Drug ID {item.DrugId} does not exist."
                        : $"{drug.DrugName}: requested {item.Quantity}, only {drug.Quantity} in stock (Available: {drug.IsAvailable}).");
            }
        }

        return ApiResponse<StockCheckResultDto>.SuccessResult(result);
    }

    public async Task<ApiResponse<bool>> DeductStockAsync(DeductStockRequestDto request)
    {
        // First verify availability for all items
        var check = await CheckAvailabilityAsync(request);
        if (!check.Data!.IsAvailable)
        {
            return ApiResponse<bool>.FailureResult("Cannot deduct stock. Some items are unavailable.", check.Data.OutOfStockItems);
        }

        // Apply deduction atomically
        foreach (var item in request.Items)
        {
            var drug = await _drugRepository.GetByIdAsync(item.DrugId);
            if (drug != null)
            {
                drug.Quantity -= item.Quantity;
                if (drug.Quantity <= 0)
                {
                    drug.Quantity = 0;
                    drug.IsAvailable = false;
                }
                drug.UpdatedDate = DateTime.UtcNow;
                await _drugRepository.UpdateAsync(drug);
            }
        }

        return ApiResponse<bool>.SuccessResult(true, "Stock deducted successfully.");
    }

    public async Task<ApiResponse<bool>> RestoreStockAsync(DeductStockRequestDto request)
    {
        if (request?.Items == null || !request.Items.Any())
        {
            return ApiResponse<bool>.SuccessResult(true, "No items to restore.");
        }

        foreach (var item in request.Items)
        {
            var drug = await _drugRepository.GetByIdAsync(item.DrugId);
            if (drug != null)
            {
                drug.Quantity += item.Quantity;
                if (drug.Quantity > 0)
                {
                    drug.IsAvailable = true;
                }
                drug.UpdatedDate = DateTime.UtcNow;
                await _drugRepository.UpdateAsync(drug);
            }
        }

        return ApiResponse<bool>.SuccessResult(true, "Stock restored successfully.");
    }

    private static DrugDto MapToDto(Drug drug) => new()
    {
        DrugId = drug.DrugId,
        DrugName = drug.DrugName,
        Description = drug.Description,
        Category = drug.Category,
        Price = drug.Price,
        ExpiryDate = drug.ExpiryDate,
        Quantity = drug.Quantity,
        MinimumStockQuantity = drug.MinimumStockQuantity,
        IsAvailable = drug.IsAvailable
    };
}

public interface ISupplierService
{
    Task<ApiResponse<IEnumerable<SupplierDto>>> GetAllSuppliersAsync();
    Task<ApiResponse<SupplierDto>> GetSupplierByIdAsync(int supplierId);
    Task<ApiResponse<SupplierDto>> CreateSupplierAsync(CreateSupplierDto dto);
    Task<ApiResponse<SupplierDto>> UpdateSupplierAsync(int supplierId, UpdateSupplierDto dto);
    Task<ApiResponse<bool>> DeleteSupplierAsync(int supplierId);
}

public class SupplierService : ISupplierService
{
    private readonly ISupplierRepository _supplierRepository;

    public SupplierService(ISupplierRepository supplierRepository)
    {
        _supplierRepository = supplierRepository;
    }

    public async Task<ApiResponse<IEnumerable<SupplierDto>>> GetAllSuppliersAsync()
    {
        var suppliers = await _supplierRepository.GetAllAsync();
        var dtos = suppliers.Select(MapToDto);
        return ApiResponse<IEnumerable<SupplierDto>>.SuccessResult(dtos, "Suppliers retrieved successfully.");
    }

    public async Task<ApiResponse<SupplierDto>> GetSupplierByIdAsync(int supplierId)
    {
        var supplier = await _supplierRepository.GetByIdAsync(supplierId);
        if (supplier == null)
        {
            return ApiResponse<SupplierDto>.FailureResult($"Supplier with ID {supplierId} not found.");
        }
        return ApiResponse<SupplierDto>.SuccessResult(MapToDto(supplier));
    }

    public async Task<ApiResponse<SupplierDto>> CreateSupplierAsync(CreateSupplierDto dto)
    {
        var supplier = new Supplier
        {
            SupplierName = dto.SupplierName.Trim(),
            Email = dto.Email.Trim().ToLower(),
            PhoneNumber = dto.PhoneNumber.Trim(),
            Address = dto.Address.Trim()
        };

        var created = await _supplierRepository.AddAsync(supplier);
        return ApiResponse<SupplierDto>.SuccessResult(MapToDto(created), "Supplier added successfully.");
    }

    public async Task<ApiResponse<SupplierDto>> UpdateSupplierAsync(int supplierId, UpdateSupplierDto dto)
    {
        var supplier = await _supplierRepository.GetByIdAsync(supplierId);
        if (supplier == null)
        {
            return ApiResponse<SupplierDto>.FailureResult($"Supplier with ID {supplierId} not found.");
        }

        supplier.SupplierName = dto.SupplierName.Trim();
        supplier.Email = dto.Email.Trim().ToLower();
        supplier.PhoneNumber = dto.PhoneNumber.Trim();
        supplier.Address = dto.Address.Trim();

        await _supplierRepository.UpdateAsync(supplier);
        return ApiResponse<SupplierDto>.SuccessResult(MapToDto(supplier), "Supplier updated successfully.");
    }

    public async Task<ApiResponse<bool>> DeleteSupplierAsync(int supplierId)
    {
        var deleted = await _supplierRepository.DeleteAsync(supplierId);
        if (!deleted)
        {
            return ApiResponse<bool>.FailureResult($"Supplier with ID {supplierId} not found.");
        }
        return ApiResponse<bool>.SuccessResult(true, "Supplier deleted successfully.");
    }

    private static SupplierDto MapToDto(Supplier supplier) => new()
    {
        SupplierId = supplier.SupplierId,
        SupplierName = supplier.SupplierName,
        Email = supplier.Email,
        PhoneNumber = supplier.PhoneNumber,
        Address = supplier.Address
    };
}

public interface IInventoryService
{
    Task<ApiResponse<IEnumerable<InventoryDto>>> GetAllInventoryAsync();
    Task<ApiResponse<InventoryDto>> AddInventoryStockAsync(CreateInventoryStockDto dto);
}

public class InventoryServiceClass : IInventoryService
{
    private readonly IInventoryRepository _inventoryRepository;
    private readonly IDrugRepository _drugRepository;
    private readonly ISupplierRepository _supplierRepository;

    public InventoryServiceClass(
        IInventoryRepository inventoryRepository,
        IDrugRepository drugRepository,
        ISupplierRepository supplierRepository)
    {
        _inventoryRepository = inventoryRepository;
        _drugRepository = drugRepository;
        _supplierRepository = supplierRepository;
    }

    public async Task<ApiResponse<IEnumerable<InventoryDto>>> GetAllInventoryAsync()
    {
        var records = await _inventoryRepository.GetAllWithDetailsAsync();
        var dtos = records.Select(i => new InventoryDto
        {
            InventoryId = i.InventoryId,
            SupplierId = i.SupplierId,
            SupplierName = i.Supplier?.SupplierName ?? "Unknown",
            DrugId = i.DrugId,
            DrugName = i.Drug?.DrugName ?? "Unknown",
            PurchasePrice = i.PurchasePrice,
            QuantitySupplied = i.QuantitySupplied,
            SupplyDate = i.SupplyDate,
            BatchNumber = i.BatchNumber,
            Notes = i.Notes
        });

        return ApiResponse<IEnumerable<InventoryDto>>.SuccessResult(dtos, "Inventory records retrieved.");
    }

    public async Task<ApiResponse<InventoryDto>> AddInventoryStockAsync(CreateInventoryStockDto dto)
    {
        var supplier = await _supplierRepository.GetByIdAsync(dto.SupplierId);
        if (supplier == null)
        {
            return ApiResponse<InventoryDto>.FailureResult($"Supplier ID {dto.SupplierId} not found.");
        }

        var drug = await _drugRepository.GetByIdAsync(dto.DrugId);
        if (drug == null)
        {
            return ApiResponse<InventoryDto>.FailureResult($"Drug ID {dto.DrugId} not found.");
        }

        int quantity = dto.QuantitySupplied > 0 ? dto.QuantitySupplied : (dto.QuantityAdded ?? 0);
        if (quantity <= 0)
        {
            return ApiResponse<InventoryDto>.FailureResult("Quantity supplied must be greater than zero.");
        }

        var inventory = new Inventory
        {
            SupplierId = dto.SupplierId,
            DrugId = dto.DrugId,
            PurchasePrice = dto.PurchasePrice,
            QuantitySupplied = quantity,
            SupplyDate = DateTime.UtcNow,
            BatchNumber = dto.BatchNumber?.Trim(),
            Notes = dto.Notes?.Trim()
        };

        var created = await _inventoryRepository.AddAsync(inventory);

        // Update drug stock & availability
        drug.Quantity += quantity;
        if (drug.Quantity > 0 && drug.ExpiryDate > DateTime.UtcNow)
        {
            drug.IsAvailable = true;
        }
        drug.UpdatedDate = DateTime.UtcNow;
        await _drugRepository.UpdateAsync(drug);

        var responseDto = new InventoryDto
        {
            InventoryId = created.InventoryId,
            SupplierId = created.SupplierId,
            SupplierName = supplier.SupplierName,
            DrugId = created.DrugId,
            DrugName = drug.DrugName,
            PurchasePrice = created.PurchasePrice,
            QuantitySupplied = created.QuantitySupplied,
            SupplyDate = created.SupplyDate,
            BatchNumber = created.BatchNumber,
            Notes = created.Notes
        };

        return ApiResponse<InventoryDto>.SuccessResult(responseDto, "Stock added to inventory and drug quantity updated.");
    }
}
