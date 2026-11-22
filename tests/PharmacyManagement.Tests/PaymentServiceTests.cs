using Microsoft.EntityFrameworkCore;
using Moq;
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
    private Mock<IOrderServiceClient> _mockOrderServiceClient = null!;
    private IPaymentService _paymentService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<PaymentDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new PaymentDbContext(options);
        _paymentRepository = new PaymentRepository(_context);
        _mockOrderServiceClient = new Mock<IOrderServiceClient>();

        // Default: Order 1 exists, Pending, TotalAmount = $500.00
        _mockOrderServiceClient
            .Setup(c => c.GetOrderForValidationAsync(1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new OrderValidationResultDto
            {
                OrderId = 1,
                DoctorID = 2,
                TotalAmount = 500.00m,
                Status = OrderStatuses.Pending
            });

        // Order 2: Cancelled order
        _mockOrderServiceClient
            .Setup(c => c.GetOrderForValidationAsync(2, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new OrderValidationResultDto
            {
                OrderId = 2,
                DoctorID = 2,
                TotalAmount = 250.00m,
                Status = OrderStatuses.Cancelled
            });

        // Non-existent order 999: returns null
        _mockOrderServiceClient
            .Setup(c => c.GetOrderForValidationAsync(999, It.IsAny<CancellationToken>()))
            .ReturnsAsync((OrderValidationResultDto?)null);

        _mockOrderServiceClient
            .Setup(c => c.UpdateOrderStatusToVerifiedAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        _paymentService = new PaymentServiceClass(_paymentRepository, _mockOrderServiceClient.Object);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC17_SimulatePayment_ForPendingOrder_CreatesPaymentCompletedRecord()
    {
        // Arrange
        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 1,
            Amount = 500.00m,
            PaymentMethod = "UPI",
            SimulateFailure = false
        };

        // Act
        var result = await _paymentService.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.OrderId, Is.EqualTo(1));
        Assert.That(result.Data.Amount, Is.EqualTo(500.00m));
        Assert.That(result.Data.PaymentStatus, Is.EqualTo(PaymentStatuses.Completed));
        Assert.That(result.Data.TransactionReference, Is.Not.Empty);
        Assert.That(result.Message, Does.Contain("No real money was transferred"));
        _mockOrderServiceClient.Verify(c => c.UpdateOrderStatusToVerifiedAsync(1, It.IsAny<CancellationToken>()), Times.Once);
    }

    [Test]
    public async Task TC18_SimulateDuplicatePayment_RejectsDuplicatePaymentForSameOrder()
    {
        // Arrange: Existing completed payment for OrderId 1
        var existingPayment = new Payment
        {
            OrderId = 1,
            Amount = 500.00m,
            PaymentDate = DateTime.UtcNow,
            PaymentMethod = "UPI",
            PaymentStatus = PaymentStatuses.Completed,
            TransactionReference = "SIM-TXN-12345"
        };
        await _context.Payments.AddAsync(existingPayment);
        await _context.SaveChangesAsync();

        var duplicateDto = new SimulatePaymentDto
        {
            OrderId = 1,
            Amount = 500.00m,
            PaymentMethod = "UPI"
        };

        // Act
        var result = await _paymentService.SimulatePaymentAsync(duplicateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("already been paid"));
    }

    [Test]
    public async Task TC28_SimulatePayment_WithIncorrectAmount_RejectsPayment()
    {
        // Arrange: Order 1 has TotalAmount $500.00, but client sends $300.00
        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 1,
            Amount = 300.00m,
            PaymentMethod = "CreditCard"
        };

        // Act
        var result = await _paymentService.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("does not match the actual order total"));
    }

    [Test]
    public async Task TC30_SimulatePayment_ForCancelledOrder_StrictlyRejected()
    {
        // Arrange: Order 2 is Cancelled
        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 2,
            Amount = 250.00m,
            PaymentMethod = "UPI"
        };

        // Act
        var result = await _paymentService.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("Cannot process payment for a cancelled order"));
    }

    [Test]
    public async Task TC35_SimulatePayment_WithNonExistentOrder_RejectsPayment()
    {
        // Arrange: Order 999 does not exist
        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 999,
            Amount = 100.00m,
            PaymentMethod = "Cash"
        };

        // Act
        var result = await _paymentService.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("does not exist"));
    }

    [Test]
    public async Task TC36_SimulatePayment_WithSimulateFailureToggle_CreatesFailedTransactionRecord()
    {
        // Arrange: Toggle failure simulation to true
        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 1,
            Amount = 500.00m,
            PaymentMethod = "DebitCard",
            SimulateFailure = true
        };

        // Act
        var result = await _paymentService.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.PaymentStatus, Is.EqualTo(PaymentStatuses.Failed));
        Assert.That(result.Data.TransactionReference, Does.StartWith("SIM-FAILED-"));
        // Order should not be verified on failed payment
        _mockOrderServiceClient.Verify(c => c.UpdateOrderStatusToVerifiedAsync(1, It.IsAny<CancellationToken>()), Times.Never);
    }
}
