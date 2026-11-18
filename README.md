# Pharmacy Management System (.NET 8 Microservices)

A distributed microservices-based **Pharmacy Management System** developed using **.NET 8, C#, Entity Framework Core (EF Core), LINQ, ASP.NET Core Web API, and Microsoft SQL Server**.

Each microservice is an independent Web API adhering to the internal **MVC (Model-View-Controller / Controller-Service-Repository) pattern**, with its own dedicated SQL Server database and automated Swagger / OpenAPI documentation.

---

## Architecture & Technology Stack

- **Framework**: .NET 8 (C# 12)
- **Architecture**: Distributed Microservices Architecture
- **Web Layer**: ASP.NET Core Web API (Internal MVC pattern)
- **Data Access**: Entity Framework Core 8, LINQ
- **Database**: Microsoft SQL Server (LocalDB / Dedicated SQL Server Instances)
- **Security**: JWT (JSON Web Tokens) Bearer Authentication with Role-Based Access Control (`Admin`, `Doctor`)
- **API Documentation & Testing**: Swagger / OpenAPI with Bearer Authorization Lock Support
- **Containerization**: Docker & Docker Compose

---

## 5 Microservices Overview

| # | Microservice | Database Name | Default Port | Swagger URL |
|---|---|---|---|---|
| 1 | **Auth Service** | `Pharmacy_UserDB` | `5001` | `http://localhost:5001/swagger` |
| 2 | **Inventory Service** | `Pharmacy_InventoryDB` | `5002` | `http://localhost:5002/swagger` |
| 3 | **Order Service** | `Pharmacy_OrderDB` | `5003` | `http://localhost:5003/swagger` |
| 4 | **Payment Service** | `Pharmacy_PaymentDB` | `5004` | `http://localhost:5004/swagger` |
| 5 | **SaleReport Service** | `Pharmacy_SaleReportDB` | `5005` | `http://localhost:5005/swagger` |

---

## High-Resolution Architectural Diagrams (JPG)

All diagrams are available in high-resolution JPG format with professional colors in [`docs/diagrams/`](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams):

1. **Solution Architecture Diagram**: [01_Solution_Architecture_Diagram.jpg](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams/01_Solution_Architecture_Diagram.jpg)
2. **Use Case Diagram**: [02_Use_Case_Diagram.jpg](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams/02_Use_Case_Diagram.jpg)
3. **Sequence Diagrams (3 Workflows)**: [03_Sequence_Diagram.jpg](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams/03_Sequence_Diagram.jpg)
4. **Flow Diagram (Order Lifecycle & Inventory)**: [04_Flow_Diagram.jpg](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams/04_Flow_Diagram.jpg)
5. **Entity-Relationship (ER) Diagram**: [05_ER_Diagram.jpg](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams/05_ER_Diagram.jpg)
6. **Database Schema Diagram (5 SQL Server DBs)**: [06_Database_Schema_Diagram.jpg](file:///c:/Users/chikoti%20lahari/OneDrive/Desktop/pharmacyManagement/docs/diagrams/06_Database_Schema_Diagram.jpg)

---

## Relationships Implemented

- **User to Order**: `1:M` (A Doctor user can place multiple Orders)
- **Order to OrderItem**: `1:M` (Each Order contains multiple OrderItems)
- **Drug to OrderItem**: `1:M` (A Drug can appear in multiple OrderItems)
- **Supplier to Inventory**: `1:M` (A Supplier provides multiple Inventory stock entries)
- **Drug to Inventory**: `1:M` (A Drug is stocked through multiple Inventory records)
- **Order to Payment**: `1:1` (Each Order has exactly one Payment transaction via unique `OrderId` constraint)
- **SaleReport**: Standalone aggregated entity computing financial metrics from Orders and Inventory

---

## Features

### For Admin:
1. **Login/Signup**: Sign up with basic details: name, contact, email, and password.
2. **View drugs**: View and check details of each and every drug available.
3. **Add/Edit/Delete drugs**: Complete CRUD operations on pharmaceuticals.
4. **View suppliers**: View and check details of each and every supplier.
5. **Add/Edit/Delete supplier**: Complete CRUD operations on wholesale suppliers.
6. **View doctor orders**: View orders placed by all doctors across the hospital/clinic network.
7. **Verify orders**: Validate doctor orders and transition status to `Verified`.
8. **Add order to pickedUp section**: Hand over fulfilled medications and update status to `PickedUp`.
9. **View Sales Report**: Access historical reports (Daily, Weekly, Monthly, Yearly).
10. **Download/Print sales report**: Export report as CSV spreadsheet or retrieve formatted printable receipt.

### For Doctor User:
1. **Login/Signup**: Sign up with basic details: name, contact, email, and password.
2. **View drugs**: View and check details of each and every drug available.
3. **Buy drugs**: Place medication orders with automated stock deduction.
4. **View own orders**: Track order progress (`Cart` / `Pending` / `Verified` / `PickedUp`).
5. **Process payment**: Complete checkout via Credit Card, Debit Card, UPI, etc.

---

## Project Structure

```
pharmacyManagement/
├── PharmacyManagement.sln               # Master Solution File
├── docker-compose.yml                   # Docker configuration for SQL Server + all 5 services
├── scripts/
│   └── InitDatabases.sql                # Complete SQL Server creation & seed script
├── docs/
│   └── PharmacyManagement_LLD.md        # Full Low Level Design (LLD) document with Diagrams
├── src/
│   ├── Common/
│   │   └── PharmacyManagement.Common/   # Shared JWT security, models, responses, and helpers
│   └── Services/
│       ├── AuthService/                 # Port 5001: User & JWT Authentication Service
│       ├── InventoryService/            # Port 5002: Drugs, Suppliers & Stock Inventory Service
│       ├── OrderService/                # Port 5003: Doctor Orders & Verification Service
│       ├── PaymentService/              # Port 5004: 1:1 Order Payment Processing Service
│       └── SaleReportService/           # Port 5005: Sales & Profit Analytics Reporting Service
└── README.md
```

---

## Database Setup

You can initialize the SQL Server databases in one of two ways:

### Option A: Automatic EF Core Code-First Seeding (Default)
When each microservice starts, EF Core automatically initializes the database tables and seeds sample data (users, drugs, suppliers, inventory stock, sample orders, and reports).

### Option B: Execute SQL Server Initialization Script
Execute the provided script in SQL Server Management Studio (SSMS) or Azure Data Studio:
```sql
-- File located at: scripts/InitDatabases.sql
```
This script creates all 5 databases (`Pharmacy_UserDB`, `Pharmacy_InventoryDB`, `Pharmacy_OrderDB`, `Pharmacy_PaymentDB`, `Pharmacy_SaleReportDB`) with primary keys, foreign keys, unique constraints, and seed data.

---

## How to Run & Test with Swagger

### Option 1: Visual Studio 2022
1. Open `PharmacyManagement.sln` in Visual Studio 2022.
2. Right-click the Solution in Solution Explorer -> **Configure Startup Projects...**
3. Select **Multiple startup projects** and set the Action for all 5 services (`AuthService`, `InventoryService`, `OrderService`, `PaymentService`, `SaleReportService`) to **Start**.
4. Press **F5** or click **Start**.
5. Each service will open its interactive **Swagger UI** in your browser:
   - Auth Service: [http://localhost:5001/swagger](http://localhost:5001/swagger)
   - Inventory Service: [http://localhost:5002/swagger](http://localhost:5002/swagger)
   - Order Service: [http://localhost:5003/swagger](http://localhost:5003/swagger)
   - Payment Service: [http://localhost:5004/swagger](http://localhost:5004/swagger)
   - SaleReport Service: [http://localhost:5005/swagger](http://localhost:5005/swagger)

### Option 2: Command Line (.NET CLI)
Open 5 terminal windows and run each service:
```bash
# Terminal 1: Auth Service
cd src/Services/AuthService
dotnet run --launch-profile http

# Terminal 2: Inventory Service
cd src/Services/InventoryService
dotnet run --launch-profile http

# Terminal 3: Order Service
cd src/Services/OrderService
dotnet run --launch-profile http

# Terminal 4: Payment Service
cd src/Services/PaymentService
dotnet run --launch-profile http

# Terminal 5: SaleReport Service
cd src/Services/SaleReportService
dotnet run --launch-profile http
```

### Option 3: Docker Compose
Run the entire solution including SQL Server with a single command:
```bash
docker-compose up -d --build
```

---

## Step-by-Step Swagger Testing Guide

### 1. Default Pre-Seeded Credentials

| Role | Email | Password | Pre-seeded ID |
|---|---|---|---|
| **Admin** | `admin@pharmacy.com` | `Admin@123` | `1` |
| **Doctor** | `doctor@pharmacy.com` | `Doctor@123` | `2` |

### 2. Testing Doctor Flow

1. Open **Auth Service** Swagger at `http://localhost:5001/swagger`.
2. Expand `POST /api/Auth/login` and authenticate with:
   ```json
   {
     "email": "doctor@pharmacy.com",
     "password": "Doctor@123"
   }
   ```
3. Copy the returned JWT `token`.
4. On any other microservice Swagger page, click the green **Authorize** lock button in the top right, paste `Bearer <token>`, and click **Authorize**.
5. In **Inventory Service** (`http://localhost:5002/swagger`), test:
   - `GET /api/Drugs`: Browse all available drugs.
   - `GET /api/Drugs/1`: Check details of Paracetamol.
6. In **Order Service** (`http://localhost:5003/swagger`), test:
   - `POST /api/Orders`: Buy drugs / place an order:
     ```json
     {
       "items": [
         {
           "drugId": 1,
           "drugName": "Paracetamol 500mg",
           "quantity": 2,
           "unitPrice": 9.99
         }
       ],
       "status": "Pending"
     }
     ```
   - Notice the inventory stock is automatically deducted in InventoryService!
   - `GET /api/Orders/my-orders`: View orders placed by this doctor.
7. In **Payment Service** (`http://localhost:5004/swagger`), test:
   - `POST /api/Payments`: Complete payment for the order:
     ```json
     {
       "orderId": 4,
       "amount": 19.98,
       "paymentMethod": "CreditCard"
     }
     ```

### 3. Testing Admin Flow

1. In **Auth Service** Swagger, login as `admin@pharmacy.com` with `Admin@123`.
2. Copy the Admin JWT token and click **Authorize** on the services.
3. In **Inventory Service** (`http://localhost:5002/swagger`):
   - `POST /api/Drugs`: Add new medications.
   - `PUT /api/Drugs/{id}`: Update drug details or price.
   - `DELETE /api/Drugs/{id}`: Delete a drug.
   - `POST /api/Suppliers`: Add a new wholesale supplier.
   - `POST /api/Inventory`: Add inventory stock with purchase price.
4. In **Order Service** (`http://localhost:5003/swagger`):
   - `GET /api/Orders`: View all doctor orders across the platform.
   - `GET /api/Orders/{id}/validate`: Check if order is valid.
   - `PUT /api/Orders/{id}/verify`: Verify the order (status transitions to `Verified`).
   - `PUT /api/Orders/{id}/pickup`: Hand over drugs and add to the `PickedUp` section.
   - `GET /api/Orders/picked-up`: View all fulfilled, picked-up orders.
5. In **SaleReport Service** (`http://localhost:5005/swagger`):
   - `POST /api/SaleReports/generate`: Generate Daily, Weekly, Monthly, or Yearly sales report.
   - `GET /api/SaleReports`: View historical financial summaries.
   - `GET /api/SaleReports/{id}/download`: Download CSV spreadsheet.
   - `GET /api/SaleReports/{id}/print`: Retrieve formatted printable receipt.
