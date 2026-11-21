-- =========================================================================================
-- PHARMACY MANAGEMENT SYSTEM - COMPLETE SQL SERVER INITIALIZATION SCRIPT
-- 5 Microservices Databases with Tables, Primary Keys, Foreign Keys, Indexes & Seed Data
-- Aligned with Low-Level Design (LLD) Specifications and Prompt Requirements
-- =========================================================================================

-- =========================================================================================
-- 1. AUTH SERVICE DATABASE (User DB)
-- =========================================================================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'Pharmacy_UserDB')
BEGIN
    CREATE DATABASE [Pharmacy_UserDB];
END
GO

USE [Pharmacy_UserDB];
GO

IF OBJECT_ID(N'dbo.Users', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Users] (
        [UserId]       INT IDENTITY(1,1) NOT NULL,
        [Name]         NVARCHAR(100) NOT NULL,
        [Email]        NVARCHAR(150) NOT NULL,
        [PhoneNumber]  NVARCHAR(20)  NOT NULL,
        [PasswordHash] NVARCHAR(255) NOT NULL,
        [Role]         NVARCHAR(20)  NOT NULL, -- 'Admin' or 'Doctor'
        [IsActive]     BIT           NOT NULL CONSTRAINT DF_Users_IsActive DEFAULT (1),
        [CreatedDate]  DATETIME2(7)  NOT NULL CONSTRAINT DF_Users_CreatedDate DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT PK_Users PRIMARY KEY CLUSTERED ([UserId] ASC),
        CONSTRAINT UQ_Users_Email UNIQUE NONCLUSTERED ([Email] ASC)
    );

    CREATE NONCLUSTERED INDEX IX_Users_Role ON [dbo].[Users] ([Role] ASC);

    -- Seed Initial Admin and Doctor Users
    -- Admin is strictly pre-seeded (Admin cannot register; can only log in)
    -- Password for Admin: 'Admin@123'
    -- Password for Doctor: 'Doctor@123'
    INSERT INTO [dbo].[Users] ([Name], [Email], [PhoneNumber], [PasswordHash], [Role], [IsActive], [CreatedDate])
    VALUES 
    (N'System Administrator', N'admin@pharmacy.com', N'+1234567890', 
     N'OSRURIaBMPUBllVO4w7cvpsa+68ksrQugHPf9n5h+BLF9RP+mtYdcJY9a+zogOYM', N'Admin', 1, SYSUTCDATETIME()),
    (N'Dr. Robert Smith', N'doctor@pharmacy.com', N'+1987654321', 
     N'w6+goA5m1GDOi2lH3Y/mzVTtjz4e+OrR4RJXNbUh8k0O64N8NxDfubkLJqI1xT9y', N'Doctor', 1, SYSUTCDATETIME());
END
GO

-- =========================================================================================
-- 2. INVENTORY SERVICE DATABASE (Inventory DB)
-- =========================================================================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'Pharmacy_InventoryDB')
BEGIN
    CREATE DATABASE [Pharmacy_InventoryDB];
END
GO

USE [Pharmacy_InventoryDB];
GO

-- a) Drugs Table
IF OBJECT_ID(N'dbo.Drugs', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Drugs] (
        [DrugId]               INT IDENTITY(1,1) NOT NULL,
        [DrugName]             NVARCHAR(150)     NOT NULL,
        [Description]          NVARCHAR(500)     NULL,
        [Category]             NVARCHAR(100)     NULL,
        [Price]                DECIMAL(18,2)     NOT NULL, -- Selling Price
        [ExpiryDate]           DATETIME2(7)      NOT NULL,
        [Quantity]             INT               NOT NULL,
        [MinimumStockQuantity] INT               NOT NULL CONSTRAINT DF_Drugs_MinimumStockQuantity DEFAULT (20),
        [IsAvailable]          BIT               NOT NULL CONSTRAINT DF_Drugs_IsAvailable DEFAULT (1),
        [CreatedDate]          DATETIME2(7)      NOT NULL CONSTRAINT DF_Drugs_CreatedDate DEFAULT (SYSUTCDATETIME()),
        [UpdatedDate]          DATETIME2(7)      NULL,
        CONSTRAINT PK_Drugs PRIMARY KEY CLUSTERED ([DrugId] ASC)
    );

    CREATE NONCLUSTERED INDEX IX_Drugs_IsAvailable ON [dbo].[Drugs] ([IsAvailable], [Quantity]);
    CREATE NONCLUSTERED INDEX IX_Drugs_LowStock ON [dbo].[Drugs] ([Quantity], [MinimumStockQuantity]);
    CREATE NONCLUSTERED INDEX IX_Drugs_ExpiryDate ON [dbo].[Drugs] ([ExpiryDate] ASC);
