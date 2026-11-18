using Microsoft.EntityFrameworkCore;
using OrderService.Data;
using OrderService.Models;

namespace OrderService.Repositories;

public interface IOrderRepository
{
    Task<IEnumerable<Order>> GetAllOrdersAsync();
    Task<IEnumerable<Order>> GetOrdersByDoctorIdAsync(int doctorId);
    Task<IEnumerable<Order>> GetOrdersByStatusAsync(string status);
    Task<Order?> GetOrderByIdAsync(int orderId);
    Task<Order> CreateOrderAsync(Order order);
    Task UpdateOrderAsync(Order order);
    Task<bool> ExistsAsync(int orderId);
}

public class OrderRepository : IOrderRepository
{
    private readonly OrderDbContext _context;

    public OrderRepository(OrderDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Order>> GetAllOrdersAsync()
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .AsNoTracking()
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync();
    }

    public async Task<IEnumerable<Order>> GetOrdersByDoctorIdAsync(int doctorId)
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .AsNoTracking()
            .Where(o => o.DoctorID == doctorId)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync();
    }

    public async Task<IEnumerable<Order>> GetOrdersByStatusAsync(string status)
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .AsNoTracking()
            .Where(o => o.Status.ToLower() == status.Trim().ToLower())
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync();
    }

    public async Task<Order?> GetOrderByIdAsync(int orderId)
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .FirstOrDefaultAsync(o => o.OrderId == orderId);
    }

    public async Task<Order> CreateOrderAsync(Order order)
    {
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();
        return order;
    }

    public async Task UpdateOrderAsync(Order order)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync();
    }

    public async Task<bool> ExistsAsync(int orderId)
    {
        return await _context.Orders.AnyAsync(o => o.OrderId == orderId);
    }
}
