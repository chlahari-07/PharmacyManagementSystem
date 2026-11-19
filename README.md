# Pharmacy Management System (.NET Microservices Architecture)

A distributed microservices-based **Pharmacy Management System** developed using **C#, ASP.NET Core Web API, .NET 10 / .NET 8, Entity Framework Core (EF Core) Code-First, Microsoft SQL Server, YARP API Gateway, JWT Security, Swagger/OpenAPI, and NUnit Testing with Payment Simulation**.

Each microservice is an independent Web API adhering to the internal **MVC (Controller-Service-Repository) pattern**, with its own dedicated SQL Server database and automated Swagger / OpenAPI documentation.

---

## Architecture & Technology Stack

- **Language & Framework**: C#, ASP.NET Core Web API (.NET 10 / .NET 8)
- **Architecture**: Distributed Microservice Architecture (5 Services + YARP Gateway)
- **Data Access**: Entity Framework Core (EF Core) Code-First with LINQ
- **Database**: Microsoft SQL Server 2022 (Database-per-service pattern)
- **API Gateway**: YARP (Yet Another Reverse Proxy) with Unified Routing
- **Security**: JWT (JSON Web Tokens) Bearer Authentication with Role-Based Access Control (`Admin`, `Doctor`)
- **API Documentation & Testing**: Swagger / OpenAPI UI on all services and gateway
- **Unit Testing**: NUnit 3 Test Suite (TC-01 to TC-22) with Moq and InMemory DbContext
- **Payment Simulation**: Built-in payment gateway simulator (no real payment API required)
- **Deployment & Execution**: Direct native execution on Windows via .NET CLI / Visual Studio (Zero Docker dependency)

---

## 5 Microservices & YARP Gateway Overview

| # | Component | Database Name | Default Port | Swagger / Gateway URL |
|---|---|---|---|---|
| 0 | **YARP API Gateway** | *N/A (Routing Layer)* | `5000` | `http://localhost:5000` |
| 1 | **Auth Service** | `Pharmacy_UserDB` | `5001` | `http://localhost:5001/swagger` |
| 2 | **Inventory Service** | `Pharmacy_InventoryDB` | `5002` | `http://localhost:5002/swagger` |
| 3 | **Order Service** | `Pharmacy_OrderDB` | `5003` | `http://localhost:5003/swagger` |
| 4 | **Payment Service** | `Pharmacy_PaymentDB` | `5004` | `http://localhost:5004/swagger` |
| 5 | **SaleReport Service** | `Pharmacy_SaleReportDB` | `5005` | `http://localhost:5005/swagger` |

---

## Microservices Table Attributes & Relationships

### 1. AuthService (`Pharmacy_UserDB`)
- **`Users` Table**: `UserId` (PK, int), `Name` (nvarchar 100), `Email` (nvarchar 150, unique), `PhoneNumber` (nvarchar 20), `PasswordHash` (nvarchar 255), `Role` (nvarchar 20: `Admin`/`Doctor`), `CreatedDate` (datetime2), `IsActive` (bit).

### 2. InventoryService (`Pharmacy_InventoryDB`)
- **`Drugs` Table**: `DrugId` (PK, int), `DrugName` (nvarchar 150), `Description` (nvarchar 500), `Category` (nvarchar 100), `Price` (decimal 18,2 - selling price), `ExpiryDate` (datetime2), `Quantity` (int), `MinimumStockQuantity` (int, default 20), `IsAvailable` (bit), `CreatedDate` (datetime2), `UpdatedDate` (datetime2).
- **`Suppliers` Table**: `SupplierId` (PK, int), `SupplierName` (nvarchar 150), `Email` (nvarchar 150), `PhoneNumber` (nvarchar 20), `Address` (nvarchar 300).
- **`Inventory` Table**: `InventoryId` (PK, int), `SupplierId` (FK, int), `DrugId` (FK, int), `PurchasePrice` (decimal 18,2), `SupplyDate` (datetime2), `QuantitySupplied` (int), `BatchNumber` (nvarchar 100), `Notes` (nvarchar 500).