END
GO

-- b) Supplier Table
IF OBJECT_ID(N'dbo.Suppliers', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Suppliers] (
        [SupplierId]   INT IDENTITY(1,1) NOT NULL,
        [SupplierName] NVARCHAR(150)     NOT NULL,
        [Email]        NVARCHAR(150)     NOT NULL,
        [PhoneNumber]  NVARCHAR(20)      NOT NULL,
        [Address]      NVARCHAR(300)     NOT NULL,
        CONSTRAINT PK_Suppliers PRIMARY KEY CLUSTERED ([SupplierId] ASC)
    );
END
GO

-- c) Inventory Table (Linking Supplier & Drug)
-- Supplier to Inventory (1:M), Drug to Inventory (1:M)
IF OBJECT_ID(N'dbo.Inventory', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Inventory] (
        [InventoryId]      INT IDENTITY(1,1) NOT NULL,
        [SupplierId]       INT               NOT NULL,
        [DrugId]           INT               NOT NULL,
        [PurchasePrice]    DECIMAL(18,2)     NOT NULL,
        [QuantitySupplied] INT               NOT NULL,
        [SupplyDate]       DATETIME2(7)      NOT NULL CONSTRAINT DF_Inventory_SupplyDate DEFAULT (SYSUTCDATETIME()),
        [BatchNumber]      NVARCHAR(100)     NULL,
        [Notes]            NVARCHAR(500)     NULL,
        CONSTRAINT PK_Inventory PRIMARY KEY CLUSTERED ([InventoryId] ASC),
        CONSTRAINT FK_Inventory_Suppliers FOREIGN KEY ([SupplierId]) REFERENCES [dbo].[Suppliers] ([SupplierId]),
        CONSTRAINT FK_Inventory_Drugs FOREIGN KEY ([DrugId]) REFERENCES [dbo].[Drugs] ([DrugId])
    );

    CREATE NONCLUSTERED INDEX IX_Inventory_SupplierId ON [dbo].[Inventory] ([SupplierId]);
    CREATE NONCLUSTERED INDEX IX_Inventory_DrugId ON [dbo].[Inventory] ([DrugId]);

    -- Seed Suppliers
    INSERT INTO [dbo].[Suppliers] ([SupplierName], [Email], [PhoneNumber], [Address])
    VALUES 
    (N'Apex Pharma Logistics', N'contact@apexpharma.com', N'+1555123456', N'100 Medical Boulevard, Suite 400, Chicago, IL'),
    (N'BioCare Health Supplies', N'sales@biocare.com', N'+1555987654', N'742 Healthcare Parkway, Boston, MA');

    -- Seed Drugs
    INSERT INTO [dbo].[Drugs] ([DrugName], [Description], [Category], [Price], [ExpiryDate], [Quantity], [MinimumStockQuantity], [IsAvailable])
    VALUES 
    (N'Paracetamol 500mg', N'Pain reliever and a fever reducer (Acetaminophen)', N'Analgesics', 9.99, DATEADD(YEAR, 2, SYSUTCDATETIME()), 200, 20, 1),
    (N'Amoxicillin 250mg', N'Broad-spectrum penicillin antibiotic', N'Antibiotics', 18.50, DATEADD(YEAR, 1, SYSUTCDATETIME()), 150, 25, 1),
    (N'Ibuprofen 400mg', N'Nonsteroidal anti-inflammatory drug (NSAID)', N'Analgesics', 12.00, DATEADD(MONTH, 18, SYSUTCDATETIME()), 300, 30, 1),
    (N'Metformin 500mg', N'Oral diabetes medicine for blood sugar control', N'Antidiabetic', 15.75, DATEADD(YEAR, 2, SYSUTCDATETIME()), 120, 20, 1),
    (N'Azithromycin 500mg', N'Macrolide antibiotic for bacterial infections', N'Antibiotics', 24.50, DATEADD(MONTH, 8, SYSUTCDATETIME()), 8, 20, 1),
    (N'Cough Syrup Dx 100ml', N'Antitussive cough suppressant', N'Cough & Cold', 8.25, DATEADD(DAY, -15, SYSUTCDATETIME()), 15, 10, 0);

    -- Seed Inventory Entries
    INSERT INTO [dbo].[Inventory] ([SupplierId], [DrugId], [PurchasePrice], [QuantitySupplied], [SupplyDate], [BatchNumber], [Notes])
    VALUES 
    (1, 1, 5.50, 200, DATEADD(DAY, -30, SYSUTCDATETIME()), N'BATCH-PCM-2026', N'Standard replenishment shipment'),
    (1, 2, 11.00, 150, DATEADD(DAY, -20, SYSUTCDATETIME()), N'BATCH-AMX-2026', N'Antibiotic restocking'),
    (2, 3, 7.00, 300, DATEADD(DAY, -15, SYSUTCDATETIME()), N'BATCH-IBU-2026', N'Anti-inflammatory stock'),
    (2, 4, 9.20, 120, DATEADD(DAY, -10, SYSUTCDATETIME()), N'BATCH-MET-2026', N'Diabetes care shipment');
