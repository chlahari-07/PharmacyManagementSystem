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
        Description = "Microservice for Generating, Viewing, Downloading, and Printing Daily/Weekly/Monthly/Yearly Sales Reports"
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

// HttpClient to OrderService for retrieving order metrics
var orderServiceUrl = builder.Configuration.GetValue<string>("ServiceUrls:OrderService") ?? "http://localhost:5003";
builder.Services.AddHttpClient<ISaleReportService, SaleReportServiceClass>(client =>
{
    client.BaseAddress = new Uri(orderServiceUrl);
    client.Timeout = TimeSpan.FromSeconds(10);
});

// Register Repositories and Services (Internal MVC pattern)
builder.Services.AddScoped<ISaleReportRepository, SaleReportRepository>();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy => policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod());
});

var app = builder.Build();

// Seed initial reports
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var context = services.GetRequiredService<SaleReportDbContext>();
        await DbInitializer.InitializeAsync(context);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "An error occurred while seeding the SaleReport database.");
    }
}

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "SaleReport Service API v1");
    c.RoutePrefix = "swagger";
});

app.UseCors("AllowAll");
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