### 3. OrderService (`Pharmacy_OrderDB`)
- **`Orders` Table**: `OrderId` (PK, int), `DoctorID` (Logical FK from User table), `OrderDate` (datetime2), `TotalAmount` (decimal 18,2), `Status` (nvarchar 20: `Cart` / `Pending` / `Verified` / `PickedUp` / `Cancelled`).
- **`OrderItems` Table**: `OrderItemId` (PK, int), `OrderId` (FK to Orders), `DrugId` (Logical FK to Drugs), `DrugName` (nvarchar 150), `Quantity` (int), `UnitPrice` (decimal 18,2).

### 4. PaymentService (`Pharmacy_PaymentDB`)
- **`Payments` Table**: `PaymentId` (PK, int), `OrderId` (Logical FK from Orders, unique 1:1), `Amount` (decimal 18,2), `PaymentDate` (datetime2), `PaymentMethod` (nvarchar 50: `CreditCard`, `DebitCard`, `UPI`, `NetBanking`, `Cash`), `PaymentStatus` (nvarchar 20: `Pending` / `Completed` / `Failed`), `TransactionReference` (nvarchar 100).

### 5. SaleReportService (`Pharmacy_SaleReportDB`)
- **`SaleReports` Table**: `SaleReportId` (PK, int), `ReportType` (nvarchar 20: `Daily`, `Weekly`, `Monthly`, `Yearly`), `FromDate` (datetime2), `ToDate` (datetime2), `TotalOrders` (int), `TotalRevenue` (decimal 18,2), `GeneratedDate` (datetime2), `Profit` (decimal 18,2).

### Entity Relationships
- **User to Order**: `1:M` (A doctor places multiple orders)
- **Order to OrderItem**: `1:M` (An order contains multiple line items)
- **Drug to OrderItem**: `1:M` (A drug appears in multiple order line items)
- **Supplier to Inventory**: `1:M` (A supplier supplies multiple stock batches)
- **Drug to Inventory**: `1:M` (A drug is replenished through multiple inventory batches)
- **Order to Payment**: `1:1` (Each order has exactly one payment record)
- **SaleReport**: Standalone aggregated entity

---

## Features Implemented

### For Admin:
1. **Login/Signup**: Sign up with basic details: name, contact, email, and password.
2. **View drugs**: View and check details of each and every drug available (`GET /api/drugs`).
3. **Add/Edit/Delete drugs**: Full CRUD operations with minimum stock threshold (`POST`, `PUT`, `DELETE /api/drugs`).
4. **View suppliers**: View and check details of each and every supplier (`GET /api/suppliers`).
5. **Add/Edit/Delete supplier**: Full supplier management (`POST`, `PUT`, `DELETE /api/suppliers`).
6. **View doctor orders & Validate**: View orders placed by all doctors and check if order is valid (`GET /api/orders`, `GET /api/orders/{id}/validate`).
7. **Verify orders**: On validating the order, verify the order transitioning status to `Verified` (`PUT /api/orders/{id}/verify`).
8. **Add order to pickedUp section**: Move order to `PickedUp` section upon medication handover (`PUT /api/orders/{id}/pickup`, `GET /api/orders/picked-up`).
9. **View Sales Report**: Access historical reports Daily, Weekly, Monthly, Yearly (`GET /api/salereports`).
10. **Download/Print sales report**: Export report as CSV spreadsheet or retrieve formatted printable receipt (`GET /api/salereports/{id}/download`, `GET /api/salereports/{id}/print`).
11. **Admin Analytics Suite**:
    - **Low Stock Monitoring**: View medicines where `Quantity <= MinimumStockQuantity` (`GET /api/drugs/low-stock`).
    - **Expired Drug Report**: View medicines where `ExpiryDate < DateTime.UtcNow` (`GET /api/drugs/expired`).
    - **Profit Analysis**: View profit generated based on purchase price vs selling price (`GET /api/salereports/analytics/profit`).
    - **Top Selling Drugs Report**: View drugs with the highest sales quantity (`GET /api/salereports/analytics/top-selling`).
    - **Dashboard Analytics**: Overall platform statistics: total orders, total revenue, and profit (`GET /api/salereports/analytics/dashboard`).