END
GO

-- =========================================================================================
-- 3. ORDER SERVICE DATABASE (Order DB)
-- =========================================================================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'Pharmacy_OrderDB')
BEGIN
    CREATE DATABASE [Pharmacy_OrderDB];
END
GO

USE [Pharmacy_OrderDB];
GO

-- a) Order Table
-- User to Order has (1:M) -> DoctorID links to Users.UserId
IF OBJECT_ID(N'dbo.Orders', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Orders] (
        [OrderId]     INT IDENTITY(1,1) NOT NULL,
        [DoctorID]    INT               NOT NULL, -- Logical FK from User table
        [OrderDate]   DATETIME2(7)      NOT NULL CONSTRAINT DF_Orders_OrderDate DEFAULT (SYSUTCDATETIME()),
        [TotalAmount] DECIMAL(18,2)     NOT NULL,
        [Status]      NVARCHAR(20)      NOT NULL, -- Cart / Pending / Verified / PickedUp / Cancelled
        CONSTRAINT PK_Orders PRIMARY KEY CLUSTERED ([OrderId] ASC)
    );

    CREATE NONCLUSTERED INDEX IX_Orders_DoctorID ON [dbo].[Orders] ([DoctorID]);
    CREATE NONCLUSTERED INDEX IX_Orders_Status ON [dbo].[Orders] ([Status]);
END
GO

-- b) OrderItem Table
-- Order to OrderItem has (1:M), Drug to OrderItem has (1:M)
IF OBJECT_ID(N'dbo.OrderItems', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[OrderItems] (
        [OrderItemId] INT IDENTITY(1,1) NOT NULL,
        [OrderId]     INT               NOT NULL, -- FK to Orders
        [DrugId]      INT               NOT NULL, -- Logical FK to Drugs table
        [DrugName]    NVARCHAR(150)     NULL,
        [Quantity]    INT               NOT NULL,
        [UnitPrice]   DECIMAL(18,2)     NOT NULL,
        CONSTRAINT PK_OrderItems PRIMARY KEY CLUSTERED ([OrderItemId] ASC),
        CONSTRAINT FK_OrderItems_Orders FOREIGN KEY ([OrderId]) REFERENCES [dbo].[Orders] ([OrderId]) ON DELETE CASCADE
    );

    CREATE NONCLUSTERED INDEX IX_OrderItems_OrderId ON [dbo].[OrderItems] ([OrderId]);
    CREATE NONCLUSTERED INDEX IX_OrderItems_DrugId ON [dbo].[OrderItems] ([DrugId]);

    -- Seed Sample Orders
    INSERT INTO [dbo].[Orders] ([DoctorID], [OrderDate], [TotalAmount], [Status])
    VALUES 
    (2, DATEADD(DAY, -2, SYSUTCDATETIME()), 48.47, N'Verified'),
    (2, DATEADD(DAY, -1, SYSUTCDATETIME()), 24.00, N'Pending'),
    (2, DATEADD(DAY, -5, SYSUTCDATETIME()), 31.50, N'PickedUp');

    INSERT INTO [dbo].[OrderItems] ([OrderId], [DrugId], [DrugName], [Quantity], [UnitPrice])
    VALUES 
    (1, 1, N'Paracetamol 500mg', 3, 9.99),
    (1, 2, N'Amoxicillin 250mg', 1, 18.50),
    (2, 3, N'Ibuprofen 400mg', 2, 12.00),
    (3, 4, N'Metformin 500mg', 2, 15.75);
END
GO

-- =========================================================================================
-- 4. PAYMENT SERVICE DATABASE (Payment DB)
-- =========================================================================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'Pharmacy_PaymentDB')
BEGIN
    CREATE DATABASE [Pharmacy_PaymentDB];
