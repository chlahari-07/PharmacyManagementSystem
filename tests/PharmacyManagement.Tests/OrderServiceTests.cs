using Microsoft.EntityFrameworkCore;
using Moq;
using NUnit.Framework;
using OrderService.Data;
using OrderService.DTOs;
using OrderService.Models;
using OrderService.Repositories;
using OrderService.Services;
using PharmacyManagement.Common.Models;

namespace PharmacyManagement.Tests;

[TestFixture]
public class OrderServiceTests
{
    private OrderDbContext _context = null!;
    private IOrderRepository _orderRepository = null!;
    private Mock<IInventoryServiceClient> _mockInventoryClient = null!;
    private IOrderService _orderService = null!;

    [SetUp]
    public void SetUp()
    {
        var options = new DbContextOptionsBuilder<OrderDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new OrderDbContext(options);
        _orderRepository = new OrderRepository(_context);
        _mockInventoryClient = new Mock<IInventoryServiceClient>();

        _mockInventoryClient
            .Setup(c => c.DeductStockAsync(It.IsAny<InterServiceDeductStockRequest>()))
            .ReturnsAsync(true);

        _mockInventoryClient
            .Setup(c => c.ReleaseStockAsync(It.IsAny<InterServiceDeductStockRequest>()))
            .ReturnsAsync(true);

        _orderService = new OrderServiceClass(_orderRepository, _mockInventoryClient.Object);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC11_CreateOrder_WithValidItems_CalculatesTotalAndTriggersStockDeduction()
    {
        // Arrange
        var orderDto = new CreateOrderDto
        {
            DoctorId = 1,
            Status = "Pending",
            Items = new List<CreateOrderItemDto>
            {
                new() { DrugId = 1, DrugName = "Paracetamol 500mg", Quantity = 2, UnitPrice = 10.00m }
            }
        };

        // Act
        var result = await _orderService.CreateOrderAsync(1, orderDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Status, Is.EqualTo(OrderStatuses.Pending));
        Assert.That(result.Data.TotalAmount, Is.EqualTo(20.00m));
        _mockInventoryClient.Verify(c => c.DeductStockAsync(It.IsAny<InterServiceDeductStockRequest>()), Times.Once);
    }

    [Test]
    public async Task TC12_CreateOrder_WithEmptyCart_FailsValidation()
    {
        // Arrange: empty items list
        var orderDto = new CreateOrderDto
        {
            DoctorId = 1,
            Items = new List<CreateOrderItemDto>()
        };

        // Act
        var result = await _orderService.CreateOrderAsync(1, orderDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("at least one item"));
    }

    [Test]
    public async Task TC13_GetMyOrders_DoctorViewsOwnOrderHistory_ReturnsOnlyDoctorOrders()
    {
        // Arrange
        var orderDoctor1 = new Order
        {
            DoctorID = 1,
            TotalAmount = 50.00m,
            Status = OrderStatuses.Pending
        };
        var orderDoctor2 = new Order
        {
            DoctorID = 2,
            TotalAmount = 80.00m,
            Status = OrderStatuses.Pending
        };
        await _context.Orders.AddRangeAsync(orderDoctor1, orderDoctor2);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.GetMyOrdersAsync(1);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.All(o => o.DoctorID == 1), Is.True);
        Assert.That(result.Data!.Count(), Is.EqualTo(1));
    }

    [Test]
    public async Task TC14_VerifyOrder_AdminVerifiesPendingOrder_UpdatesStatusToVerified()
    {
        // Arrange
        var order = new Order
        {
            DoctorID = 1,
            TotalAmount = 100.00m,
            Status = OrderStatuses.Pending
        };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.VerifyOrderAsync(order.OrderId);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.Status, Is.EqualTo(OrderStatuses.Verified));
    }

    [Test]
    public async Task TC15_MarkOrderAsPickedUp_AdminMarksVerifiedOrder_UpdatesStatusToPickedUp()
    {
        // Arrange
        var order = new Order
        {
            DoctorID = 1,
            TotalAmount = 75.00m,
            Status = OrderStatuses.Verified // Verified status is required before pickup
        };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.MarkOrderAsPickedUpAsync(order.OrderId);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.Status, Is.EqualTo(OrderStatuses.PickedUp));
    }

    [Test]
    public async Task TC16_CancelOrder_DoctorCancelsBeforePaymentAndPickup_UpdatesStatusToCancelledAndReleasesStock()
    {
        // Arrange: Order is Pending (before payment is completed)
        var order = new Order
        {
            DoctorID = 1,
            TotalAmount = 100.00m,
            Status = OrderStatuses.Pending,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 1, DrugName = "Paracetamol", Quantity = 2, UnitPrice = 10.00m }
            }
        };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.CancelOrderAsync(order.OrderId);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.Status, Is.EqualTo(OrderStatuses.Cancelled));
        _mockInventoryClient.Verify(c => c.ReleaseStockAsync(It.IsAny<InterServiceDeductStockRequest>()), Times.Once);
    }

    [Test]
    public async Task TC26_CreateOrder_ForExpiredOrUnavailableMedicine_RejectsOrder()
    {
        // Arrange: Mock InventoryClient to report failure (e.g. medicine expired/unavailable)
        _mockInventoryClient
            .Setup(c => c.DeductStockAsync(It.IsAny<InterServiceDeductStockRequest>()))
            .ReturnsAsync(false);

        var orderDto = new CreateOrderDto
        {
            DoctorId = 1,
            Status = "Pending",
            Items = new List<CreateOrderItemDto>
            {
                new() { DrugId = 5, DrugName = "Expired Amoxicillin", Quantity = 1, UnitPrice = 25.00m }
            }
        };

        // Act
        var result = await _orderService.CreateOrderAsync(1, orderDto);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("expired").Or.Contains("out of stock").Or.Contains("unavailable"));
    }

    [Test]
    public async Task TC27_CancelOrder_AfterPickup_RejectsCancellation()
    {
        // Arrange: Order is PickedUp
        var order = new Order
        {
            DoctorID = 1,
            TotalAmount = 150.00m,
            Status = OrderStatuses.PickedUp
        };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.CancelOrderAsync(order.OrderId);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("already been picked up"));
    }
}
