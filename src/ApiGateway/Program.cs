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
        Title = "Pharmacy Management - Unified API Gateway",
        Version = "v1",
        Description = "Unified Gateway routing for Pharmacy Management Microservices. Select a microservice from the dropdown above to view and test its endpoints."
    });
});

// Restrictive CORS
var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>()
    ?? new[] { "http://localhost:3000", "http://localhost:4200", "http://localhost:5000", "http://localhost:5173" };

builder.Services.AddCors(options =>
{
    options.AddPolicy("ConfiguredCorsPolicy", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseCors("ConfiguredCorsPolicy");

// Enable Unified Swagger UI displaying all five microservices
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Gateway (Overview)");
    c.SwaggerEndpoint("/docs/auth/v1/swagger.json", "1. Auth Service (Users & JWT)");
    c.SwaggerEndpoint("/docs/inventory/v1/swagger.json", "2. Inventory Service (Drugs & Stock)");
    c.SwaggerEndpoint("/docs/orders/v1/swagger.json", "3. Order Service (Orders & Cart)");
    c.SwaggerEndpoint("/docs/payments/v1/swagger.json", "4. Payment Service (SIMULATED Payments)");
    c.SwaggerEndpoint("/docs/salereports/v1/swagger.json", "5. SaleReport Service (Analytics)");
    c.RoutePrefix = string.Empty; // Serve Swagger at http://localhost:5000/
});

// Gateway Health endpoints
app.MapGet("/health/live", () => Results.Ok(new
{
    status = "Healthy",
    service = "ApiGateway",
    timestamp = DateTime.UtcNow
}));

app.MapGet("/health/ready", () => Results.Ok(new
{
    status = "Ready",
    service = "ApiGateway",
    routingLayer = "YARP",
    timestamp = DateTime.UtcNow
}));

// Map YARP Reverse Proxy routes
app.MapReverseProxy();

app.Run();
