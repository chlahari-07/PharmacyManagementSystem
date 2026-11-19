using Microsoft.EntityFrameworkCore;
using NUnit.Framework;
using PaymentService.Data;
using PaymentService.DTOs;
using PaymentService.Models;
using PaymentService.Repositories;
using PaymentService.Services;
using PharmacyManagement.Common.Models;

namespace PharmacyManagement.Tests;

[TestFixture]
public class PaymentServiceTests
{
    private PaymentDbContext _context = null!;
    private IPaymentRepository _paymentRepository = null!;
    private IPaymentService _paymentService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<PaymentDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new PaymentDbContext(options);
        _paymentRepository = new PaymentRepository(_context);
        _paymentService = new PaymentServiceClass(_paymentRepository);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC17_ProcessPayment_ValidOrder_CreatesPaymentCompletedWith1to1Relationship()
    {
        // Arrange
        var paymentDto = new ProcessPaymentDto
        {
            OrderId = 101,
            Amount = 48.50m,
            PaymentMethod = "CreditCard"
        };

        // Act
        var result = await _paymentService.ProcessPaymentAsync(paymentDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.OrderId, Is.EqualTo(101));
        Assert.That(result.Data.PaymentStatus, Is.EqualTo(PaymentStatuses.Completed));
        Assert.That(result.Data.TransactionReference, Is.Not.Empty);

        // Verify duplicate payment for same order is rejected
        var duplicateResult = await _paymentService.ProcessPaymentAsync(paymentDto);
        Assert.That(duplicateResult.Success, Is.False);
    }

    [Test]
    public async Task TC18_SimulatePayment_SuccessAndFailureScenarios()
    {
        // 1. Successful simulation
        var successDto = new SimulatePaymentDto
        {
            OrderId = 201,
            Amount = 99.00m,
            PaymentMethod = "UPI",
            SimulateFailure = false
        };

        var successResult = await _paymentService.SimulatePaymentAsync(successDto);

        Assert.That(successResult.Success, Is.True);
        Assert.That(successResult.Data!.PaymentStatus, Is.EqualTo(PaymentStatuses.Completed));

        // 2. Failed simulation
        var failedDto = new SimulatePaymentDto
        {
            OrderId = 202,
            Amount = 150.00m,
            PaymentMethod = "NetBanking",
            SimulateFailure = true
        };

        var failResult = await _paymentService.SimulatePaymentAsync(failedDto);

        Assert.That(failResult.Success, Is.True);
        Assert.That(failResult.Data!.PaymentStatus, Is.EqualTo(PaymentStatuses.Failed));
    }
}
