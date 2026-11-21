# Pharmacy Management System (.NET Microservices Architecture)

A distributed, enterprise-grade **Pharmacy Management System** developed using **C#, ASP.NET Core Web API, .NET 10 / .NET 8, Entity Framework Core (EF Core) Code-First Migrations, Microsoft SQL Server, YARP API Gateway, JWT Security, Swagger / OpenAPI, and NUnit Testing with Payment Simulation**.

Each microservice is an independent Web API adhering to the internal **MVC (Controller-Service-Repository) pattern**, with its own dedicated SQL Server database, automated migrations, and interactive Swagger / OpenAPI documentation.

---

## Table of Contents
- [Architecture & Technology Stack](#architecture--technology-stack)
- [Microservices & Gateway Overview](#microservices--gateway-overview)
- [Key Business Rules & Features](#key-business-rules--features)
  - [1. Admin Login Only (Pre-Seeded Credentials)](#1-admin-login-only-pre-seeded-credentials)
  - [2. Doctor User Registration & Order Workflow](#2-doctor-user-registration--order-workflow)
  - [3. Order Cancellation Before Payment & Stock Restoration](#3-order-cancellation-before-payment--stock-restoration)
  - [4. Payment Simulation & Validation](#4-payment-simulation--validation)
  - [5. Admin Inventory & Analytics Suite](#5-admin-inventory--analytics-suite)
- [Entity Framework Core (EF Core) Migrations — Detailed Guide](#entity-framework-core-ef-core-migrations--detailed-guide)
  - [Migration Architecture & Design](#migration-architecture--design)
  - [Automated Migrations on Startup](#automated-migrations-on-startup)
  - [How to Implement & Run Migrations via .NET CLI](#how-to-implement--run-migrations-via-net-cli)
  - [Generating SQL Scripts for Production / CI/CD](#generating-sql-scripts-for-production--cicd)
  - [Database Connection String Configuration](#database-connection-string-configuration)
- [Database Schemas & Data Dictionary](#database-schemas--data-dictionary)
- [Complete API Catalogue](#complete-api-catalogue)
- [Swagger UI Interactive Testing Guide](#swagger-ui-interactive-testing-guide)
- [How to Run the Application](#how-to-run-the-application)
- [Automated NUnit Testing Suite (30 Test Cases)](#automated-nunit-testing-suite-30-test-cases)
- [Project Structure & Documentation](#project-structure--documentation)

---

## Architecture & Technology Stack

- **Language & Framework**: C#, ASP.NET Core Web API (.NET 10 / .NET 8)
- **Architecture**: Distributed Microservice Architecture (5 Services + YARP Gateway)
- **Data Access & ORM**: Entity Framework Core (EF Core) Code-First with LINQ
- **Database Migrations**: EF Core Code-First Migrations (Auto-applied on startup + CLI-managed)
- **Database Engine**: Microsoft SQL Server 2022 (Database-per-service pattern, 5 isolated databases)
- **API Gateway**: YARP (Yet Another Reverse Proxy) with Unified Routing and path-based forwarding
- **Security & RBAC**: JWT (JSON Web Tokens) Bearer Authentication with Role-Based Access Control (`Admin`, `Doctor`)
- **API Documentation & Testing**: Swagger / OpenAPI UI on all services and gateway
- **Unit Testing**: NUnit 3 Test Suite (30 test cases: TC-01 to TC-30) with Moq and InMemory DbContext
- **Payment Simulation**: Built-in payment gateway simulator (Card, UPI, NetBanking, Cash) with cancellation protection
- **Deployment & Execution**: Direct native execution on Windows via .NET CLI / Visual Studio (Zero Docker dependency required)

---

## Microservices & Gateway Overview

| # | Component | Database Name | Default Port | Direct Swagger URL | Gateway Route |
|---|---|---|---|---|---|
| 0 | **YARP API Gateway** | *N/A (Routing Layer)* | `5000` | `http://localhost:5000` | `/api/*` |
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

### 3. Order Cancellation Before Payment & Stock Restoration
- **Cancel Order Before Payment**: Doctors have the ability to cancel an order at any time before payment is completed (`PUT /api/orders/{id}/cancel`).
- **Eligibility**: Orders in `Pending` or `Cart` status can be cancelled. Once an order is verified or marked as `PickedUp`, cancellation is strictly rejected.
- **Automated Stock Restoration**:
  - When an order is cancelled, `OrderService` automatically makes an inter-service HTTP call to `InventoryService` endpoint `PUT /api/drugs/restore-stock`.
  - For each line item in the order, the exact ordered quantity is immediately added back to the active drug stock (`Quantity += item.Quantity`), and `IsAvailable` is set to `true` if previously depleted.
  - This ensures that stock is never permanently lost or locked by abandoned or cancelled orders.

### 4. Payment Simulation & Validation
- **Payment Cancellation Protection**:
  - `PaymentService` validates the order status before processing any payment.
  - If a doctor attempts to simulate or submit payment for a cancelled order, the payment is rejected with HTTP 400: `"Cannot process payment for a cancelled order."`
- **Payment Amount Validation**: The payment amount must exactly match the calculated order total.
- **Payment Methods Supported**: `CreditCard`, `DebitCard`, `UPI`, `NetBanking`, `Cash`.
- **Successful Payment**: Upon successful payment simulation (`POST /api/payments/simulate`), the payment status is marked `Completed`, and an inter-service call marks the order as `Verified`.
- **Order Pickup**: Admins review verified orders and transition them to `PickedUp` upon physical handover of medicines (`PUT /api/orders/{id}/pickup`).

### 5. Admin Inventory & Analytics Suite
- **Drugs Management**: Add, update, view, and delete drugs (`/api/drugs`). Supports minimum stock threshold (default: 20 units).
- **Suppliers Management**: Register, update, view, and delete suppliers (`/api/suppliers`).
- **Inventory Stock Batches**: Record incoming stock batches with purchase price, batch number, and supply date (`POST /api/inventory`).
- **Low Stock Monitoring**: View medicines where `Quantity <= MinimumStockQuantity` (`GET /api/drugs/low-stock`).
- **Expired Drug Monitoring**: View medicines where `ExpiryDate < DateTime.UtcNow` (`GET /api/drugs/expired`).
- **Profit Margin Analysis**: Calculate profit generated per drug based on `SellingPrice - PurchasePrice` (`GET /api/salereports/analytics/profit`).
- **Top Selling Medicines**: Retrieve highest volume drugs sold across all completed orders (`GET /api/salereports/analytics/top-selling`).
- **Sales Reporting**: Generate Daily, Weekly, Monthly, and Yearly sales summaries with total orders, total revenue, and profit (`GET /api/salereports`).
- **Export & Print**: Download sales reports as CSV spreadsheet files (`GET /api/salereports/{id}/download`) or view printable formatted receipts (`GET /api/salereports/{id}/print`).

---

## Entity Framework Core (EF Core) Migrations — Detailed Guide

The project implements **Entity Framework Core Code-First Migrations** across all 5 microservices. Each service maintains its own isolated `DbContext`, migration history table (`__EFMigrationsHistory`), and dedicated SQL Server database.

### Migration Architecture & Design

Each microservice contains a dedicated `Migrations/` directory with:
1. `20261121000001_InitialCreate.cs`: Migration operations (`Up()` and `Down()`) defining tables, primary keys, foreign keys, column types, and unique constraints.
2. `20261121000001_InitialCreate.Designer.cs`: Metadata and model snapshot representation at the time of migration creation.
3. `<ServiceName>DbContextModelSnapshot.cs`: Current snapshot of the EF Core entity model used to calculate subsequent migrations.

```
src/Services/
├── AuthService/
│   ├── Data/AuthDbContext.cs
│   └── Migrations/
│       ├── 20261121000001_InitialCreate.cs
│       ├── 20261121000001_InitialCreate.Designer.cs
│       └── AuthDbContextModelSnapshot.cs
├── InventoryService/
│   ├── Data/InventoryDbContext.cs
│   └── Migrations/
│       ├── 20261121000001_InitialCreate.cs
│       ├── 20261121000001_InitialCreate.Designer.cs
│       └── InventoryDbContextModelSnapshot.cs
├── OrderService/
│   ├── Data/OrderDbContext.cs
│   └── Migrations/
│       ├── 20261121000001_InitialCreate.cs
│       ├── 20261121000001_InitialCreate.Designer.cs
│       └── OrderDbContextModelSnapshot.cs
├── PaymentService/
│   ├── Data/PaymentDbContext.cs
│   └── Migrations/
│       ├── 20261121000001_InitialCreate.cs
│       ├── 20261121000001_InitialCreate.Designer.cs
│       └── PaymentDbContextModelSnapshot.cs
└── SaleReportService/
    ├── Data/SaleReportDbContext.cs
    └── Migrations/
        ├── 20261121000001_InitialCreate.cs
        ├── 20261121000001_InitialCreate.Designer.cs
        └── SaleReportDbContextModelSnapshot.cs
```

---

### Automated Migrations on Startup

You do not need to run manual migration commands to start using the system. Each microservice's `DbInitializer.cs` automatically detects if a relational SQL Server is available and applies pending migrations at startup:

```csharp
// Program.cs / DbInitializer.cs execution pattern
if (context.Database.IsRelational())
{
    // Applies any pending EF Core migrations and creates database if it does not exist
    await context.Database.MigrateAsync();
}

// Pre-seeds initial Admin and Doctor credentials if not present
await DbInitializer.InitializeAsync(context);
```

When you start any service via `dotnet run` or double-click `RunAllServices.bat`, EF Core automatically creates the database and all required tables if they do not exist.

---

### How to Implement & Run Migrations via .NET CLI

If you modify entity models or want to manage migrations manually, follow these detailed CLI instructions.

#### 1. Prerequisites
Ensure the .NET EF Core CLI tool is installed globally on your machine:
```powershell
dotnet tool install --global dotnet-ef
```
To update the tool to the latest version:
```powershell
dotnet tool update --global dotnet-ef
```

---

#### 2. Applying Existing Migrations to the Database
To apply the existing migrations and update the SQL Server database for each microservice:

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

#### 3. Adding a New Migration After Changing an Entity Model
Whenever you add a new property, table, or constraint to an entity model:

1. Edit the Model class in the target microservice (e.g., `Drug.cs` in `InventoryService`).
2. Run the `migrations add` command targeting that service:

```powershell
# Syntax: dotnet ef migrations add <MigrationName> --project <PathToProject> --startup-project <PathToProject>

# Example: Adding a new migration to InventoryService
dotnet ef migrations add AddManufacturerToDrugs --project src/Services/InventoryService --startup-project src/Services/InventoryService

# Example: Adding a new migration to OrderService
dotnet ef migrations add AddTrackingNumberToOrders --project src/Services/OrderService --startup-project src/Services/OrderService
```
3. Apply the newly created migration to the database:
```powershell
dotnet ef database update --project src/Services/InventoryService --startup-project src/Services/InventoryService
```

---

#### 4. Removing or Reverting a Migration
If you created a migration but have not applied it to the database yet and want to remove it:
```powershell
dotnet ef migrations remove --project src/Services/InventoryService --startup-project src/Services/InventoryService
```
If the migration was already applied to the database, first roll back the database to the previous migration, then remove it:
```powershell
# Roll back to the specific previous migration name
dotnet ef database update InitialCreate --project src/Services/InventoryService --startup-project src/Services/InventoryService

# Then remove the reverted migration files
dotnet ef migrations remove --project src/Services/InventoryService --startup-project src/Services/InventoryService
```

---

### Generating SQL Scripts for Production / CI/CD

In production environments where direct CLI access is restricted, you can generate idempotent SQL migration scripts that can be reviewed and executed by Database Administrators (DBAs) or CI/CD pipelines:

```powershell
# Generate idempotent script for AuthService
dotnet ef migrations script --idempotent --project src/Services/AuthService --startup-project src/Services/AuthService --output scripts/AuthService_Migration.sql

# Generate idempotent script for InventoryService
dotnet ef migrations script --idempotent --project src/Services/InventoryService --startup-project src/Services/InventoryService --output scripts/InventoryService_Migration.sql

# Generate idempotent script for OrderService
dotnet ef migrations script --idempotent --project src/Services/OrderService --startup-project src/Services/OrderService --output scripts/OrderService_Migration.sql

# Generate idempotent script for PaymentService
dotnet ef migrations script --idempotent --project src/Services/PaymentService --startup-project src/Services/PaymentService --output scripts/PaymentService_Migration.sql

# Generate idempotent script for SaleReportService
dotnet ef migrations script --idempotent --project src/Services/SaleReportService --startup-project src/Services/SaleReportService --output scripts/SaleReportService_Migration.sql
```

The `--idempotent` flag ensures that the generated SQL script checks the `__EFMigrationsHistory` table before applying each change, making it safe to execute multiple times on any environment.

---

### Database Connection String Configuration

Each microservice specifies its database connection string in its `appsettings.json`. By default, it connects to local SQL Server using Windows Authentication:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=Pharmacy_UserDB;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=true"
  }
}
```

#### SQL Server Fallback Script:
If you prefer running a direct SQL script in SQL Server Management Studio (SSMS) instead of EF Core migrations, execute the master script located at:
```sql
-- Open and execute in SSMS
scripts/InitDatabases.sql
```
This script creates all 5 databases, tables, indices, foreign keys, and seed records in a single execution.

---

## Database Schemas & Data Dictionary

### 1. AuthService (`Pharmacy_UserDB`)
- **`Users` Table**:
  - `UserId` (int, Primary Key, Identity 1,1)
  - `Name` (nvarchar(100), NOT NULL)
  - `Email` (nvarchar(150), NOT NULL, UNIQUE index)
  - `PhoneNumber` (nvarchar(20), NOT NULL)
  - `PasswordHash` (nvarchar(255), NOT NULL)
  - `Role` (nvarchar(20), NOT NULL — `Admin` or `Doctor`)
  - `CreatedDate` (datetime2, NOT NULL)
  - `IsActive` (bit, NOT NULL, DEFAULT 1)

### 2. InventoryService (`Pharmacy_InventoryDB`)
- **`Drugs` Table**:
  - `DrugId` (int, Primary Key, Identity 1,1)
  - `DrugName` (nvarchar(150), NOT NULL)
  - `Description` (nvarchar(500), NULL)
  - `Category` (nvarchar(100), NOT NULL)
  - `Price` (decimal(18,2), NOT NULL — Selling price)
  - `ExpiryDate` (datetime2, NOT NULL)
  - `Quantity` (int, NOT NULL, DEFAULT 0)
  - `MinimumStockQuantity` (int, NOT NULL, DEFAULT 20)
  - `IsAvailable` (bit, NOT NULL, DEFAULT 1)
  - `CreatedDate` (datetime2, NOT NULL)
  - `UpdatedDate` (datetime2, NULL)
- **`Suppliers` Table**:
  - `SupplierId` (int, Primary Key, Identity 1,1)
  - `SupplierName` (nvarchar(150), NOT NULL)
  - `Email` (nvarchar(150), NOT NULL)
  - `PhoneNumber` (nvarchar(20), NOT NULL)
  - `Address` (nvarchar(300), NOT NULL)
- **`Inventory` Table**:
  - `InventoryId` (int, Primary Key, Identity 1,1)
  - `SupplierId` (int, Foreign Key to `Suppliers.SupplierId`, NOT NULL)
  - `DrugId` (int, Foreign Key to `Drugs.DrugId`, NOT NULL)
  - `PurchasePrice` (decimal(18,2), NOT NULL)
  - `SupplyDate` (datetime2, NOT NULL)
  - `QuantitySupplied` (int, NOT NULL)
  - `BatchNumber` (nvarchar(100), NOT NULL)
  - `Notes` (nvarchar(500), NULL)

### 3. OrderService (`Pharmacy_OrderDB`)
- **`Orders` Table**:
  - `OrderId` (int, Primary Key, Identity 1,1)
  - `DoctorID` (int, Logical Foreign Key referencing `Users.UserId`, NOT NULL)
  - `OrderDate` (datetime2, NOT NULL)
  - `TotalAmount` (decimal(18,2), NOT NULL)
  - `Status` (nvarchar(20), NOT NULL — `Cart`, `Pending`, `Verified`, `PickedUp`, `Cancelled`)
- **`OrderItems` Table**:
  - `OrderItemId` (int, Primary Key, Identity 1,1)
  - `OrderId` (int, Foreign Key to `Orders.OrderId`, ON DELETE CASCADE, NOT NULL)
  - `DrugId` (int, Logical Foreign Key referencing `Drugs.DrugId`, NOT NULL)
  - `DrugName` (nvarchar(150), NOT NULL)
  - `Quantity` (int, NOT NULL)
  - `UnitPrice` (decimal(18,2), NOT NULL)

### 4. PaymentService (`Pharmacy_PaymentDB`)
- **`Payments` Table**:
  - `PaymentId` (int, Primary Key, Identity 1,1)
  - `OrderId` (int, Logical Foreign Key referencing `Orders.OrderId`, NOT NULL, UNIQUE index for strict 1:1)
  - `Amount` (decimal(18,2), NOT NULL)
  - `PaymentDate` (datetime2, NOT NULL)
  - `PaymentMethod` (nvarchar(50), NOT NULL — `CreditCard`, `DebitCard`, `UPI`, `NetBanking`, `Cash`)
  - `PaymentStatus` (nvarchar(20), NOT NULL — `Pending`, `Completed`, `Failed`)
  - `TransactionReference` (nvarchar(100), NOT NULL)

### 5. SaleReportService (`Pharmacy_SaleReportDB`)
- **`SaleReports` Table**:
  - `SaleReportId` (int, Primary Key, Identity 1,1)
  - `ReportType` (nvarchar(20), NOT NULL — `Daily`, `Weekly`, `Monthly`, `Yearly`)
  - `FromDate` (datetime2, NOT NULL)
  - `ToDate` (datetime2, NOT NULL)
  - `TotalOrders` (int, NOT NULL)
  - `TotalRevenue` (decimal(18,2), NOT NULL)
  - `Profit` (decimal(18,2), NOT NULL)
  - `GeneratedDate` (datetime2, NOT NULL)

---

## Complete API Catalogue

### 1. AuthService (Port 5001 / Gateway `/api/auth`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `POST` | `/api/auth/register` | Public (Doctor only) | Self-registration for doctors. Admin registration is strictly blocked. |
| `POST` | `/api/auth/login` | Public | Authenticates credentials and returns a signed JWT Bearer token. |
| `GET` | `/api/auth/current-user` | Authenticated | Returns current authenticated user profile (`UserId`, `Email`, `Role`, `Name`). |

### 2. InventoryService (Port 5002 / Gateway `/api/drugs`, `/api/suppliers`, `/api/inventory`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/drugs` | Public / Doctor / Admin | List all active medications. |
| `GET` | `/api/drugs/{id}` | Public / Doctor / Admin | Get medication by ID. |
| `GET` | `/api/drugs/search` | Public / Doctor / Admin | Search drugs by name or category. |
| `GET` | `/api/drugs/low-stock` | Admin | Retrieve medicines below minimum stock threshold (`Quantity <= 20`). |
| `GET` | `/api/drugs/expired` | Admin | Retrieve medicines whose expiry date has passed. |
| `POST` | `/api/drugs` | Admin | Add a new drug with pricing and stock threshold. |
| `PUT` | `/api/drugs/{id}` | Admin | Update drug details. |
| `DELETE` | `/api/drugs/{id}` | Admin | Delete a drug record. |
| `PUT` | `/api/drugs/restore-stock` | Internal / OrderService | Restores drug stock quantities when an order is cancelled. |
| `GET` | `/api/suppliers` | Admin | List all registered suppliers. |
| `GET` | `/api/suppliers/{id}` | Admin | Get supplier details by ID. |
| `POST` | `/api/suppliers` | Admin | Register a new supplier. |
| `PUT` | `/api/suppliers/{id}` | Admin | Update supplier contact info. |
| `DELETE` | `/api/suppliers/{id}` | Admin | Delete a supplier. |
| `POST` | `/api/inventory` | Admin | Record incoming inventory stock batch from supplier. |

### 3. OrderService (Port 5003 / Gateway `/api/orders`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/orders` | Admin | View all orders placed across all doctors. |
| `GET` | `/api/orders/{id}` | Authenticated | View details of a specific order. |
| `GET` | `/api/orders/my-orders` | Doctor | View order history for the authenticated doctor. |
| `GET` | `/api/orders/cart` | Doctor | Retrieve current active cart items for the logged-in doctor. |
| `POST` | `/api/orders/cart` | Doctor | Add drug items to cart. |
| `POST` | `/api/orders` | Doctor | Place order, deduct stock from Inventory, and move to `Pending`. |
| `PUT` | `/api/orders/{id}/cancel` | Doctor / Admin | **Cancel order before payment.** Releases and restores stock back to inventory. |
| `GET` | `/api/orders/{id}/validate` | Admin | Validate order items, pricing, and stock feasibility. |
| `PUT` | `/api/orders/{id}/verify` | Admin | Verify order status after successful payment (`Status = Verified`). |
| `PUT` | `/api/orders/{id}/pickup` | Admin | Mark order as `PickedUp` upon physical handover of medicines. |
| `GET` | `/api/orders/picked-up` | Admin | List all completed picked-up orders. |

### 4. PaymentService (Port 5004 / Gateway `/api/payments`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `POST` | `/api/payments/simulate` | Doctor | **Simulates payment.** Validates order exists, is not cancelled, and amount matches. Updates order to `Verified`. |
| `GET` | `/api/payments/{id}` | Admin / Doctor | View payment receipt and transaction reference. |
| `GET` | `/api/payments/order/{orderId}` | Admin / Doctor | Retrieve payment record by associated Order ID (1:1). |

### 5. SaleReportService (Port 5005 / Gateway `/api/salereports`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/salereports` | Admin | List all generated sales reports. |
| `GET` | `/api/salereports/{id}` | Admin | Retrieve sales report by ID. |
| `POST` | `/api/salereports/generate` | Admin | Generate a new Daily, Weekly, Monthly, or Yearly sales report. |
| `GET` | `/api/salereports/{id}/download` | Admin | Export and download sales report as CSV spreadsheet. |
| `GET` | `/api/salereports/{id}/print` | Admin | Retrieve formatted printable receipt view. |
| `GET` | `/api/salereports/analytics/profit` | Admin | View profit analysis (`SellingPrice - PurchasePrice`). |
| `GET` | `/api/salereports/analytics/top-selling` | Admin | View highest selling drugs by total quantity sold. |
| `GET` | `/api/salereports/analytics/dashboard` | Admin | High-level business KPI dashboard (Revenue, Orders, Profit). |

---

## Swagger UI Interactive Testing Guide

All microservices and the API Gateway include built-in Swagger / OpenAPI documentation with interactive testing support and JWT Bearer authentication.

### Direct Access URLs:
- **YARP API Gateway**: `http://localhost:5000` (Routes all microservices through a single entry point)
- **Auth Service**: `http://localhost:5001/swagger`
- **Inventory Service**: `http://localhost:5002/swagger`
- **Order Service**: `http://localhost:5003/swagger`
- **Payment Service**: `http://localhost:5004/swagger`
- **SaleReport Service**: `http://localhost:5005/swagger`

---

### Step-by-Step Testing Workflow via Swagger

#### Step 1: Authenticate as Pre-Seeded Admin
1. Open `http://localhost:5001/swagger` (AuthService).
2. Expand `POST /api/auth/login`. Click **Try it out**.
3. Submit pre-seeded Admin credentials:
```json
{
  "email": "admin@pharmacy.com",
  "password": "Admin@123"
}
```
4. Copy the returned `token` from the JSON response.
5. In Swagger, click the **Authorize 🔓** button at the top right of the page.
6. Enter `Bearer <YOUR_COPIED_TOKEN>` and click **Authorize**. The lock icon changes to locked 🔒.

#### Step 2: Verify Admin Cannot Register
1. In `AuthService` Swagger, expand `POST /api/auth/register`.
2. Try submitting an Admin registration request:
```json
{
  "name": "New Admin",
  "email": "anotheradmin@pharmacy.com",
  "phoneNumber": "9998887770",
  "password": "AdminPassword@123",
  "role": "Admin"
}
```
3. Observe the immediate **HTTP 400 Bad Request** error: `"Admin registration is not allowed. Admin accounts must be pre-seeded or provisioned by system administration."`

#### Step 3: Register and Authenticate as a Doctor
1. In `POST /api/auth/register`, submit valid Doctor registration details:
```json
{
  "name": "Dr. Sarah Smith",
  "email": "sarah.smith@hospital.com",
  "phoneNumber": "9876543210",
  "password": "Doctor@123",
  "role": "Doctor"
}
```
2. Log in using `POST /api/auth/login` with the newly created doctor credentials.
3. Copy the doctor token and authorize Swagger on port `5003` (OrderService) and port `5004` (PaymentService).

#### Step 4: Admin Adds Drugs and Suppliers
1. Open `http://localhost:5002/swagger` (InventoryService) with the **Admin Token**.
2. Create a supplier via `POST /api/suppliers`:
```json
{
  "supplierName": "Apex Healthcare Pharma",
  "email": "contact@apexpharma.com",
  "phoneNumber": "9876500001",
  "address": "45 Industrial Zone, Sector 4, Hyderabad"
}
```
3. Create a drug via `POST /api/drugs`:
```json
{
  "drugName": "Amoxicillin 500mg",
  "description": "Broad-spectrum antibacterial medication",
  "category": "Antibiotics",
  "price": 25.00,
  "expiryDate": "2027-12-31T00:00:00Z",
  "quantity": 100,
  "minimumStockQuantity": 20
}
```

#### Step 5: Doctor Places an Order
1. Open `http://localhost:5003/swagger` (OrderService) with the **Doctor Token**.
2. Submit `POST /api/orders`:
```json
{
  "items": [
    {
      "drugId": 1,
      "drugName": "Amoxicillin 500mg",
      "quantity": 10,
      "unitPrice": 25.00
    }
  ]
}
```
3. The response returns an order with `orderId: 1`, `status: "Pending"`, and `totalAmount: 250.00`.
4. Check `GET /api/drugs/1` in InventoryService: notice the stock quantity has atomically dropped from `100` to `90`.

#### Step 6: Test Order Cancellation Before Payment & Stock Restoration
1. In `OrderService` Swagger, execute `PUT /api/orders/1/cancel`.
2. Notice the order status updates to `"Cancelled"`.
3. Check `GET /api/drugs/1` in `InventoryService`: observe that the quantity has been **automatically restored back to 100** via the stock restore hook!
4. Switch to `http://localhost:5004/swagger` (PaymentService) and try to simulate payment for this cancelled order:
```json
{
  "orderId": 1,
  "amount": 250.00,
  "paymentMethod": "UPI"
}
```
5. Observe the **HTTP 400 Bad Request** error: `"Cannot process payment for a cancelled order."`

#### Step 7: Place a New Order, Pay, Verify, and Pick Up
1. Doctor places a new order via `POST /api/orders` (e.g., `orderId: 2`, `totalAmount: 250.00`).
2. Simulate payment via `POST /api/payments/simulate`:
```json
{
  "orderId": 2,
  "amount": 250.00,
  "paymentMethod": "UPI"
}
```
3. The payment is recorded as `Completed` with a unique transaction reference (e.g., `TXN-ORD2-...`), and the order status updates to `Verified`.
4. As Admin, call `PUT /api/orders/2/pickup` in `OrderService`: order transitions to `PickedUp`.

#### Step 8: Admin Generates and Downloads Sales Reports
1. Open `http://localhost:5005/swagger` (SaleReportService) with the **Admin Token**.
2. Generate a sales report via `POST /api/salereports/generate`:
```json
{
  "reportType": "Daily",
  "fromDate": "2026-11-01T00:00:00Z",
  "toDate": "2026-11-30T23:59:59Z"
}
```
3. Export and download as CSV via `GET /api/salereports/1/download`.
4. Inspect analytics via `GET /api/salereports/analytics/profit` and `GET /api/salereports/analytics/dashboard`.

---

## How to Run the Application

### Option 1: 1-Click Windows Launcher Script (Recommended)
Double-click `RunAllServices.bat` in the repository root folder.

This script launches all 5 microservices and the YARP API Gateway in parallel:
- AuthService (Port 5001)
- InventoryService (Port 5002)
- OrderService (Port 5003)
- PaymentService (Port 5004)
- SaleReportService (Port 5005)
- YARP API Gateway (Port 5000)

And automatically opens all Swagger interactive testing dashboards in your default web browser.

---

### Option 2: Run Microservices Individually via .NET CLI
Run each microservice in its own terminal window:
```powershell
# Terminal 1: Auth Service
dotnet run --project src/Services/AuthService

# Terminal 2: Inventory Service
dotnet run --project src/Services/InventoryService

# Terminal 3: Order Service
dotnet run --project src/Services/OrderService

# Terminal 4: Payment Service
dotnet run --project src/Services/PaymentService

# Terminal 5: SaleReport Service
dotnet run --project src/Services/SaleReportService

# Terminal 6: YARP API Gateway
dotnet run --project src/ApiGateway
```

---

## Automated NUnit Testing Suite (30 Test Cases)

The project includes a comprehensive automated test suite in `tests/PharmacyManagement.Tests/` containing **30 unit and integration tests** built using **NUnit 3, Moq, and EF Core InMemory**:

```powershell
dotnet test tests/PharmacyManagement.Tests
```

### Test Case Coverage Matrix:
- **AuthService Tests (`TC-01` to `TC-04`, `TC-23`, `TC-29`)**:
  - `TC-01`: Successful Doctor registration.
  - `TC-02`: Duplicate email rejection.
  - `TC-03`: Successful login & JWT Bearer token generation.
  - `TC-04`: Invalid password login failure.
  - `TC-23`: Pre-seeded Admin and Doctor credentials verification.
  - `TC-29`: **Admin registration prevention** (Admin cannot register; can only login).
- **InventoryService Tests (`TC-05` to `TC-09`, `TC-24`, `TC-25`, `TC-28`)**:
  - `TC-05`: Drug creation with stock quantity.
  - `TC-06`: Low-stock threshold detection (`Quantity <= 20`).
  - `TC-07`: Expired drug detection (`ExpiryDate < UtcNow`).
  - `TC-08`: Supplier registration.
  - `TC-09`: Inventory stock batch inward and quantity addition.
  - `TC-24`: Drug search filtering by name and category.
  - `TC-25`: Non-existent drug ID lookup returning null/404.
  - `TC-28`: **Stock restoration on order cancellation** (`RestoreStockAsync`).
- **OrderService Tests (`TC-10` to `TC-14`, `TC-26`, `TC-27`)**:
  - `TC-10`: Add drug items to staging cart.
  - `TC-11`: Place order with inventory stock reduction.
  - `TC-12`: Admin order verification (`Pending` -> `Verified`).
  - `TC-13`: Admin order pickup (`Verified` -> `PickedUp`).
  - `TC-14`: Reject order placement when drug is out of stock.
  - `TC-26`: **Cancel order before payment** with automated stock release.
  - `TC-27`: Prevent cancellation of picked-up orders.
- **PaymentService Tests (`TC-15` to `TC-18`, `TC-30`)**:
  - `TC-15`: Payment simulation with method (Card, UPI, Cash) and transaction reference generation.
  - `TC-16`: Payment amount mismatch rejection.
  - `TC-17`: Duplicate payment rejection on same order (1:1 enforcement).
  - `TC-18`: Non-existent order payment rejection.
  - `TC-30`: **Payment rejection on cancelled order** (`"Cannot process payment for a cancelled order."`).
- **SaleReportService Tests (`TC-19` to `TC-22`)**:
  - `TC-19`: Daily and Monthly sales summary report generation.
  - `TC-20`: Profit margin analysis calculation (`SellingPrice - PurchasePrice`).
  - `TC-21`: Top-selling drugs reporting.
  - `TC-22`: CSV export data formatting and receipt generation.

---

## Project Structure & Documentation

```
pharmacyManagement/
├── PharmacyManagement.sln                   # Master Visual Studio Solution File
├── RunAllServices.bat                       # 1-Click Launch Script for all microservices & gateway
├── README.md                                # Comprehensive project & migrations documentation
├── scripts/
│   ├── InitDatabases.sql                    # Master SQL Server database initialization & seed script
│   ├── generate_lld_docx.py                 # LLD Word document generator
│   ├── generate_lld_pdf.py                  # LLD PDF generator
│   └── generate_reference_style_diagrams.py # Architectural diagram rendering script
├── docs/
│   ├── LLD v1.docx                          # Official Low Level Design (LLD) Word Document
│   ├── PharmacyManagement_LLD.md            # Complete Markdown LLD Document with diagram links
│   └── diagrams/                            # Architectural & Design Diagrams
│       ├── architecture.jpg                 # Figure 6.0: Solution Architecture Diagram
│       ├── useCase.jpg                      # Figure 7.0: Use Case Diagram
│       ├── ER.jpg                           # Figure 8.0: Entity-Relationship Diagram
│       ├── Database.jpg                     # Figure 9.0: Database Schema Diagram
│       └── Class.jpg                        # Figure 10.0: Domain Class Diagram
├── src/
│   ├── ApiGateway/                          # Port 5000: YARP API Gateway & unified routing
│   ├── Common/
│   │   └── PharmacyManagement.Common/       # Shared JWT security, models, responses, and helpers
│   └── Services/
│       ├── AuthService/                     # Port 5001: JWT Authentication & User Service + Migrations
│       ├── InventoryService/                # Port 5002: Drugs, Suppliers & Stock Inventory + Migrations
│       ├── OrderService/                    # Port 5003: Orders, Cart, Cancellation & Stock Release + Migrations
│       ├── PaymentService/                  # Port 5004: Payment Simulation & Cancellation Protection + Migrations
│       └── SaleReportService/               # Port 5005: Sales Reports, Profit Analytics & CSV Export + Migrations
└── tests/
    └── PharmacyManagement.Tests/            # NUnit 3 Test Project covering TC-01 to TC-30
```

### Architectural Diagrams Reference:
All architectural diagrams are maintained in high resolution in `docs/diagrams/`:
- **Solution Architecture Diagram**: [docs/diagrams/architecture.jpg](docs/diagrams/architecture.jpg)
- **Use Case Diagram**: [docs/diagrams/useCase.jpg](docs/diagrams/useCase.jpg)
- **Entity-Relationship Diagram**: [docs/diagrams/ER.jpg](docs/diagrams/ER.jpg)
- **Database Schema Diagram**: [docs/diagrams/Database.jpg](docs/diagrams/Database.jpg)
- **Domain Class Diagram**: [docs/diagrams/Class.jpg](docs/diagrams/Class.jpg)
