@echo off
setlocal enabledelayedexpansion
title Pharmacy Management System - Intelligent Readiness Launcher
echo =====================================================================
echo  PHARMACY MANAGEMENT SYSTEM - .NET 10 LAUNCHER
echo  (5 Isolated Microservices + YARP API Gateway)
echo =====================================================================
echo.

:: 1. Preliminary check for SQL Server Express
echo [Check] Verifying local SQL Server Express service...
sc query MSSQL$SQLEXPRESS >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] SQL Server Express (MSSQL$SQLEXPRESS) service detected.
) else (
    echo [NOTE] SQL Server Express service not found under standard service name MSSQL$SQLEXPRESS.
    echo        If using another instance (e.g. localhost, (localdb)\MSSQLLocalDB), Ensure it is active.
)
echo.

:: 2. Launch AuthService (Port 5001)
echo [1/6] Starting AuthService on port 5001...
start "AuthService (Port 5001)" cmd /k "dotnet run --project src\Services\AuthService"
call :WaitForService 5001 "AuthService"
if !READY! neq 1 goto StartupFailed

:: 3. Launch InventoryService (Port 5002)
echo [2/6] Starting InventoryService on port 5002...
start "InventoryService (Port 5002)" cmd /k "dotnet run --project src\Services\InventoryService"
call :WaitForService 5002 "InventoryService"
if !READY! neq 1 goto StartupFailed

:: 4. Launch OrderService (Port 5003)
echo [3/6] Starting OrderService on port 5003...
start "OrderService (Port 5003)" cmd /k "dotnet run --project src\Services\OrderService"
call :WaitForService 5003 "OrderService"
if !READY! neq 1 goto StartupFailed

:: 5. Launch PaymentService (Port 5004)
echo [4/6] Starting PaymentService on port 5004...
start "PaymentService (Port 5004)" cmd /k "dotnet run --project src\Services\PaymentService"
call :WaitForService 5004 "PaymentService"
if !READY! neq 1 goto StartupFailed

:: 6. Launch SaleReportService (Port 5005)
echo [5/6] Starting SaleReportService on port 5005...
start "SaleReportService (Port 5005)" cmd /k "dotnet run --project src\Services\SaleReportService"
call :WaitForService 5005 "SaleReportService"
if !READY! neq 1 goto StartupFailed

:: 7. Launch YARP API Gateway (Port 5000)
echo [6/6] Starting YARP API Gateway on port 5000...
start "ApiGateway (Port 5000)" cmd /k "dotnet run --project src\ApiGateway"
call :WaitForService 5000 "ApiGateway"
if !READY! neq 1 goto StartupFailed

echo.
echo =====================================================================
echo  ALL 5 MICROSERVICES AND YARP GATEWAY ARE ONLINE AND READY!
echo  OPENING UNIFIED SWAGGER AT: http://localhost:5000/
echo =====================================================================
start http://localhost:5000
start http://localhost:5001/swagger
start http://localhost:5002/swagger
start http://localhost:5003/swagger
start http://localhost:5004/swagger
start http://localhost:5005/swagger

echo.
echo Press any key to exit this launcher window (microservices will continue running).
pause >nul
exit /b 0

:: =====================================================================
:: Subroutine: WaitForService <Port> <ServiceName>
:: Uses curl.exe to probe /health/ready with retry limit
:: =====================================================================
:WaitForService
set PORT=%1
set SNAME=%2
set READY=0
set ATTEMPTS=0
set MAX_ATTEMPTS=25

echo       Waiting for %SNAME% on port %PORT% (/health/ready)...
:RetryLoop
timeout /t 1 >nul 2>&1
set /a ATTEMPTS+=1

:: Probe readiness endpoint
curl.exe -s -f http://localhost:%PORT%/health/ready >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo       [OK] %SNAME% is READY on port %PORT%!
    set READY=1
    exit /b 0
)

if !ATTEMPTS! lss !MAX_ATTEMPTS! goto RetryLoop

echo       [TIMEOUT] %SNAME% did not respond on port %PORT% within !MAX_ATTEMPTS! seconds.
echo                 Please check the "%SNAME%" terminal window for migration or startup errors.
set READY=0
exit /b 1

:StartupFailed
echo.
echo =====================================================================
echo  STARTUP FAILED: A microservice failed readiness checks.
echo  Please inspect the corresponding terminal window for details.
echo =====================================================================
pause
exit /b 1