### For Doctor User:
1. **Login/Signup**: Sign up with basic details: name, contact, email, and password.
2. **View drugs**: Browse and search active available medications (`GET /api/drugs`, `GET /api/drugs/search`).
3. **Buy drugs**: Place active medication order with automated inventory deduction (`POST /api/orders`).
4. **Add drugs to cart**: Stage items into active cart order (`POST /api/orders/cart`, `GET /api/orders/cart`).
5. **Payment simulation**: Simulate payment processing (CreditCard, DebitCard, UPI, NetBanking, Cash) with success/failure scenarios (`POST /api/payments/simulate`).
6. **Track order status**: Real-time status lookup (`GET /api/orders/{id}`).
7. **View order history**: View all orders placed by the authenticated doctor (`GET /api/orders/my-orders`).

---

## Project Structure

```
pharmacyManagement/
├── PharmacyManagement.sln               # Master Solution File (6 Services + Gateway + Tests)
├── RunAllServices.bat                   # 1-Click Launch Script for all microservices & gateway
├── scripts/
│   ├── InitDatabases.sql                # Complete SQL Server creation & seed script
│   ├── generate_lld_docx.py             # Python DOCX generator for LLD
│   ├── generate_lld_pdf.py              # Python PDF generator for LLD
│   └── generate_reference_style_diagrams.py # Pillow diagram rendering engine
├── docs/
│   ├── PharmacyManagement_LLD.docx      # Editable Word Low Level Design Document
│   ├── PharmacyManagement_LLD.pdf       # Professional 22-page LLD PDF Document
│   ├── PharmacyManagement_LLD.md        # Complete Markdown LLD Document
│   └── diagrams/                        # 6 Reference-style architectural diagrams
├── src/
│   ├── ApiGateway/                      # Port 5000: YARP API Gateway with unified Swagger
│   ├── Common/
│   │   └── PharmacyManagement.Common/   # Shared JWT security, models, responses, and helpers
│   └── Services/
│       ├── AuthService/                 # Port 5001: User & JWT Authentication Service
│       ├── InventoryService/            # Port 5002: Drugs, Suppliers & Stock Inventory Service
│       ├── OrderService/                # Port 5003: Doctor Orders, Cart & Verification Service
│       ├── PaymentService/              # Port 5004: 1:1 Payment & Simulation Service
│       └── SaleReportService/           # Port 5005: Sales, Analytics & Profit Reporting Service
└── tests/
    └── PharmacyManagement.Tests/        # NUnit 3 Test Project covering TC-01 to TC-22
```

---

## How to Run the Project

### Option 1: 1-Click Windows Launcher Script
Double-click `RunAllServices.bat` in the root folder. It will launch:
- AuthService (Port 5001)
- InventoryService (Port 5002)
- OrderService (Port 5003)
- PaymentService (Port 5004)
- SaleReportService (Port 5005)
- YARP API Gateway (Port 5000)
And automatically open the interactive Swagger testing dashboards in your default browser.

### Option 2: Run Unit Tests via .NET CLI
```powershell
dotnet test tests/PharmacyManagement.Tests
```
All 22 NUnit test cases will execute against the in-memory test databases and verify:
- Authentication & JWT generation
- Inventory stock management & low-stock alerts
- Order validation, verification, cart staging, and pickup
- 1:1 Payment simulation and failure handling
- Sales report generation and profit margin analysis

---

## Database Initialization

Run the complete SQL script in SQL Server Management Studio (SSMS):
```sql
-- Execute scripts/InitDatabases.sql
```
This script creates all 5 databases (`Pharmacy_UserDB`, `Pharmacy_InventoryDB`, `Pharmacy_OrderDB`, `Pharmacy_PaymentDB`, `Pharmacy_SaleReportDB`) with primary keys, foreign keys, unique constraints, and seed records.
Alternatively, EF Core Code-First automatically initializes the tables and seeds default records on service startup via `DbInitializer.cs`.

---

## Default Pre-Seeded Credentials

| Role | Email | Password | Pre-seeded ID |
|---|---|---|---|
| **Admin** | `admin@pharmacy.com` | `Admin@123` | `1` |
| **Doctor** | `doctor@pharmacy.com` | `Doctor@123` | `2` |
