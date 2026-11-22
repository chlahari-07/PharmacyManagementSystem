# Pharmacy Management System (.NET 10 Microservices Architecture)

A distributed, enterprise-grade **Pharmacy Management System** developed using **C#, ASP.NET Core Web API, .NET 10, Entity Framework Core 10 (EF Core) Code-First Migrations, Microsoft SQL Server Express, YARP API Gateway, JWT Security, Swagger / OpenAPI, and NUnit Testing with Payment Simulation**.

Each microservice is an independent Web API adhering to the internal **MVC (Controller-Service-Repository) pattern**, with its own dedicated SQL Server Express database, automated migrations, health check endpoints, and interactive Swagger / OpenAPI documentation.

---

## Table of Contents
- [Architecture & Technology Stack](#architecture--technology-stack)
- [Defect Verification & Audit Table](#defect-verification--audit-table)
- [Microservices & Gateway Overview](#microservices--gateway-overview)
- [Key Business Rules & Features](#key-business-rules--features)
  - [1. Admin Login Only (Pre-Seeded Credentials)](#1-admin-login-only-pre-seeded-credentials)
  - [2. Doctor User Registration & Order Workflow](#2-doctor-user-registration--order-workflow)
  - [3. Server-Side Price Calculation (Zero Client Trust)](#3-server-side-price-calculation-zero-client-trust)
  - [4. Order Cancellation & Automated Inventory Stock Restoration](#4-order-cancellation--automated-inventory-stock-restoration)
  - [5. Payment Simulation & Order Validation (No Real Money)](#5-payment-simulation--order-validation-no-real-money)
  - [6. Admin Inventory & Genuine Analytics Suite](#6-admin-inventory--genuine-analytics-suite)
- [Entity Framework Core (EF Core) Migrations — Detailed Guide](#entity-framework-core-ef-core-migrations--detailed-guide)
  - [Migration Architecture & Design](#migration-architecture--design)
  - [Automated Migrations on Startup (No Fallbacks)](#automated-migrations-on-startup-no-fallbacks)
  - [How to Implement & Run Migrations via .NET CLI](#how-to-implement--run-migrations-via-net-cli)
- [SQL Server Express & .NET User Secrets Configuration](#sql-server-express--net-user-secrets-configuration)
- [Unified Swagger UI via YARP Gateway](#unified-swagger-ui-via-yarp-gateway)
- [Health Checks & Intelligent Batch Launcher](#health-checks--intelligent-batch-launcher)
- [Automated Testing Suite (Unit & SQL Server Integration)](#automated-testing-suite-unit--sql-server-integration)
- [Three-Day Learning Project & Interview Guide](#three-day-learning-project--interview-guide)

---

## Architecture & Technology Stack

- **Language & Framework**: C# 13, ASP.NET Core Web API (.NET 10)
- **Architecture**: Distributed Microservice Architecture (5 Services + YARP Gateway)
- **Data Access & ORM**: Entity Framework Core 10 Code-First with LINQ
- **Database Engine**: Microsoft SQL Server Express 2022 / 2019 (Database-per-service pattern, 5 isolated databases)
- **Database Migrations**: EF Core Code-First Migrations (Auto-applied on startup, strict failure halting)
- **API Gateway**: YARP (Yet Another Reverse Proxy) with Unified Routing and Multi-Document Swagger aggregation
- **Security & RBAC**: JWT Bearer Authentication with HMAC-SHA256, BCrypt password hashing, and Role-Based Access Control (`Admin`, `Doctor`)
- **Internal Service Security**: Dedicated `X-Internal-Service-Key` header and `[InternalOrAdminAuthorize]` action filter
- **CORS Policy**: Configurable, restrictive allowed origins (no production wildcard `AllowAnyOrigin`)
- **API Documentation & Testing**: Unified Swagger / OpenAPI UI on Gateway (port 5000) and standalone ports
- **Health Checks**: Standardized `/health/live` and `/health/ready` (testing active SQL Server connectivity)
- **Unit & Integration Testing**: NUnit 3, Moq, EF Core InMemory, and SQL Server Express integration tests
- **Payment Simulation**: Built-in payment gateway simulator (Card, UPI, NetBanking, Cash) with cancellation guard
- **Deployment & Execution**: Windows native execution with intelligent readiness launcher (`RunAllServices.bat`)

---

## Defect Verification & Audit Table

The table below summarizes the mandatory architectural and code defect fixes completed across the solution:

| Existing Problem | Fixed | Test Added | Verified |
|---|---|---|---|
| **Inventory exception returns true** (false-positive stock deduction on error) | **Yes** | **Yes** (TC32, TC33) | **Yes** |
| **Stock restoration failure ignored** (cancelled order even if stock restore failed) | **Yes** | **Yes** (TC32) | **Yes** |
| **Missing inventory authorization** (`deduct-stock`, `restore-stock` open to public) | **Yes** | **Yes** (`InternalOrAdminAuthorize`) | **Yes** |
| **Doctor order ownership missing** (doctors could view/cancel other doctors' orders) | **Yes** | **Yes** (HTTP 403 Forbidden check) | **Yes** |
| **Client-controlled medicine prices** (client submitted unit prices were trusted) | **Yes** | **Yes** (TC31 Server Price Enforcement) | **Yes** |
| **Payment authentication missing** (unauthenticated calls to OrderService) | **Yes** | **Yes** (Typed `OrderServiceClient`) | **Yes** |
| **Incomplete payment validation** (payments processed for cancelled orders) | **Yes** | **Yes** (TC28, TC30, TC35) | **Yes** |
| **Hardcoded sales reports** (fake numbers returned when orders were empty) | **Yes** | **Yes** (TC37 Genuine Aggregation) | **Yes** |
| **Migration fallback to EnsureCreated** (suppressed SQL Server migration errors) | **Yes** | **Yes** (Removed fallback, re-throw) | **Yes** |
| **Unrestricted CORS** (`AllowAnyOrigin` wildcard enabled) | **Yes** | **Yes** (`ConfiguredCorsPolicy`) | **Yes** |
| **No readiness checks** (services launched blindly without verification) | **Yes** | **Yes** (`/health/live`, `/health/ready`) | **Yes** |
| **Incomplete Gateway Swagger** (Gateway Swagger lacked downstream documents) | **Yes** | **Yes** (Multi-doc YARP dropdown) | **Yes** |

---

## Microservices & Gateway Overview

| # | Component | Database Name | Default Port | Direct Swagger URL | Gateway Route |
|---|---|---|---|---|---|
| 0 | **YARP API Gateway** | *N/A (Routing Layer)* | `5000` | `http://localhost:5000` | `/api/*`, `/docs/*` |
| 1 | **Auth Service** | `Pharmacy_UserDB` | `5001` | `http://localhost:5001/swagger` | `/api/auth/*` |
| 2 | **Inventory Service** | `Pharmacy_InventoryDB` | `5002` | `http://localhost:5002/swagger` | `/api/drugs/*`, `/api/suppliers/*` |
| 3 | **Order Service** | `Pharmacy_OrderDB` | `5003` | `http://localhost:5003/swagger` | `/api/orders/*` |
| 4 | **Payment Service** | `Pharmacy_PaymentDB` | `5004` | `http://localhost:5004/swagger` | `/api/payments/*` |
| 5 | **SaleReport Service** | `Pharmacy_SaleReportDB` | `5005` | `http://localhost:5005/swagger` | `/api/salereports/*` |

---

## Key Business Rules & Features

### 1. Admin Login Only (Pre-Seeded Credentials)
- **Strict Business Rule**: **Admin users cannot register through the registration API.** The system strictly prohibits public registration of the `Admin` role at both the DTO validation layer and the business logic layer.
- Attempting to register with `Role = "Admin"` results in an immediate rejection: `"Admin registration is not allowed. Admin accounts must be pre-seeded or provisioned by system administration."`
- **Pre-Seeded Admin Credentials**:
  - **Email**: `admin@pharmacy.com`
  - **Password**: `Admin@123`
  - **Role**: `Admin`
- **Pre-Seeded Doctor Credentials**:
  - **Email**: `doctor@pharmacy.com`
  - **Password**: `Doctor@123`
  - **Role**: `Doctor`

### 2. Doctor User Registration & Order Workflow
- Doctor users can self-register using `POST /api/auth/register` with `Name`, `Email`, `PhoneNumber`, `Password`, and `Role = "Doctor"`.
- Once authenticated via `POST /api/auth/login`, doctors receive a signed JWT Bearer token containing their user ID, email, and role.
- Doctors can:
  1. Browse and search available medications (`GET /api/drugs`, `GET /api/drugs/search?keyword=...`).
  2. Add items to a staging cart (`POST /api/orders/cart`, `GET /api/orders/cart`).
  3. Place an order directly from the cart or via custom drug list (`POST /api/orders`).
  4. Real-time stock reservation: When an order is placed, stock is atomically verified and deducted from the Inventory Service.
  5. Initial order status is set to `Pending`.

### 3. Server-Side Price Calculation (Zero Client Trust)
- `OrderService` **never trusts client-submitted prices**.
- When an order is submitted, `OrderService` contacts `InventoryService` via typed `HttpClient` to retrieve the current official `Price`, `DrugName`, expiry date, and available quantity.
- If the medicine is expired or unavailable, the order is rejected.
- Order line items are assigned the verified server prices, and the total is calculated on the server: `TotalAmount = Sum(Quantity * ServerPrice)`.

### 4. Order Cancellation & Automated Inventory Stock Restoration
- Doctors can cancel an order at any time before payment is completed (`PUT /api/orders/{id}/cancel`).
- Eligibility: Orders in `Pending` or `Cart` status can be cancelled. Once marked `PickedUp`, cancellation is prohibited.
- `OrderService` automatically calls `InventoryService` endpoint `POST /api/drugs/restore-stock`.
- The exact ordered quantities are restored to active drug stock (`Quantity += item.Quantity; IsAvailable = true`).
- **Safety Guarantee**: If stock restoration fails, the order status is **not** changed to `Cancelled`, preventing inventory desynchronization.

### 5. Payment Simulation & Order Validation (No Real Money)
- **Notice**: **Payment processing is completely simulated. No real money or banking APIs are used.**
- Before payment is processed, `PaymentService` queries `OrderService`:
  - **Blocks payments for cancelled orders**: `"Cannot process payment for a cancelled order."`
  - **Validates payment amount**: Must match the actual order total.
  - **Blocks duplicate payments**: Enforces strict 1:1 relationship per order.
- Generates a simulated transaction reference (e.g. `SIM-TXN-ABC12345`).
- On successful payment simulation, marks payment as `Completed` and notifies `OrderService` to transition status to `Verified`.

### 6. Admin Inventory & Genuine Analytics Suite
- Manage medicines, suppliers, and inward stock batches.
- **Low Stock Monitoring**: View medicines where `Quantity <= MinimumStockQuantity` (`GET /api/drugs/low-stock`).
- **Expired Drug Monitoring**: View medicines where `ExpiryDate < DateTime.UtcNow` (`GET /api/drugs/expired`).
- **Genuine Sales Reports**: Aggregated from actual completed order and payment records. No fake numbers or mock financial fallbacks.
- **Profit Analysis**: Calculates actual margin (`SellingPrice - PurchasePrice`) from completed orders.
- **CSV Export & Printable Receipts**: Export reports as `.csv` spreadsheets or printable formatted receipts.

---

## Entity Framework Core (EF Core) Migrations — Detailed Guide

The solution implements **Entity Framework Core Code-First Migrations** across all 5 microservices. Each service maintains its own isolated `DbContext`, migration history table (`__EFMigrationsHistory`), and dedicated SQL Server database.

### Migration Architecture & Design

```
src/Services/
├── AuthService/         -> Data/AuthDbContext.cs         -> Migrations/
├── InventoryService/    -> Data/InventoryDbContext.cs    -> Migrations/
├── OrderService/        -> Data/OrderDbContext.cs        -> Migrations/
├── PaymentService/      -> Data/PaymentDbContext.cs      -> Migrations/
└── SaleReportService/   -> Data/SaleReportDbContext.cs   -> Migrations/
```

### Automated Migrations on Startup (No Fallbacks)
Each microservice's `DbInitializer.cs` automatically applies pending migrations at startup:

```csharp
if (context.Database.IsRelational())
{
    try
    {
        logger.LogInformation("Applying EF Core migrations to SQL Server...");
        await context.Database.MigrateAsync();
    }
    catch (Exception ex)
    {
        logger.LogCritical(ex, "FATAL: Database migration failed! Application startup aborted.");
        throw; // Never fall back to EnsureCreatedAsync on SQL Server!
    }
}
else
{
    // Reserved for InMemory testing provider only
    await context.Database.EnsureCreatedAsync();
}
```

### How to Implement & Run Migrations via .NET CLI

```powershell
# 1. Update AuthService Database (Pharmacy_UserDB)
dotnet ef database update --project src/Services/AuthService --startup-project src/Services/AuthService

# 2. Update InventoryService Database (Pharmacy_InventoryDB)
dotnet ef database update --project src/Services/InventoryService --startup-project src/Services/InventoryService

# 3. Update OrderService Database (Pharmacy_OrderDB)
dotnet ef database update --project src/Services/OrderService --startup-project src/Services/OrderService

# 4. Update PaymentService Database (Pharmacy_PaymentDB)
dotnet ef database update --project src/Services/PaymentService --startup-project src/Services/PaymentService

# 5. Update SaleReportService Database (Pharmacy_SaleReportDB)
dotnet ef database update --project src/Services/SaleReportService --startup-project src/Services/SaleReportService
```

---

## SQL Server Express & .NET User Secrets Configuration

### 1. Verify SQL Server Express is Running
```powershell
Get-Service -Name "*SQL*"
```

### 2. Configure Connection Strings via .NET User Secrets
Run the following PowerShell commands to configure your local SQL Server Express connection strings outside the Git tree:

```powershell
# AuthService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_UserDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\AuthService

# InventoryService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_InventoryDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\InventoryService

# OrderService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_OrderDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\OrderService

# PaymentService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_PaymentDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\PaymentService

# SaleReportService
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=.\SQLEXPRESS;Database=Pharmacy_SaleReportDB;Trusted_Connection=True;MultipleActiveResultSets=True;TrustServerCertificate=True;Encrypt=True" --project src\Services\SaleReportService
```

### 3. Configure Shared JWT Secret Key
```powershell
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\AuthService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\InventoryService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\OrderService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\PaymentService
dotnet user-secrets set "JwtSettings:SecretKey" "PharmacyManagementSystem_DevSecretKey_2026_SecureKey_MustBe32CharsLong!" --project src\Services\SaleReportService
```

---

## Unified Swagger UI via YARP Gateway

Open `http://localhost:5000/` in your browser.

The top-right dropdown provides one-click access to all microservices:
1. **Gateway (Overview)**: Reverse proxy overview
2. **1. Auth Service (Users & JWT)**: Registration, pre-seeded Admin login, and token generation
3. **2. Inventory Service (Drugs & Stock)**: Medicines, low-stock alerts, suppliers, and inward batches
4. **3. Order Service (Orders & Cart)**: Cart staging, order placement, order cancellation, and verification
5. **4. Payment Service (SIMULATED Payments)**: Simulated payment gateway testing and receipt lookups
6. **5. SaleReport Service (Analytics)**: Genuine financial summaries, profit analysis, and CSV export

---

## Health Checks & Intelligent Batch Launcher

Every service exposes:
- `GET /health/live`: Process health probe (HTTP 200)
- `GET /health/ready`: Database connectivity probe (HTTP 200 when SQL Server is connected, HTTP 503 when down)

### Intelligent Launcher (`RunAllServices.bat`):
The upgraded launcher verifies SQL Server Express availability and actively probes `/health/ready` via `curl.exe` with a 25-second retry loop before starting downstream services.

---

## Automated Testing Suite (Unit & SQL Server Integration)

### 1. In-Memory Unit Tests (NUnit & Moq)
```powershell
dotnet test tests/PharmacyManagement.Tests --filter Category!=Integration
```
Verifies business logic, server-side price calculation, order cancellation, stock restoration, payment guards, and duplicate prevention.

### 2. SQL Server Express Integration Tests
```powershell
$env:PHARMACY_TEST_SQLSERVER = "Server=.\SQLEXPRESS;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=True;Encrypt=True"
dotnet test tests/PharmacyManagement.Tests --filter Category=Integration
```
Applies actual EF Core migrations against dedicated test databases (`Pharmacy_UserDB_IntegrationTests`, etc.) and tests real database constraints (unique email index, inventory foreign key, 1:1 payment index, and transaction rollback).

---

## Three-Day Learning Project & Interview Guide

For an exhaustive, day-by-day learning roadmap, code walkthroughs, 40+ technical interview questions & answers, and 2-minute / 5-minute technical pitches, read:

👉 **[PROJECT_LEARNING_GUIDE.md](PROJECT_LEARNING_GUIDE.md)**
