using Microsoft.EntityFrameworkCore;
using PaymentService.Data;
using PaymentService.Models;

namespace PaymentService.Repositories;

public interface IPaymentRepository
{
    Task<IEnumerable<Payment>> GetAllAsync();
    Task<Payment?> GetByIdAsync(int paymentId);
    Task<Payment?> GetByOrderIdAsync(int orderId);
    Task<Payment> AddAsync(Payment payment);
    Task UpdateAsync(Payment payment);
}

public class PaymentRepository : IPaymentRepository
{
    private readonly PaymentDbContext _context;

    public PaymentRepository(PaymentDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Payment>> GetAllAsync()
    {
        return await _context.Payments
            .AsNoTracking()
            .OrderByDescending(p => p.PaymentDate)
            .ToListAsync();
    }

    public async Task<Payment?> GetByIdAsync(int paymentId)
    {
        return await _context.Payments.FirstOrDefaultAsync(p => p.PaymentId == paymentId);
    }

    public async Task<Payment?> GetByOrderIdAsync(int orderId)
    {
        return await _context.Payments.FirstOrDefaultAsync(p => p.OrderId == orderId);
    }

    public async Task<Payment> AddAsync(Payment payment)
    {
        await _context.Payments.AddAsync(payment);
        await _context.SaveChangesAsync();
        return payment;
    }

    public async Task UpdateAsync(Payment payment)
    {
        _context.Payments.Update(payment);
        await _context.SaveChangesAsync();
    }
}
