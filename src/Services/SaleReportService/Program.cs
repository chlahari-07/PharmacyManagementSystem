using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using PharmacyManagement.Common.Security;
using SaleReportService.Data;
using SaleReportService.Repositories;
using SaleReportService.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Pharmacy Management - SaleReport Service API",
        Version = "v1",
        Description = "Microservice for Sales Summary, Historical Reporting, Profit Margin Analysis & CSV Downloads"
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
builder.Services.AddDbContext<SaleReportDbContext>(options =>
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
        options.UseInMemoryDatabase("Pharmacy_SaleReportDB");
    }
});

builder.Services.AddPharmacyJwtAuthentication(builder.Configuration);

// Register Repositories and Services
builder.Services.AddScoped<ISaleReportRepository, SaleReportRepository>();

// Register typed HttpClient for OrderService communication
var orderServiceUrl = builder.Configuration["ServiceUrls:OrderService"] ?? "http://localhost:5003";
builder.Services.AddHttpClient<ISaleReportService, SaleReportServiceClass>(client =>
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
        var context = services.GetRequiredService<SaleReportDbContext>();
        await DbInitializer.InitializeAsync(context, logger, environment);
    }
    catch (Exception ex)
    {
        logger.LogCritical(ex, "FATAL: SaleReportService database initialization failed. Halting application startup.");
        throw;
    }
}

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "SaleReport Service API v1");
    c.RoutePrefix = "swagger";
});

app.UseCors("ConfiguredCorsPolicy");
app.UseAuthentication();
app.UseAuthorization();

// Health check endpoints: /health/live and /health/ready
app.MapGet("/health/live", () => Results.Ok(new
{
    status = "Healthy",
    service = "SaleReportService",
    timestamp = DateTime.UtcNow
}));

app.MapGet("/health/ready", async (SaleReportDbContext context) =>
{
    try
    {
        bool canConnect = await context.Database.CanConnectAsync();
        if (canConnect)
        {
            return Results.Ok(new
            {
                status = "Ready",
                service = "SaleReportService",
                database = "Pharmacy_SaleReportDB",
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
            service = "SaleReportService",
            error = ex.Message,
            timestamp = DateTime.UtcNow
        }, statusCode: StatusCodes.Status503ServiceUnavailable);
    }
});

app.MapControllers();

app.Run();
