using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Add YARP Reverse Proxy configuration
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

// Add Swagger / OpenAPI for API Gateway
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Pharmacy Management - YARP API Gateway",
        Version = "v1",
        Description = "Unified API Gateway for Pharmacy Management System Microservices (Auth, Inventory, Orders, Payments, SaleReports)."
    });
});

// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseCors("AllowAll");

// Enable Swagger UI on Gateway
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Pharmacy Management API Gateway v1");
    c.RoutePrefix = string.Empty; // Swagger at root http://localhost:5000/
});

// Map YARP Reverse Proxy routes
app.MapReverseProxy();

app.Run();
