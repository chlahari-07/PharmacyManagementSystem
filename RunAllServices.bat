@echo off
title Pharmacy Management System - Launcher
echo =====================================================================
echo  STARTING PHARMACY MANAGEMENT SYSTEM (5 MICROSERVICES)
echo =====================================================================
echo.

echo [1/5] Launching AuthService on port 5001...
start "AuthService (Port 5001)" cmd /k "dotnet run --project src\Services\AuthService"

timeout /t 2 >nul

echo [2/5] Launching InventoryService on port 5002...
start "InventoryService (Port 5002)" cmd /k "dotnet run --project src\Services\InventoryService"

timeout /t 2 >nul

echo [3/5] Launching OrderService on port 5003...
start "OrderService (Port 5003)" cmd /k "dotnet run --project src\Services\OrderService"

timeout /t 2 >nul

echo [4/5] Launching PaymentService on port 5004...
start "PaymentService (Port 5004)" cmd /k "dotnet run --project src\Services\PaymentService"

timeout /t 2 >nul

echo [5/5] Launching SaleReportService on port 5005...
start "SaleReportService (Port 5005)" cmd /k "dotnet run --project src\Services\SaleReportService"

timeout /t 3 >nul

echo.
echo =====================================================================
echo  ALL 5 SERVICES LAUNCHED! OPENING SWAGGER TESTING DASHBOARDS...
echo =====================================================================
start http://localhost:5001/swagger
start http://localhost:5002/swagger
start http://localhost:5003/swagger
start http://localhost:5004/swagger
start http://localhost:5005/swagger

echo.
echo Press any key to exit this launcher window (microservices will keep running).
pause >nul