END
GO

USE [Pharmacy_PaymentDB];
GO

-- Payment Table
-- Order to Payment has (1:1) -> Unique constraint on OrderId
IF OBJECT_ID(N'dbo.Payments', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Payments] (
        [PaymentId]            INT IDENTITY(1,1) NOT NULL,
        [OrderId]              INT               NOT NULL, -- Logical FK from Order table (1:1)
        [Amount]               DECIMAL(18,2)     NOT NULL,
        [PaymentDate]          DATETIME2(7)      NOT NULL CONSTRAINT DF_Payments_PaymentDate DEFAULT (SYSUTCDATETIME()),
        [PaymentMethod]        NVARCHAR(50)      NOT NULL, -- CreditCard / DebitCard / UPI / NetBanking / Cash
        [PaymentStatus]        NVARCHAR(20)      NOT NULL, -- Pending / Completed / Failed
        [TransactionReference] NVARCHAR(100)     NULL,
        CONSTRAINT PK_Payments PRIMARY KEY CLUSTERED ([PaymentId] ASC),
        CONSTRAINT UQ_Payments_OrderId UNIQUE NONCLUSTERED ([OrderId] ASC)
    );

    CREATE NONCLUSTERED INDEX IX_Payments_Status ON [dbo].[Payments] ([PaymentStatus]);

    -- Seed Sample Payments
    INSERT INTO [dbo].[Payments] ([OrderId], [Amount], [PaymentDate], [PaymentMethod], [PaymentStatus], [TransactionReference])
    VALUES 
    (1, 48.47, DATEADD(DAY, -2, SYSUTCDATETIME()), N'CreditCard', N'Completed', N'TXN-A83F91B2C4D5'),
    (3, 31.50, DATEADD(DAY, -5, SYSUTCDATETIME()), N'UPI', N'Completed', N'TXN-B94E02C3D5E6');
END
GO

-- =========================================================================================
-- 5. SALE REPORT SERVICE DATABASE (SaleReport DB)
-- =========================================================================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'Pharmacy_SaleReportDB')
BEGIN
    CREATE DATABASE [Pharmacy_SaleReportDB];
END
GO

USE [Pharmacy_SaleReportDB];
GO

-- SaleReport Table (Standalone aggregated entity)
IF OBJECT_ID(N'dbo.SaleReports', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SaleReports] (
        [SaleReportId]  INT IDENTITY(1,1) NOT NULL,
        [ReportType]    NVARCHAR(20)      NOT NULL, -- Daily / Weekly / Monthly / Yearly
        [FromDate]      DATETIME2(7)      NOT NULL,
        [ToDate]        DATETIME2(7)      NOT NULL,
        [TotalOrders]   INT               NOT NULL,
        [TotalRevenue]  DECIMAL(18,2)     NOT NULL,
        [GeneratedDate] DATETIME2(7)      NOT NULL CONSTRAINT DF_SaleReports_GeneratedDate DEFAULT (SYSUTCDATETIME()),
        [Profit]        DECIMAL(18,2)     NOT NULL,
        CONSTRAINT PK_SaleReports PRIMARY KEY CLUSTERED ([SaleReportId] ASC)
    );

    CREATE NONCLUSTERED INDEX IX_SaleReports_ReportType ON [dbo].[SaleReports] ([ReportType]);
    CREATE NONCLUSTERED INDEX IX_SaleReports_GeneratedDate ON [dbo].[SaleReports] ([GeneratedDate]);

    -- Seed Sample Reports
    INSERT INTO [dbo].[SaleReports] ([ReportType], [FromDate], [ToDate], [TotalOrders], [TotalRevenue], [GeneratedDate], [Profit])
    VALUES 
    (N'Daily', CAST(SYSUTCDATETIME() AS DATE), SYSUTCDATETIME(), 12, 1540.00, SYSUTCDATETIME(), 462.00),
    (N'Weekly', DATEADD(DAY, -7, CAST(SYSUTCDATETIME() AS DATE)), SYSUTCDATETIME(), 84, 10850.50, SYSUTCDATETIME(), 3255.15),
    (N'Monthly', DATEADD(MONTH, -1, CAST(SYSUTCDATETIME() AS DATE)), SYSUTCDATETIME(), 340, 45200.00, SYSUTCDATETIME(), 14464.00);
END
GO

PRINT '====================================================================='
PRINT 'All 5 Pharmacy Management Microservices Databases initialized successfully!'
PRINT '====================================================================='
