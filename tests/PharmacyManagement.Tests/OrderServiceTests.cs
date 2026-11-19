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

        _orderService = new OrderServiceClass(_orderRepository, _mockInventoryClient.Object);
    }

    [TearDown]
    public void TearDown()
    {
        _context.Dispose();
    }

    [Test]
    public async Task TC11_AddToCart_DoctorAddsDrug_CreatesOrderWithStatusCart()
    {
        // Arrange
        var addToCartDto = new AddToCartDto
        {
            DoctorId = 2,
            Items = new List<CreateOrderItemDto>
            {
                new() { DrugId = 1, DrugName = "Paracetamol 500mg", Quantity = 2, UnitPrice = 9.99m }
            }
        };

        // Act
        var result = await _orderService.AddToCartAsync(2, addToCartDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Status, Is.EqualTo(OrderStatuses.Cart));
        Assert.That(result.Data.TotalAmount, Is.EqualTo(19.98m));
    }

    [Test]
    public async Task TC12_PlaceOrder_DoctorBuysDrugs_CreatesOrderWithStatusPendingAndTriggersStockDeduction()
    {
        // Arrange
        var orderDto = new CreateOrderDto
        {
            DoctorId = 2,
            Status = "Pending",
            Items = new List<CreateOrderItemDto>
            {
                new() { DrugId = 1, DrugName = "Paracetamol 500mg", Quantity = 3, UnitPrice = 9.99m },
                new() { DrugId = 2, DrugName = "Amoxicillin 250mg", Quantity = 1, UnitPrice = 18.50m }
            }
        };

        // Act
        var result = await _orderService.CreateOrderAsync(2, orderDto);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data, Is.Not.Null);
        Assert.That(result.Data!.Status, Is.EqualTo(OrderStatuses.Pending));
        Assert.That(result.Data.TotalAmount, Is.EqualTo(48.47m));
        _mockInventoryClient.Verify(c => c.DeductStockAsync(It.IsAny<InterServiceDeductStockRequest>()), Times.Once);
    }

    [Test]
    public async Task TC13_ValidateOrder_ValidOrder_ReturnsTrue()
    {
        // Arrange
        var order = new Order
        {
            DoctorID = 2,
            TotalAmount = 50.00m,
            Status = OrderStatuses.Pending,
            OrderItems = new List<OrderItem>
            {
                new() { DrugId = 1, DrugName = "Paracetamol", Quantity = 5, UnitPrice = 10.00m }
            }
        };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.ValidateOrderAsync(order.OrderId);

        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.Data!.IsValid, Is.True);
        Assert.That(result.Data.ItemCount, Is.EqualTo(1));
    }

    [Test]
    public async Task TC14_VerifyOrder_AdminValidatesAndVerifies_UpdatesStatusToVerified()
    {
        // Arrange
        var order = new Order
        {
            DoctorID = 2,
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
    public async Task TC15_MarkOrderAsPickedUp_VerifiedOrder_MovesToPickedUpSection()
    {
        // Arrange
        var order = new Order
        {
            DoctorID = 2,
            TotalAmount = 75.00m,
            Status = OrderStatuses.Verified // Already verified
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
    public async Task TC16_MarkOrderAsPickedUp_UnverifiedOrder_RejectsPickup()
    {
        // Arrange
        var order = new Order
        {
            DoctorID = 2,
            TotalAmount = 75.00m,
            Status = OrderStatuses.Pending // Not yet verified
        };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _orderService.MarkOrderAsPickedUpAsync(order.OrderId);

        // Assert
        Assert.That(result.Success, Is.False);
        Assert.That(result.Message, Does.Contain("must be verified"));
    }
}
