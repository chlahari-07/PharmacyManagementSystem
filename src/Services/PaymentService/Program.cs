using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using PaymentService.Data;
using PaymentService.Repositories;
using PaymentService.Services;
using PharmacyManagement.Common.Security;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Pharmacy Management - Payment Service API (SIMULATED)",
        Version = "v1",
        Description = "Microservice for Simulated 1:1 Order Payment Processing. IMPORTANT: Payment processing is completely simulated. No real money is transferred."
    });

    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Enter JWT Bearer token format: Bearer {token}"
    });

    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<PaymentDbContext>(options =>
{
    if (!string.IsNullOrEmpty(connectionString))
    {
        options.UseSqlServer(connectionString, sqlOptions =>
        {
            sqlOptions.EnableRetryOnFailure(maxRetryCount: 3, maxRetryDelay: TimeSpan.FromSeconds(5), errorNumbersToAdd: null);
        });
    }
    else
    {
        options.UseInMemoryDatabase("Pharmacy_PaymentDB");
    }
});

builder.Services.AddPharmacyJwtAuthentication(builder.Configuration);

// Register Repositories and Services
builder.Services.AddScoped<IPaymentRepository, PaymentRepository>();
builder.Services.AddScoped<IPaymentService, PaymentServiceClass>();

// Register typed HttpClient for OrderServiceClient
var orderServiceUrl = builder.Configuration["ServiceUrls:OrderService"] ?? "http://localhost:5003";
builder.Services.AddHttpClient<IOrderServiceClient, OrderServiceClient>(client =>
{
    client.BaseAddress = new Uri(orderServiceUrl);
    client.Timeout = TimeSpan.FromSeconds(10);
});

// Restrictive CORS
var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>()
    ?? new[] { "http://localhost:3000", "http://localhost:4200", "http://localhost:5000", "http://localhost:5173" };

builder.Services.AddCors(options =>
{
    options.AddPolicy("ConfiguredCorsPolicy", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Seed initial data during startup
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    var logger = services.GetRequiredService<ILogger<Program>>();
    var environment = services.GetRequiredService<IHostEnvironment>();

    try
    {
        var context = services.GetRequiredService<PaymentDbContext>();
        await DbInitializer.InitializeAsync(context, logger, environment);
    }
    catch (Exception ex)
    {
        logger.LogCritical(ex, "FATAL: PaymentService database initialization failed. Halting application startup.");
        throw;
    }
}

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Payment Service API (SIMULATED) v1");
    c.RoutePrefix = "swagger";
});

app.UseCors("ConfiguredCorsPolicy");
app.UseAuthentication();
app.UseAuthorization();

// Health check endpoints: /health/live and /health/ready
app.MapGet("/health/live", () => Results.Ok(new
{
    status = "Healthy",
    service = "PaymentService",
    isSimulation = true,
    timestamp = DateTime.UtcNow
}));

app.MapGet("/health/ready", async (PaymentDbContext context) =>
{
    try
    {
        bool canConnect = await context.Database.CanConnectAsync();
        if (canConnect)
        {
            return Results.Ok(new
            {
                status = "Ready",
                service = "PaymentService",
                database = "Pharmacy_PaymentDB",
                timestamp = DateTime.UtcNow
            });
        }
        return Results.StatusCode(StatusCodes.Status503ServiceUnavailable);
    }
    catch (Exception ex)
    {
        return Results.Json(new
        {
            status = "Unhealthy",
            service = "PaymentService",
            error = ex.Message,
            timestamp = DateTime.UtcNow
        }, statusCode: StatusCodes.Status503ServiceUnavailable);
    }
});

app.MapControllers();

app.Run();
