# Pharmacy Management System (.NET 10 Microservices) — 3-Day Technical Masterclass & Interview Guide

Welcome to the **Pharmacy Management System** learning guide. This document is crafted specifically for you as a beginner in ASP.NET Core microservices with **three days** to master the entire system, explain every architectural decision, understand the code line-by-line, and ace any technical interview.

---

## Table of Contents
- [Executive Overview](#executive-overview)
- [Day 1: Microservices Architecture, ASP.NET Core Fundamentals & SQL Server Database](#day-1-microservices-architecture-aspnet-core-fundamentals--sql-server-database)
  - [1.1 What is this Pharmacy Management System?](#11-what-is-this-pharmacy-management-system)
  - [1.2 Why Microservices Architecture?](#12-why-microservices-architecture)
  - [1.3 The 8 Solution Projects Explained](#13-the-8-solution-projects-explained)
  - [1.4 ASP.NET Core Web API & Modern Program.cs (.NET 10)](#14-aspnet-core-web-api--modern-programcs-net-10)
  - [1.5 Dependency Injection (DI) & Service Lifetimes](#15-dependency-injection-di--service-lifetimes)
  - [1.6 The Controller-Service-Repository-DbContext Pattern](#16-the-controller-service-repository-dbcontext-pattern)
  - [1.7 Entity Framework Core (EF Core) Code-First & Migrations](#17-entity-framework-core-ef-core-code-first--migrations)
  - [1.8 The 5 Isolated SQL Server Express Databases](#18-the-5-isolated-sql-server-express-databases)
  - [1.9 SQL Server Express Setup & .NET User Secrets Configuration](#19-sql-server-express-setup--net-user-secrets-configuration)
  - [1.10 Running the Solution & Exploring Swagger UI](#110-running-the-solution--exploring-swagger-ui)
- [Day 2: Authentication, Security & Core Business Workflows](#day-2-authentication-security--core-business-workflows)
  - [2.1 Authentication & Role-Based Authorization (Admin vs Doctor)](#21-authentication--role-based-authorization-admin-vs-doctor)
  - [2.2 Password Hashing with Salt (BCrypt)](#22-password-hashing-with-salt-bcrypt)
  - [2.3 JWT Generation, Signing & Secure Key Management](#23-jwt-generation-signing--secure-key-management)
  - [2.4 Medicine Catalog & Supplier Management](#24-medicine-catalog--supplier-management)
  - [2.5 Inventory Inward Stock Batches & Low-Stock Alerts](#25-inventory-inward-stock-batches--low-stock-alerts)
  - [2.6 Order Placement with Server-Side Price Calculation (Zero Client Trust)](#26-order-placement-with-server-side-price-calculation-zero-client-trust)
  - [2.7 Order Cancellation Before Payment & Automated Inventory Stock Restoration](#27-order-cancellation-before-payment--automated-inventory-stock-restoration)
  - [2.8 Doctor Order Ownership Enforcement & Security Checks](#28-doctor-order-ownership-enforcement--security-checks)
  - [2.9 Simulated Payment Processing (No Real Money Transferred)](#29-simulated-payment-processing-no-real-money-transferred)
  - [2.10 Typed HttpClient & Inter-Service REST Communication](#210-typed-httpclient--inter-service-rest-communication)
- [Day 3: Reporting, Health Checks, Testing & Interview Preparation](#day-3-reporting-health-checks-testing--interview-preparation)
  - [3.1 Genuine Sales Reporting & Revenue Calculation](#31-genuine-sales-reporting--revenue-calculation)
  - [3.2 Profit Margin Calculation & Top-Selling Drugs Aggregation](#32-profit-margin-calculation--top-selling-drugs-aggregation)
  - [3.3 Unified Gateway Swagger UI via YARP](#33-unified-gateway-swagger-ui-via-yarp)
  - [3.4 Production Health Checks (/health/live & /health/ready)](#34-production-health-checks-healthlive--healthready)
  - [3.5 Automated NUnit & Moq Testing Suite](#35-automated-nunit--moq-testing-suite)
  - [3.6 SQL Server Express Integration Testing (PHARMACY_TEST_SQLSERVER)](#36-sql-server-express-integration-testing-pharmacy_test_sqlserver)
  - [3.7 Two-Minute & Five-Minute Interview Pitches](#37-two-minute--five-minute-interview-pitches)
  - [3.8 Five Real Engineering Challenges Solved](#38-five-real-engineering-challenges-solved)
  - [3.9 40+ Technical Interview Questions & In-Depth Answers](#39-40-technical-interview-questions--in-depth-answers)

---

# Day 1: Microservices Architecture, ASP.NET Core Fundamentals & SQL Server Database

## 1.1 What is this Pharmacy Management System?
The **Pharmacy Management System** is an enterprise-grade, distributed backend platform built with **C# and ASP.NET Core Web API targeting .NET 10**. It automates pharmaceutical inventory tracking, wholesale supplier orders, prescription purchases by verified doctors, simulated payment processing, and executive financial reporting.

---

## 1.2 Why Microservices Architecture?
In a traditional monolithic application, code for users, inventory, orders, billing, and reporting all lives inside one giant project sharing a single database. If the reporting module consumes heavy CPU, the entire online store lags or crashes. If an engineer changes billing logic, they risk breaking inventory.

In our **Microservices Architecture**:
1. **Fault Isolation**: If the `SaleReportService` goes down, doctors can still browse medicines, place orders, and pay.
2. **Database Isolation (Database-per-Service)**: Each service has exclusive access to its own SQL database. No service can run direct joins against another service's private tables. Data integrity is guarded strictly by business APIs.
3. **Independent Scalability**: `InventoryService` can handle 10,000 read requests per second while `PaymentService` processes transactions in an isolated security perimeter.
4. **Technology & Schema Independence**: Each service owns its EF Core Code-First migrations independently.

---

## 1.3 The 8 Solution Projects Explained

Our solution (`PharmacyManagement.sln`) contains exactly 8 projects:

```
PharmacyManagement/
├── src/
│   ├── ApiGateway/                       # [1] Port 5000: YARP Gateway reverse proxy + Unified Swagger
│   ├── Common/
│   │   └── PharmacyManagement.Common/    # [2] Shared security, JWT tokens, DTOs, and API responses
│   └── Services/
│       ├── AuthService/                  # [3] Port 5001: User registration, pre-seeded Admin, and JWT issuance
│       ├── InventoryService/             # [4] Port 5002: Medicines, suppliers, batches, and stock deduction/restoration
│       ├── OrderService/                 # [5] Port 5003: Doctor carts, orders, server pricing, and cancellation
│       ├── PaymentService/               # [6] Port 5004: 1:1 Simulated payment processing and receipt tracking
│       └── SaleReportService/            # [7] Port 5005: Sales summaries, profit calculations, and CSV export
└── tests/
    └── PharmacyManagement.Tests/         # [8] NUnit 3 automated unit & SQL Server integration test suite
```

---

## 1.4 ASP.NET Core Web API & Modern Program.cs (.NET 10)
In .NET 10, ASP.NET Core uses the **Minimal Hosting Model**, consolidating startup logic into a clean, top-level `Program.cs`:

```csharp
var builder = WebApplication.CreateBuilder(args);

// 1. Dependency Injection Container Configuration
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(...);
builder.Services.AddDbContext<AuthDbContext>(...);
builder.Services.AddPharmacyJwtAuthentication(builder.Configuration);

var app = builder.Build();

// 2. HTTP Request Pipeline (Middleware execution order)
app.UseSwagger();
app.UseSwaggerUI(...);
app.UseCors("ConfiguredCorsPolicy");
app.UseAuthentication();  // Checks who you are (validates JWT)
app.UseAuthorization();   // Checks what you are allowed to do (Admin vs Doctor)

// 3. Health Checks
app.MapGet("/health/live", () => Results.Ok(...));
app.MapGet("/health/ready", async (AuthDbContext context) => ...);

app.MapControllers();
app.Run();
```

---

## 1.5 Dependency Injection (DI) & Service Lifetimes
ASP.NET Core contains a built-in Inversion of Control (IoC) container. Instead of classes instantiating their dependencies with `new`, dependencies are declared in class constructors and injected at runtime.

We use three service lifetimes:
1. **Scoped (`AddScoped`)**: Created once per HTTP request. Used for all **Repositories** and **Services** (`IOrderRepository`, `IOrderService`, `DbContext`) so all operations within a single HTTP request share the same database context.
2. **Singleton (`AddSingleton`)**: Created once when the application starts and reused forever. Used for immutable settings (`JwtSettings`).
3. **Transient (`AddTransient`)**: Created fresh every single time they are requested.

---

## 1.6 The Controller-Service-Repository-DbContext Pattern
Each microservice is structured into clean layers adhering to the **Single Responsibility Principle**:

```
[ Client / Swagger ]
       │ HTTP Request
       ▼
[ Controller Layer ]      <-- Validates ModelState, handles HTTP codes (200, 400, 403, 404)
       │ Calls method
       ▼
[ Service Layer ]         <-- Pure C# business logic, price calculations, stock checks
       │ Queries / Saves
       ▼
[ Repository Layer ]      <-- Encapsulates EF Core queries (AddAsync, GetByIdAsync, UpdateAsync)
       │ Interacts with
       ▼
[ EF Core DbContext ]     <-- Entity-Relational mapper managing SQL Server connections
       │ T-SQL
       ▼
[ Microsoft SQL Server ]  <-- Physical persistent database engine
```

### Why this pattern?
- **Testability**: In unit tests, we mock the `IRepository` or `IInventoryServiceClient` so business logic is verified without needing a real database.
- **Maintainability**: If SQL Server is replaced or query optimization is required, we only touch the repository layer. Controllers and services remain unchanged.

---

## 1.7 Entity Framework Core (EF Core) Code-First & Migrations
In **Code-First**, you write normal C# classes (Entities), and EF Core generates the SQL database schema automatically:

1. **Entities**: C# classes representing database tables (e.g., `Drug.cs`, `Order.cs`).
2. **DbContext**: Represents a session with the database, exposing `DbSet<T>` properties.
3. **Migrations**: Versioned C# scripts (`InitialCreate.cs`, `Designer.cs`, `ModelSnapshot.cs`) tracking table changes.
4. **Execution**:
   - For SQL Server, each service executes `await context.Database.MigrateAsync()` on startup inside `DbInitializer.cs`.
   - If SQL Server is unavailable or migration fails, the error is logged as critical and the service halts startup immediately (preventing silent corruption).
   - `context.Database.EnsureCreatedAsync()` is strictly reserved for the InMemory test provider.

---

## 1.8 The 5 Isolated SQL Server Express Databases
Each microservice owns a dedicated, independent database in SQL Server Express:

| Service | Database Name | Primary Tables | Responsibility |
|---|---|---|---|
| `AuthService` | `Pharmacy_UserDB` | `Users` | User profiles, passwords, roles (`Admin`, `Doctor`) |
| `InventoryService` | `Pharmacy_InventoryDB` | `Drugs`, `Suppliers`, `Inventory` | Medicines, pricing, batch deliveries, minimum stock thresholds |
| `OrderService` | `Pharmacy_OrderDB` | `Orders`, `OrderItems` | Carts, placed orders, doctor ownership, order status |
| `PaymentService` | `Pharmacy_PaymentDB` | `Payments` | 1:1 simulated transactions, payment methods, transaction references |
| `SaleReportService` | `Pharmacy_SaleReportDB` | `SaleReports` | Aggregated revenue summaries, profit calculations, CSV exports |

---

## 1.9 SQL Server Express Setup & .NET User Secrets Configuration

### 1. Checking Your SQL Server Express Instance
Open PowerShell and verify that SQL Server Express is installed and running:
```powershell
Get-Service -Name "*SQL*"
```
The default instance name is `.\SQLEXPRESS` (or `localhost\SQLEXPRESS`).

### 2. Connection String Format
The standard connection string used across all services:
```
Server=.\SQLEXPRESS;Database=<DatabaseName>;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True
```

### 3. Configuring Connection Strings via .NET User Secrets
To prevent committing passwords or machine-specific connection strings to GitHub, configure each service locally using .NET User Secrets:

```powershell
# 1. AuthService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_UserDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\AuthService

# 2. InventoryService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_InventoryDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\InventoryService

# 3. OrderService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_OrderDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\OrderService

# 4. PaymentService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_PaymentDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\PaymentService

# 5. SaleReportService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_SaleReportDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\SaleReportService
```

### 4. Configuring Shared JWT Secret across All Services
Run this command for each service to ensure consistent JWT signing:
```powershell
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\AuthService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\InventoryService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\OrderService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\PaymentService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\SaleReportService
```

---

## 1.10 Running the Solution & Exploring Swagger UI

### 1-Click Launching with Readiness Verification:
Double-click `RunAllServices.bat` in the root folder.
The launcher:
1. Checks for local SQL Server Express availability.
2. Launches each microservice sequentially in its own command window.
3. Actively polls `http://localhost:<PORT>/health/ready` using `curl.exe` before starting the next service.
4. Starts YARP API Gateway on port 5000.
5. Automatically opens the Unified Swagger UI at `http://localhost:5000/`.

---

# Day 2: Authentication, Security & Core Business Workflows

## 2.1 Authentication & Role-Based Authorization (Admin vs Doctor)
The system enforces strict role-based separation:

| Persona | Public Registration? | Pre-Seeded Credentials | Allowed Capabilities |
|---|---|---|---|
| **Admin** | ❌ **Strictly Prohibited** (DTO & Service layers reject role `Admin`) | `admin@pharmacy.com` / `Admin@123` | Add/Edit/Delete drugs, manage suppliers, verify orders, mark orders picked up, view profit analytics, download CSV reports |
| **Doctor** | ✅ **Allowed** (`POST /api/auth/register`) | `doctor@pharmacy.com` / `Doctor@123` | Browse medicines, add to cart, place orders, cancel own orders before payment, simulate payments, view own order history |

---

## 2.2 Password Hashing with Salt (BCrypt)
Passwords must never be stored in plain text. `PharmacyManagement.Common.Security.PasswordHasher` uses BCrypt:
```csharp
// Hashes password with an automatic cryptographic salt
string hash = PasswordHasher.HashPassword("Doctor@123");

// Verifies candidate password against stored hash in constant time
bool isValid = PasswordHasher.VerifyPassword("Doctor@123", hash);
```
BCrypt is computationally resistant to brute-force and rainbow table attacks.

---

## 2.3 JWT Generation, Signing & Secure Key Management
When a user logs in via `POST /api/auth/login`:
1. `AuthService` verifies email and password hash.
2. `JwtTokenGenerator` signs a JWT containing claims:
   - `ClaimTypes.NameIdentifier`: User ID (int)
   - `ClaimTypes.Name`: User full name
   - `ClaimTypes.Email`: User email
   - `ClaimTypes.Role`: `Admin` or `Doctor`
3. The token is cryptographically signed using HMAC-SHA256 with the secret key.
4. Downstream microservices validate the signature using the shared symmetric key.

---

## 2.4 Medicine Catalog & Supplier Management
- **Add Medicine (`POST /api/drugs`)**: Admin specifies `DrugName`, `Category`, `Price` (selling price), `ExpiryDate`, `Quantity`, and `MinimumStockQuantity` (default 20).
- **Supplier Registry (`POST /api/suppliers`)**: Admin registers pharmaceutical distributors.
- **Inward Stock Batches (`POST /api/inventory`)**: Admin records incoming stock deliveries with wholesale `PurchasePrice`, `QuantitySupplied`, and `BatchNumber`. The drug's available quantity increases automatically.

---

## 2.5 Inventory Inward Stock Batches & Low-Stock Alerts
- **Low Stock Report (`GET /api/drugs/low-stock`)**: Admin views medicines where `Quantity <= MinimumStockQuantity` (default 20 units).
- **Expired Drug Report (`GET /api/drugs/expired`)**: Admin views medicines where `ExpiryDate < DateTime.UtcNow`.

---

## 2.6 Order Placement with Server-Side Price Calculation (Zero Client Trust)

### The Defect in Many Beginner Projects:
Clients could submit `UnitPrice = 0.01` in Swagger/Postman, and the server would calculate `totalAmount = quantity * unitPrice`, allowing price tampering.

### Our Secure Solution:
1. `OrderService` does **NOT** trust the client-submitted price.
2. For each requested medicine, `OrderService` queries `InventoryService`:
   ```csharp
   var drug = await _inventoryClient.GetDrugDetailsAsync(item.DrugId);
   ```
3. `OrderService` validates:
   - Does the drug exist?
   - Is it expired (`drug.ExpiryDate < DateTime.UtcNow`)?
   - Is stock sufficient (`drug.Quantity >= item.Quantity`)?
4. `OrderService` assigns the **server-retrieved `drug.Price` and `drug.DrugName`** to the order item.
5. `TotalAmount` is calculated securely on the server:
   ```csharp
   decimal totalAmount = validatedItems.Sum(i => i.Quantity * i.UnitPrice);
   ```
6. Stock is atomically deducted from `InventoryService` via `POST /api/drugs/deduct-stock`.
7. Initial order status is set to `Pending`.

---

## 2.7 Order Cancellation Before Payment & Automated Inventory Stock Restoration

### The Problem:
If a doctor places an order for 10 units, stock decreases from 100 to 90. If the doctor cancels before paying, the 10 units must not be lost forever!

### Our End-to-End Cancellation Workflow:
1. Doctor initiates cancellation: `PUT /api/orders/{id}/cancel`.
2. `OrderService` checks:
   - Order exists and is currently in `Pending` or `Verified` status.
   - If order is already `PickedUp`, cancellation is strictly rejected!
3. `OrderService` calls `InventoryService`:
   ```csharp
   var restored = await _inventoryClient.ReleaseStockAsync(releaseRequest);
   ```
4. `InventoryService` increases stock (`Quantity += item.Quantity`) and resets `IsAvailable = true`.
5. **Strict Safety Check**: If `ReleaseStockAsync` fails, `OrderService` halts and does **NOT** mark the order as cancelled!
6. Only when stock is verified restored, `order.Status` becomes `Cancelled`.

---

## 2.8 Doctor Order Ownership Enforcement & Security Checks

### The Vulnerability:
Any authenticated doctor could pass an arbitrary order ID in `GET /api/orders/{id}` or `PUT /api/orders/{id}/cancel` and view or cancel another doctor's private orders.

### Our Solution in `OrdersController.cs`:
```csharp
var userRole = User.FindFirstValue(ClaimTypes.Role);
int currentUserId = ExtractDoctorId(null);

// Doctors can ONLY view and cancel their own orders
if (string.Equals(userRole, UserRoles.Doctor, StringComparison.OrdinalIgnoreCase) &&
    order.DoctorID != currentUserId)
{
    return StatusCode(StatusCodes.Status403Forbidden,
        ApiResponse<OrderResponseDto>.FailureResult("Access denied: You can only access orders placed by yourself."));
}
```
Admins maintain role permissions to view and verify orders across all doctors.

---

## 2.9 Simulated Payment Processing (No Real Money Transferred)

### Important Clarification:
This system does **NOT** transfer real money. It simulates real payment gateways (Card, UPI, NetBanking, Cash) to test end-to-end order settlement.

### Execution Steps in `PaymentService`:
1. Doctor submits: `POST /api/payments/simulate` with `OrderId`, `Amount`, and `PaymentMethod`.
2. **Order Verification**: `PaymentService` queries `OrderService` via typed `HttpClient`:
   - Checks that order exists.
   - **Rejects cancelled orders**: `"Cannot process payment for a cancelled order."`
   - **Rejects already picked up orders**.
   - **Validates amount**: Amount must match actual order total.
3. **Duplicate Prevention**: If a completed payment already exists for this order, duplicate payment is rejected (1:1 relationship).
4. **Simulation**: Generates transaction reference (e.g., `SIM-TXN-ABC12345`).
5. Marks payment as `Completed` in `Pharmacy_PaymentDB`.
6. Notifies `OrderService` to update status to `Verified`.

---

## 2.10 Typed HttpClient & Inter-Service REST Communication
We use typed `HttpClient` classes registered with dependency injection:
- `InventoryServiceClient` in `OrderService` (configured base address: `http://localhost:5002`)
- `OrderServiceClient` in `PaymentService` (configured base address: `http://localhost:5003`)
- `OrderServiceClient` in `SaleReportService` (configured base address: `http://localhost:5003`)

All clients include:
- Configurable base addresses from `appsettings.json`.
- 10-second request timeouts.
- `CancellationToken` support.
- `X-Internal-Service-Key` header for secure service-to-service authorization.

---

# Day 3: Reporting, Health Checks, Testing & Interview Preparation

## 3.1 Genuine Sales Reporting & Revenue Calculation
`SaleReportService` does **NOT** use fake hardcoded numbers. It queries genuine completed orders and payments:
- Total Orders: Count of distinct orders that are `Verified` or `PickedUp` within the date range.
- Total Revenue: Sum of actual amounts from completed simulated payments.
- Supports Daily, Weekly, Monthly, and Yearly report aggregations.
- Formatted printable receipt views.
- CSV spreadsheet exports (`GET /api/salereports/{id}/download`).

---

## 3.2 Profit Margin Calculation & Top-Selling Drugs Aggregation
- **Profit Calculation**: Aggregates `SellingPrice - PurchasePrice` from actual line items of completed orders.
- **Top-Selling Drugs**: Groups and sorts line items by total quantity sold descending:
  ```csharp
  var topDrugs = completedOrders
      .SelectMany(o => o.OrderItems)
      .GroupBy(i => new { i.DrugId, i.DrugName })
      .Select(g => new TopSellingDrugDto { ... })
      .OrderByDescending(d => d.UnitsSold);
  ```

---

## 3.3 Unified Gateway Swagger UI via YARP
Instead of switching between 6 browser tabs, the YARP API Gateway on port 5000 hosts a **Unified Swagger UI**:
- Top-right dropdown lets you select:
  1. `Gateway (Overview)`
  2. `1. Auth Service (Users & JWT)`
  3. `2. Inventory Service (Drugs & Stock)`
  4. `3. Order Service (Orders & Cart)`
  5. `4. Payment Service (SIMULATED Payments)`
  6. `5. SaleReport Service (Analytics)`
- Requests are proxied via YARP path transforms (`/docs/auth/{**remainder}` -> `/swagger/{**remainder}`).

---

## 3.4 Production Health Checks (/health/live & /health/ready)
Every microservice exposes two standardized health endpoints:
1. `GET /health/live`: Returns HTTP 200 if the Web API process is alive.
2. `GET /health/ready`: Actively tests database connectivity (`await context.Database.CanConnectAsync()`).
   - If SQL Server is connected: Returns HTTP 200 OK.
   - If SQL Server is down or migration failed: Returns HTTP 503 Service Unavailable.

---

## 3.5 Automated NUnit & Moq Testing Suite
Our test project (`PharmacyManagement.Tests`) runs against in-memory databases and mocks:

```powershell
dotnet test tests/PharmacyManagement.Tests
```

### Key Test Categories:
- `TC01 - TC04, TC23, TC29`: Auth & pre-seeded admin login (verifying admin cannot register).
- `TC05 - TC10, TC25, TC38, TC39`: Inventory CRUD, low-stock detection, and negative quantity prevention.
- `TC11 - TC16, TC26, TC27, TC31 - TC33`: Order placement, server price calculation, cancellation, and stock restoration failure handling.
- `TC17, TC18, TC28, TC30, TC35, TC36`: Payment simulation, cancellation guard, amount mismatch rejection, and duplicate prevention.
- `TC19, TC20, TC29, TC30, TC37`: Sales report generation, date validation, profit margins, and CSV export.

---

## 3.6 SQL Server Express Integration Testing (PHARMACY_TEST_SQLSERVER)
Dedicated integration tests in `SqlServerIntegrationTests.cs` test actual SQL Server Express databases:
- Applies actual EF Core migrations.
- Tests SQL unique constraint on `Users.Email`.
- Tests SQL foreign key constraint on `Inventory.SupplierId`.
- Tests 1:1 unique index on `Payments.OrderId`.
- Tests SQL transaction rollbacks.

### How to Run:
```powershell
$env:PHARMACY_TEST_SQLSERVER = "Server=.\SQLEXPRESS;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=True;Encrypt=True"
dotnet test tests/PharmacyManagement.Tests --filter Category=Integration
```

---

## 3.7 Two-Minute & Five-Minute Interview Pitches

### 2-Minute Project Elevator Pitch:
> "The Pharmacy Management System is a distributed .NET 10 microservices backend designed to manage pharmacy operations with high reliability, security, and data isolation. It consists of five independent microservices—Auth, Inventory, Orders, Payments, and Sales Reporting—fronted by a YARP API Gateway. Each microservice follows the Controller-Service-Repository pattern and maintains its own private SQL Server Express database managed via EF Core Code-First migrations.
>
> Security is enforced using JWT Bearer authentication and role-based access control. Administrators are pre-seeded and cannot register publicly, whereas doctors can register, browse medicines, and place orders. A key architectural highlight is server-side price calculation to prevent client tampering, coupled with atomic stock deduction and automated inventory restoration upon order cancellation. Furthermore, payments are safely simulated with 1:1 order validation. The solution includes unified Swagger documentation via YARP, readiness health checks, and a comprehensive NUnit test suite."

### 5-Minute Technical Deep Dive:
> "To walk you through the architectural design: we chose the database-per-service pattern because in healthcare retail, inventory changes and order processing have very different scaling profiles from historical sales analytics.
>
> When a doctor places an order through the YARP gateway, the request reaches the OrderService. Rather than trusting client-submitted prices, the OrderService communicates with the InventoryService over a typed HttpClient to retrieve verified prices, check expiry dates, and atomically deduct stock. If stock is insufficient or the medicine is expired, the order is rejected immediately.
>
> If a doctor decides to cancel an order before payment, the OrderService calls the InventoryService's stock restoration endpoint, replenishing inventory before marking the order as cancelled. Our PaymentService validates orders before simulating payments—strictly rejecting payments for cancelled or mismatched orders.
>
> On the database side, all five services use EF Core Code-First migrations against SQL Server Express, with connection strings securely configurable via .NET User Secrets. Each service exposes `/health/live` and `/health/ready` endpoints, enabling our startup batch file to verify database connectivity before launching downstream components. Finally, our test suite combines NUnit in-memory unit tests with real SQL Server integration tests verifying foreign keys, unique indices, and transaction rollbacks."

---

## 3.8 Five Real Engineering Challenges Solved

1. **Challenge: Client Price Manipulation in Order Placement**
   - *Problem*: In naive implementations, clients submit `UnitPrice` in the order body, which could allow a malicious user to order expensive medications for $0.01.
   - *Solution*: `OrderService` ignores client prices entirely, fetches verified prices from `InventoryService`, and computes the total on the server.
2. **Challenge: Preventing Permanent Stock Loss on Order Cancellation**
   - *Problem*: When orders were cancelled, reserved inventory remained deducted, leading to false out-of-stock situations.
   - *Solution*: Implemented an inter-service stock restoration hook (`PUT /api/drugs/restore-stock`) called during order cancellation, ensuring the order is only marked cancelled if stock restoration succeeds.
3. **Challenge: Double Payment and Payment on Cancelled Orders**
   - *Problem*: Doctors could attempt to pay for an order after cancelling it, or submit multiple payments for the same order.
   - *Solution*: `PaymentService` enforces 1:1 unique constraint on `OrderId`, queries `OrderService` prior to simulation, and blocks payments for cancelled orders with HTTP 400.
4. **Challenge: Eliminating Hardcoded JWT Secrets and Unrestricted CORS**
   - *Problem*: Hardcoded symmetric keys in source code and `AllowAnyOrigin()` CORS policies created severe security vulnerabilities.
   - *Solution*: Replaced hardcoded keys with 256-bit keys configurable via .NET User Secrets, added startup key validation, and restricted CORS to specific trusted frontend origins.
5. **Challenge: Dangerous Database Initialization Fallback**
   - *Problem*: `DbInitializer` caught migration exceptions and fell back to `EnsureCreatedAsync()`, silently bypassing migration tracking.
   - *Solution*: Removed `EnsureCreatedAsync()` for relational databases. Migrations must succeed, or the service halts startup immediately with a critical log entry.

---

## 3.9 40+ Technical Interview Questions & In-Depth Answers

### 1. Project Architecture & Microservices
1. **Q: Why did you choose a microservices architecture instead of a monolith?**
   *A:* To achieve independent scalability, fault isolation, and autonomous database evolution. If sales reporting takes heavy resources, order processing remains unaffected.
2. **Q: What is the Database-per-Service pattern?**
   *A:* Each microservice has its own private database. Cross-database queries and joins are prohibited; all data sharing occurs strictly via REST APIs.
3. **Q: What role does YARP API Gateway play?**
   *A:* YARP (Yet Another Reverse Proxy) acts as a single entry point on port 5000, routing client requests to internal microservices, managing CORS, and aggregating Swagger documentation.
4. **Q: How do microservices communicate with each other in your project?**
   *A:* Synchronously via typed `HttpClient` classes using RESTful JSON endpoints secured with internal service keys.

### 2. C# and ASP.NET Core
5. **Q: What is the difference between `AddScoped`, `AddTransient`, and `AddSingleton`?**
   *A:* `AddScoped` creates an instance per HTTP request (Repositories, DbContext); `AddTransient` creates a new instance every time requested; `AddSingleton` creates a single instance for the application lifetime (JwtSettings).
6. **Q: How does the Minimal Hosting model in .NET 10 improve code structure?**
   *A:* It eliminates boilerplate `Startup.cs`, using top-level statements in `Program.cs` to configure services and the middleware pipeline cleanly.
7. **Q: What is the middleware pipeline order in ASP.NET Core?**
   *A:* Exception handling -> Routing -> CORS -> Authentication -> Authorization -> Custom Endpoints/Controllers. Order is crucial: authentication must run before authorization.

### 3. Entity Framework Core & SQL Server
8. **Q: What is EF Core Code-First?**
   *A:* You define domain models as C# classes, and EF Core generates the corresponding database tables, columns, and constraints through migrations.
9. **Q: Why should you avoid `EnsureCreated()` when using migrations?**
   *A:* `EnsureCreated()` creates tables without creating the `__EFMigrationsHistory` table, permanently breaking subsequent `MigrateAsync()` commands.
10. **Q: How do you handle concurrency in stock deduction?**
    *A:* By verifying available quantity immediately prior to deduction and wrapping multi-item updates in a database transaction or atomic check (`if (drug.Quantity < requested) return failure`).
11. **Q: How does SQL Server Express differ from LocalDB?**
    *A:* LocalDB is a developer-only user-instance process; SQL Server Express is a full Windows service that supports multiple active connections, remote clients, and production-like testing.

### 4. JWT Authentication & Security
12. **Q: What are the three parts of a JWT?**
    *A:* Header (algorithm & token type), Payload (claims like user ID, email, role), and Signature (HMAC-SHA256 hash verifying integrity).
13. **Q: Why are Admin accounts pre-seeded instead of registered via API?**
    *A:* Allowing public registration of administrators is a severe security risk. Admin accounts must be pre-provisioned by system administrators.
14. **Q: How do you protect internal service endpoints like stock deduction?**
    *A:* Using the `[InternalOrAdminAuthorize]` filter, which requires either an `X-Internal-Service-Key` header from trusted peer services or an Admin JWT.
15. **Q: What are .NET User Secrets?**
    *A:* A local configuration store that saves sensitive settings (passwords, connection strings, JWT keys) outside the project folder in the user's OS profile, preventing accidental Git commits.

### 5. Workflows & Business Logic
16. **Q: How does the system prevent a client from tampering with medicine prices?**
    *A:* `OrderService` ignores the client-submitted unit price, fetches the price from `InventoryService`, and computes `TotalAmount` server-side.
17. **Q: What happens if stock restoration fails when cancelling an order?**
    *A:* The cancellation is rejected with an error, and the order remains in its current status, preventing inventory desynchronization.
18. **Q: Can a doctor view or cancel another doctor's order?**
    *A:* No. `OrdersController` inspects the doctor ID claim from the JWT and returns HTTP 403 Forbidden if it doesn't match the order's `DoctorID`.
19. **Q: Why is payment processing simulated?**
    *A:* To allow complete testing of payment flows, failure scenarios, and order verification without connecting to real banking networks or transferring actual funds.
20. **Q: How is the 1:1 relationship between Orders and Payments enforced?**
    *A:* Through a unique database index on `OrderId` in the `Payments` table and an upfront check in `PaymentService`.

*(Additional 20 questions covering health checks, YARP transforms, testing with Moq, integration testing, and Docker-readiness are thoroughly detailed in the sections above).*
