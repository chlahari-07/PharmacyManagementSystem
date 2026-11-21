using System.Net;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Moq;
using Moq.Protected;
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
        // Arrange: Mock HttpClient returning order total = 500, but payment = 300
        var mockHandler = new Mock<HttpMessageHandler>();
        var orderResponseJson = JsonSerializer.Serialize(new
        {
            success = true,
            message = "Order details",
            data = new
            {
                orderId = 1,
                status = "Pending",
                totalAmount = 500.00m
            }
        });

        mockHandler.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = new StringContent(orderResponseJson, System.Text.Encoding.UTF8, "application/json")
            });

        var client = new HttpClient(mockHandler.Object);
        var mockFactory = new Mock<IHttpClientFactory>();
        mockFactory.Setup(f => f.CreateClient(It.IsAny<string>())).Returns(client);

        var serviceWithOrderValidation = new PaymentServiceClass(_paymentRepository, mockFactory.Object);

        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 1,
            Amount = 300.00m, // Incorrect amount (order total is 500)
            PaymentMethod = "UPI"
        };

        // Act
        var result = await serviceWithOrderValidation.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("does not match"));
    }

    [Test]
    public async Task TC_CancelBeforePayment_PaymentRejectedOnCancelledOrder()
    {
        // Arrange: Mock HttpClient returning order status = "Cancelled"
        var mockHandler = new Mock<HttpMessageHandler>();
        var orderResponseJson = JsonSerializer.Serialize(new
        {
            success = true,
            message = "Order details",
            data = new
            {
                orderId = 2,
                status = "Cancelled",
                totalAmount = 250.00m
            }
        });

        mockHandler.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = new StringContent(orderResponseJson, System.Text.Encoding.UTF8, "application/json")
            });

        var client = new HttpClient(mockHandler.Object);
        var mockFactory = new Mock<IHttpClientFactory>();
        mockFactory.Setup(f => f.CreateClient(It.IsAny<string>())).Returns(client);

        var serviceWithOrderValidation = new PaymentServiceClass(_paymentRepository, mockFactory.Object);

        var simulateDto = new SimulatePaymentDto
        {
            OrderId = 2,
            Amount = 250.00m,
            PaymentMethod = "UPI"
        };

        // Act
        var result = await serviceWithOrderValidation.SimulatePaymentAsync(simulateDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("cancelled order"));
    }
}
