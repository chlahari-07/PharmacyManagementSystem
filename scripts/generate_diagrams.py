import os
import math
from PIL import Image, ImageDraw, ImageFont

# Set output directories
OUT_DIR_WORKSPACE = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"
OUT_DIR_ARTIFACT = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\diagrams"

os.makedirs(OUT_DIR_WORKSPACE, exist_ok=True)
os.makedirs(OUT_DIR_ARTIFACT, exist_ok=True)

# Fonts
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
FONT_HEADER = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
FONT_SUBHEADER = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
FONT_BODY_BOLD = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
FONT_BODY = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
FONT_SMALL = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
FONT_SMALL_BOLD = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
FONT_TINY = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)

# Professional Colors Palette
CLR_BG = (248, 250, 252)          # Slate 50
CLR_CARD_BG = (255, 255, 255)     # White
CLR_HEADER_BG = (15, 23, 42)      # Slate 900
CLR_HEADER_TEXT = (255, 255, 255) # White
CLR_SUBHEADER_TEXT = (148, 163, 184) # Slate 400

CLR_NAVY = (30, 41, 59)          # Slate 800
CLR_BORDER = (203, 213, 225)      # Slate 300
CLR_BORDER_LIGHT = (226, 232, 240) # Slate 200

CLR_BLUE_PRIMARY = (37, 99, 235)  # Blue 600
CLR_BLUE_LIGHT = (239, 246, 255)  # Blue 50
CLR_BLUE_DARK = (29, 78, 216)     # Blue 700

CLR_INDIGO = (79, 70, 229)        # Indigo 600
CLR_INDIGO_LIGHT = (238, 242, 255)# Indigo 50

CLR_TEAL = (14, 116, 144)         # Cyan 700
CLR_TEAL_LIGHT = (236, 254, 255)  # Cyan 50

CLR_EMERALD = (5, 150, 105)       # Emerald 600
CLR_EMERALD_LIGHT = (236, 253, 245)# Emerald 50

CLR_AMBER = (217, 119, 6)         # Amber 600
CLR_AMBER_LIGHT = (254, 243, 199) # Amber 50

CLR_ROSE = (225, 29, 72)          # Rose 600
CLR_ROSE_LIGHT = (255, 241, 242)  # Rose 50

CLR_TEXT_DARK = (15, 23, 42)      # Slate 900
CLR_TEXT_MUTED = (100, 116, 139)  # Slate 500
CLR_TEXT_LIGHT = (255, 255, 255)  # White

def draw_top_banner(draw, width, title, subtitle):
    # Top banner background
    draw.rectangle([0, 0, width, 110], fill=CLR_HEADER_BG)
    # Accent stripe
    draw.rectangle([0, 106, width, 110], fill=CLR_BLUE_PRIMARY)
    # Title
    draw.text((40, 22), title, font=FONT_TITLE, fill=CLR_HEADER_TEXT)
    # Subtitle
    draw.text((42, 70), subtitle, font=FONT_SUBTITLE, fill=CLR_SUBHEADER_TEXT)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_badge(draw, x, y, text, bg_color, text_color, font=FONT_SMALL_BOLD):
    bbox = font.getbbox(text)
    w = (bbox[2] - bbox[0]) + 16
    h = (bbox[3] - bbox[1]) + 8
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg_color)
    draw.text((x + 8, y + 3), text, font=font, fill=text_color)
    return w, h

def draw_arrow(draw, start, end, color=CLR_NAVY, width=2, label=None, label_side="top"):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    
    # Arrow head
    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 10
    head_angle = math.pi / 6
    
    p1 = (x2 - head_len * math.cos(angle - head_angle), y2 - head_len * math.sin(angle - head_angle))
    p2 = (x2 - head_len * math.cos(angle + head_angle), y2 - head_len * math.sin(angle + head_angle))
    draw.polygon([(x2, y2), p1, p2], fill=color)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        if label_side == "top":
            draw.text((mx - 40, my - 20), label, font=FONT_TINY, fill=color)
        elif label_side == "bottom":
            draw.text((mx - 40, my + 6), label, font=FONT_TINY, fill=color)
        elif label_side == "right":
            draw.text((mx + 8, my - 8), label, font=FONT_TINY, fill=color)
        elif label_side == "left":
            draw.text((mx - 80, my - 8), label, font=FONT_TINY, fill=color)

def save_image(img, filename):
    p1 = os.path.join(OUT_DIR_WORKSPACE, filename)
    p2 = os.path.join(OUT_DIR_ARTIFACT, filename)
    img.save(p1, "JPEG", quality=95)
    img.save(p2, "JPEG", quality=95)
    print(f"Saved: {p1}")

print("Helper primitives defined successfully.")

# ==============================================================================
# 1. SOLUTION ARCHITECTURE DIAGRAM
# ==============================================================================
def generate_solution_diagram():
    W, H = 2500, 1750
    img = Image.new("RGB", (W, H), CLR_BG)
    draw = ImageDraw.Draw(img)
    
    draw_top_banner(draw, W, 
                    "PHARMACY MANAGEMENT SYSTEM - SOLUTION ARCHITECTURE DIAGRAM",
                    "Microservices Topology: ASP.NET Core Web APIs | EF Core 8 & LINQ | Dedicated SQL Server DBs | Swagger UI")

    # Section 1: Client & Testing Layer
    draw_rounded_rect(draw, (40, 140, 2460, 360), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 155, "CLIENTS & TESTING LAYER", CLR_NAVY, CLR_TEXT_LIGHT)
    
    # Client cards
    clients = [
        ("Doctor User", "Browser / Clinic Portal\nToken-based Authentication\nBrowses drugs, places orders", CLR_TEAL_LIGHT, CLR_TEAL, 80),
        ("Admin User", "Operations & Management\nUser role: Admin\nVerifies orders, manages stock", CLR_INDIGO_LIGHT, CLR_INDIGO, 560),
        ("Swagger / OpenAPI 3.0", "Interactive Web API Documentation\nConfigured on Ports 5001 - 5005\nJWT Lock Authorization built-in", CLR_EMERALD_LIGHT, CLR_EMERALD, 1040),
        ("JWT Security Gateway", "JSON Web Token Validation\nHMAC-SHA256 Signing Key\nRole-Based Claims (Admin, Doctor)", CLR_AMBER_LIGHT, CLR_AMBER, 1520),
        ("Inter-Service HTTP", "Typed HttpClient Extensions\nStock Deduction REST Calls\nOrder Analytics Reporting Calls", CLR_BLUE_LIGHT, CLR_BLUE_PRIMARY, 2000)
    ]
    for title, desc, bg, border, x in clients:
        draw_rounded_rect(draw, (x, 195, x + 420, 335), 12, bg, border, 2)
        draw.text((x + 20, 210), title, font=FONT_HEADER, fill=border)
        lines = desc.split("\n")
        for i, line in enumerate(lines):
            draw.text((x + 20, 250 + i * 24), line, font=FONT_BODY, fill=CLR_TEXT_DARK)

    # Section 2: Microservices Layer (5 Microservices)
    draw_rounded_rect(draw, (40, 400, 2460, 1140), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 415, "DISTRIBUTED MICROSERVICES LAYER (ASP.NET CORE WEB APIS WITH INTERNAL MVC PATTERN)", CLR_BLUE_PRIMARY, CLR_TEXT_LIGHT)

    services = [
        {
            "name": "1. Auth Service",
            "port": "PORT 5001",
            "db": "Pharmacy_UserDB",
            "color": CLR_AMBER,
            "light": CLR_AMBER_LIGHT,
            "ctrl": "AuthController",
            "models": "User Entity (PK UserId)",
            "methods": ["POST /api/auth/register", "POST /api/auth/login", "GET /api/auth/profile", "GET /api/auth/validate-doctor", "GET /api/auth/users"],
            "mvc": "Controller -> AuthService -> UserRepository -> AuthDbContext",
            "x": 80
        },
        {
            "name": "2. Inventory Service",
            "port": "PORT 5002",
            "db": "Pharmacy_InventoryDB",
            "color": CLR_TEAL,
            "light": CLR_TEAL_LIGHT,
            "ctrl": "Drugs / Suppliers / Inventory",
            "models": "Drugs, Suppliers, Inventory",
            "methods": ["GET/POST/PUT/DEL /api/drugs", "GET/POST/PUT/DEL /api/suppliers", "POST /api/drugs/deduct-stock", "GET/POST /api/inventory"],
            "mvc": "Controllers -> Services -> Repositories -> InventoryDbContext",
            "x": 560
        },
        {
            "name": "3. Order Service",
            "port": "PORT 5003",
            "db": "Pharmacy_OrderDB",
            "color": CLR_BLUE_PRIMARY,
            "light": CLR_BLUE_LIGHT,
            "ctrl": "OrdersController",
            "models": "Order, OrderItem (1:M)",
            "methods": ["POST /api/orders (Buy Drugs)", "GET /api/orders/my-orders", "GET /api/orders (All Doctor Orders)", "PUT /api/orders/{id}/verify", "PUT /api/orders/{id}/pickup"],
            "mvc": "OrdersController -> OrderService -> InventoryClient -> DbContext",
            "x": 1040
        },
        {
            "name": "4. Payment Service",
            "port": "PORT 5004",
            "db": "Pharmacy_PaymentDB",
            "color": CLR_EMERALD,
            "light": CLR_EMERALD_LIGHT,
            "ctrl": "PaymentsController",
            "models": "Payment Entity (1:1 with Order)",
            "methods": ["POST /api/payments (Process Payment)", "GET /api/payments/order/{orderId}", "GET /api/payments/{id}", "GET /api/payments (All Payments)", "PUT /api/payments/{id}/status"],
            "mvc": "PaymentsController -> PaymentService -> PaymentRepo -> DbContext",
            "x": 1520
        },
        {
            "name": "5. SaleReport Service",
            "port": "PORT 5005",
            "db": "Pharmacy_SaleReportDB",
            "color": CLR_INDIGO,
            "light": CLR_INDIGO_LIGHT,
            "ctrl": "SaleReportsController",
            "models": "SaleReport Entity",
            "methods": ["POST /api/salereports/generate", "GET /api/salereports", "GET /api/salereports/{id}", "GET /api/salereports/{id}/download", "GET /api/salereports/{id}/print"],
            "mvc": "SaleReportsController -> ReportService -> OrderClient -> DbContext",
            "x": 2000
        }
    ]

    for svc in services:
        x = svc["x"]
        # Service Container Card
        draw_rounded_rect(draw, (x, 460, x + 420, 1100), 12, CLR_CARD_BG, svc["color"], 2)
        # Header banner inside card
        draw_rounded_rect(draw, (x, 460, x + 420, 520), 12, svc["color"])
        draw.rectangle([x, 500, x + 420, 520], fill=svc["color"])
        draw.text((x + 15, 475), svc["name"], font=FONT_HEADER, fill=CLR_TEXT_LIGHT)
        draw_badge(draw, x + 310, 475, svc["port"], CLR_CARD_BG, svc["color"], FONT_TINY)

        # MVC Architecture Box
        draw_rounded_rect(draw, (x + 15, 535, x + 405, 620), 8, svc["light"], svc["color"], 1)
        draw.text((x + 25, 545), "MVC Architecture Inside Service:", font=FONT_SMALL_BOLD, fill=svc["color"])
        draw.text((x + 25, 570), f"Controllers: {svc['ctrl']}", font=FONT_SMALL, fill=CLR_TEXT_DARK)
        draw.text((x + 25, 592), f"Domain Models: {svc['models']}", font=FONT_SMALL, fill=CLR_TEXT_DARK)

        # API Endpoints List
        draw.text((x + 15, 635), "RESTful Web API Endpoints:", font=FONT_SMALL_BOLD, fill=CLR_NAVY)
        for idx, m in enumerate(svc["methods"]):
            draw_rounded_rect(draw, (x + 15, 665 + idx * 42, x + 405, 698 + idx * 42), 6, (241, 245, 249), CLR_BORDER_LIGHT, 1)
            draw.text((x + 25, 673 + idx * 42), m, font=FONT_TINY, fill=CLR_TEXT_DARK)

        # Technology Stack badges inside card
        draw_badge(draw, x + 15, 895, "ASP.NET Core 8", CLR_BLUE_LIGHT, CLR_BLUE_PRIMARY, FONT_TINY)
        draw_badge(draw, x + 130, 895, "EF Core & LINQ", CLR_INDIGO_LIGHT, CLR_INDIGO, FONT_TINY)
        draw_badge(draw, x + 245, 895, "Swagger Docs", CLR_EMERALD_LIGHT, CLR_EMERALD, FONT_TINY)

        # Pipeline diagram
        draw_rounded_rect(draw, (x + 15, 940, x + 405, 1080), 8, (248, 250, 252), CLR_BORDER, 1)
        draw.text((x + 25, 950), "Internal MVC Pipeline Flow:", font=FONT_SMALL_BOLD, fill=CLR_NAVY)
        draw.text((x + 25, 980), "[Controller] (REST Request / Validation)", font=FONT_SMALL, fill=CLR_TEXT_DARK)
        draw.text((x + 25, 1005), "    ↓  (DTOs / Business Logic)", font=FONT_TINY, fill=CLR_TEXT_MUTED)
        draw.text((x + 25, 1025), "[Service] -> [Repository] (LINQ Queries)", font=FONT_SMALL, fill=CLR_TEXT_DARK)
        draw.text((x + 25, 1050), "    ↓  [DbContext] -> EF Core Provider", font=FONT_SMALL, fill=CLR_BLUE_PRIMARY)

    # Inter-service arrows
    # OrderService -> InventoryService (Stock Deduction)
    draw_arrow(draw, (1040, 750), (980, 750), CLR_ROSE, 3, "Stock Deduction", "top")
    # SaleReportService -> OrderService (Fetch Orders)
    draw_arrow(draw, (2000, 750), (1460, 750), CLR_INDIGO, 3, "Query Orders", "top")

    # Section 3: Database Layer (5 Dedicated SQL Server Databases)
    draw_rounded_rect(draw, (40, 1180, 2460, 1690), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 1195, "DEDICATED SQL SERVER DATABASE STORAGE LAYER (BOUNDED CONTEXTS)", CLR_TEAL, CLR_TEXT_LIGHT)

    dbs = [
        ("Pharmacy_UserDB", "Users Table", "UserId (PK), Name, Email (UQ), Phone,\nPasswordHash, Role, IsActive, CreatedDate", 80),
        ("Pharmacy_InventoryDB", "Drugs, Suppliers, Inventory Tables", "Drugs (PK DrugId), Suppliers (PK SupplierId)\nInventory (PK InvId, FK SupplierId, FK DrugId)\nSupplier->Inv (1:M), Drug->Inv (1:M)", 560),
        ("Pharmacy_OrderDB", "Orders, OrderItems Tables", "Orders (PK OrderId, DoctorID FK, Status)\nOrderItems (PK OrderItemId, FK OrderId, FK DrugId)\nUser->Order (1:M), Order->OrderItem (1:M)", 1040),
        ("Pharmacy_PaymentDB", "Payments Table", "PaymentId (PK), OrderId (UQ - 1:1),\nAmount, PaymentDate, PaymentMethod, Status\nOrder to Payment has (1:1 Relationship)", 1520),
        ("Pharmacy_SaleReportDB", "SaleReports Table", "SaleReportId (PK), ReportType (Daily/Wk/Mo/Yr)\nFromDate, ToDate, TotalOrders, Revenue, Profit\nStandalone Financial Reporting Storage", 2000)
    ]

    for title, tables, desc, x in dbs:
        # DB Card
        draw_rounded_rect(draw, (x, 1240, x + 420, 1640), 12, (240, 249, 255), CLR_TEAL, 2)
        # Top cylinder cap representation
        draw.ellipse([x + 30, 1255, x + 390, 1295], fill=CLR_TEAL)
        draw.text((x + 80, 1265), title, font=FONT_HEADER, fill=CLR_TEXT_LIGHT)

        draw_rounded_rect(draw, (x + 20, 1315, x + 400, 1365), 6, CLR_CARD_BG, CLR_BORDER, 1)
        draw.text((x + 30, 1330), tables, font=FONT_SMALL_BOLD, fill=CLR_NAVY)

        lines = desc.split("\n")
        for i, l in enumerate(lines):
            draw.text((x + 25, 1385 + i * 26), l, font=FONT_SMALL, fill=CLR_TEXT_DARK)

        draw_badge(draw, x + 25, 1500, "SQL Server 2022 / LocalDB", CLR_TEAL_LIGHT, CLR_TEAL, FONT_TINY)
        draw_badge(draw, x + 215, 1500, "EF Core Migrations", CLR_INDIGO_LIGHT, CLR_INDIGO, FONT_TINY)

        # Connection info
        draw.text((x + 25, 1550), "Connection String:", font=FONT_TINY, fill=CLR_TEXT_MUTED)
        draw.text((x + 25, 1572), f"Server=localhost;Database={title}...", font=FONT_TINY, fill=CLR_TEXT_DARK)

        # Arrow from Microservice to Database
        draw_arrow(draw, (x + 210, 1100), (x + 210, 1240), CLR_TEAL, 2, "EF Core / LINQ", "right")

    save_image(img, "01_Solution_Architecture_Diagram.jpg")

print("Solution diagram generator ready.")

# ==============================================================================
# 2. USE CASE DIAGRAM
# ==============================================================================
def generate_usecase_diagram():
    W, H = 2500, 1750
    img = Image.new("RGB", (W, H), CLR_BG)
    draw = ImageDraw.Draw(img)
    
    draw_top_banner(draw, W, 
                    "PHARMACY MANAGEMENT SYSTEM - USE CASE DIAGRAM",
                    "Actor Roles: Admin & Doctor User | Microservices Functionalities & Permissions Boundary")

    # Left Actor: Doctor User
    draw_rounded_rect(draw, (40, 140, 360, 1690), 16, CLR_CARD_BG, CLR_TEAL, 2)
    # Actor Avatar Circle
    draw.ellipse([140, 170, 260, 290], fill=CLR_TEAL_LIGHT, outline=CLR_TEAL, width=3)
    # Head & shoulders icon representation
    draw.ellipse([175, 195, 225, 245], fill=CLR_TEAL)
    draw.chord([155, 230, 245, 280], 0, 180, fill=CLR_TEAL)
    draw.text((120, 310), "DOCTOR USER", font=FONT_HEADER, fill=CLR_TEAL)
    draw_badge(draw, 140, 350, "ROLE: DOCTOR", CLR_TEAL, CLR_TEXT_LIGHT)

    doctor_features = [
        "1. Login / Signup with Basic Details (Name, Contact, Email, Password)",
        "2. View Drugs & Check Details of Every Available Drug",
        "3. Buy Drugs (Place Medication Order with Items)",
        "4. View Own Placed Orders & Status Tracking",
        "5. Complete Online Order Payment (CreditCard, UPI, etc.)"
    ]
    draw.text((60, 410), "Authorized Operations:", font=FONT_SMALL_BOLD, fill=CLR_NAVY)
    for idx, f in enumerate(doctor_features):
        draw_rounded_rect(draw, (60, 440 + idx * 80, 340, 505 + idx * 80), 8, CLR_TEAL_LIGHT, CLR_BORDER_LIGHT, 1)
        # Wrap text
        words = f.split(" ")
        l1, l2 = " ".join(words[:5]), " ".join(words[5:])
        draw.text((70, 448 + idx * 80), l1, font=FONT_TINY, fill=CLR_TEXT_DARK)
        if l2:
            draw.text((70, 470 + idx * 80), l2, font=FONT_TINY, fill=CLR_TEXT_DARK)

    # Right Actor: Admin
    draw_rounded_rect(draw, (2140, 140, 2460, 1690), 16, CLR_CARD_BG, CLR_INDIGO, 2)
    # Actor Avatar Circle
    draw.ellipse([2240, 170, 2360, 290], fill=CLR_INDIGO_LIGHT, outline=CLR_INDIGO, width=3)
    draw.ellipse([2275, 195, 2325, 245], fill=CLR_INDIGO)
    draw.chord([2255, 230, 2345, 280], 0, 180, fill=CLR_INDIGO)
    draw.text((2235, 310), "ADMIN USER", font=FONT_HEADER, fill=CLR_INDIGO)
    draw_badge(draw, 2240, 350, "ROLE: ADMIN", CLR_INDIGO, CLR_TEXT_LIGHT)

    admin_features = [
        "1. Login / Signup (Name, Contact, Email, Password)",
        "2. View Drugs & Check Details of Available Drugs",
        "3. Add, Edit, and Delete Drugs",
        "4. View Suppliers & Supplier Details",
        "5. Add, Edit, and Delete Suppliers",
        "6. Add Stock to Inventory (Supplier + Drug + Price)",
        "7. View Orders Placed by All Doctors",
        "8. Check Order Validity & Validate Order Items",
        "9. Verify Orders (Pending -> Verified)",
        "10. Add Order to PickedUp Section (Verified -> PickedUp)",
        "11. View PickedUp Orders Section",
        "12. View Sales Reports (Daily, Weekly, Monthly, Yearly)",
        "13. Generate Sales Report with Revenue & Profit",
        "14. Download Sales Report as CSV Spreadsheet",
        "15. Print Sales Report (Official Formatted Receipt)"
    ]
    draw.text((2160, 410), "Authorized Operations:", font=FONT_SMALL_BOLD, fill=CLR_NAVY)
    for idx, f in enumerate(admin_features):
        draw_rounded_rect(draw, (2160, 435 + idx * 44, 2440, 472 + idx * 44), 6, CLR_INDIGO_LIGHT, CLR_BORDER_LIGHT, 1)
        draw.text((2170, 442 + idx * 44), f[:38] + ("..." if len(f) > 38 else ""), font=FONT_TINY, fill=CLR_TEXT_DARK)

    # Center: System Boundary Box
    draw_rounded_rect(draw, (400, 140, 2100, 1690), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 420, 155, "PHARMACY MANAGEMENT SYSTEM BOUNDARY (5 MICROSERVICES)", CLR_NAVY, CLR_TEXT_LIGHT)

    # Use Case Groups inside boundary
    groups = [
        {
            "title": "Auth Service Use Cases (UserDB)",
            "color": CLR_AMBER,
            "light": CLR_AMBER_LIGHT,
            "y": 200,
            "cases": [
                ("UC-01: User Signup", "Doctor & Admin register with name, phone, email, password", "both"),
                ("UC-02: User Login", "Authenticate credentials & issue JWT Bearer token", "both"),
                ("UC-03: Validate Doctor", "Verify doctor identity during order placement", "system"),
                ("UC-04: View All Users", "Admin manages system accounts and active statuses", "admin")
            ]
        },
        {
            "title": "Inventory Service Use Cases (InventoryDB)",
            "color": CLR_TEAL,
            "light": CLR_TEAL_LIGHT,
            "y": 480,
            "cases": [
                ("UC-05: View Drugs", "View list & check details of each available medication", "both"),
                ("UC-06: Manage Drugs", "Admin Adds, Edits, and Deletes drugs from catalog", "admin"),
                ("UC-07: Manage Suppliers", "Admin Adds, Edits, and Deletes drug suppliers", "admin"),
                ("UC-08: Add Stock to Inventory", "Admin links Supplier & Drug with purchase price & quantity", "admin"),
                ("UC-09: Deduct Stock", "Internal atomic deduction of drug stock when order is placed", "system")
            ]
        },
        {
            "title": "Order Service Use Cases (OrderDB)",
            "color": CLR_BLUE_PRIMARY,
            "light": CLR_BLUE_LIGHT,
            "y": 800,
            "cases": [
                ("UC-10: Buy Drugs (Place Order)", "Doctor creates order with items, quantities, and pricing", "doctor"),
                ("UC-11: View Own Orders", "Doctor views history and current status of placed orders", "doctor"),
                ("UC-12: View All Doctor Orders", "Admin inspects orders placed by all doctors across system", "admin"),
                ("UC-13: Validate Order", "Admin checks if order items, doctor, and totals are valid", "admin"),
                ("UC-14: Verify Order", "Admin verifies valid order (Status: Pending -> Verified)", "admin"),
                ("UC-15: Move to PickedUp Section", "Admin marks fulfilled order as PickedUp", "admin")
            ]
        },
        {
            "title": "Payment Service Use Cases (PaymentDB)",
            "color": CLR_EMERALD,
            "light": CLR_EMERALD_LIGHT,
            "y": 1150,
            "cases": [
                ("UC-16: Process Payment", "Doctor completes 1:1 order payment (CreditCard, UPI, etc.)", "doctor"),
                ("UC-17: View Payment Details", "Lookup transaction by OrderId or PaymentId", "both"),
                ("UC-18: Manage Payments", "Admin views all system transactions and updates statuses", "admin")
            ]
        },
        {
            "title": "SaleReport Service Use Cases (SaleReportDB)",
            "color": CLR_INDIGO,
            "light": CLR_INDIGO_LIGHT,
            "y": 1420,
            "cases": [
                ("UC-19: Generate Sales Report", "Admin generates Daily, Weekly, Monthly, Yearly reports", "admin"),
                ("UC-20: View Sales Reports", "Admin analyzes total orders, total revenue, and net profit", "admin"),
                ("UC-21: Download Sales Report (CSV)", "Admin exports financial report as CSV spreadsheet", "admin"),
                ("UC-22: Print Sales Report", "Admin retrieves formatted official printable summary view", "admin")
            ]
        }
    ]

    for grp in groups:
        gy = grp["y"]
        draw_rounded_rect(draw, (420, gy, 2080, gy + 240), 10, grp["light"], grp["color"], 1)
        draw.text((440, gy + 12), grp["title"], font=FONT_SUBHEADER, fill=grp["color"])

        for c_idx, (uc_title, uc_desc, actor_type) in enumerate(grp["cases"]):
            cx = 440 + (c_idx % 2) * 810
            cy = gy + 45 + (c_idx // 2) * 85
            draw_rounded_rect(draw, (cx, cy, cx + 790, cy + 72), 24, CLR_CARD_BG, CLR_BORDER, 1)

            # Oval use case badge
            badge_color = CLR_TEAL if actor_type == "doctor" else (CLR_INDIGO if actor_type == "admin" else (CLR_NAVY if actor_type == "both" else CLR_AMBER))
            badge_label = "DOCTOR" if actor_type == "doctor" else ("ADMIN" if actor_type == "admin" else ("DOCTOR & ADMIN" if actor_type == "both" else "SYSTEM CALL"))
            draw_badge(draw, cx + 15, cy + 12, badge_label, badge_color, CLR_TEXT_LIGHT, FONT_TINY)

            draw.text((cx + 140, cy + 12), uc_title, font=FONT_SMALL_BOLD, fill=CLR_NAVY)
            draw.text((cx + 25, cy + 42), uc_desc, font=FONT_TINY, fill=CLR_TEXT_MUTED)

            # Draw association lines to actors
            if actor_type in ("doctor", "both"):
                draw.line([(360, 250), (cx, cy + 36)], fill=(14, 116, 144, 120), width=1)
            if actor_type in ("admin", "both"):
                draw.line([(2140, 250), (cx + 790, cy + 36)], fill=(79, 70, 229, 120), width=1)

    save_image(img, "02_Use_Case_Diagram.jpg")

print("Use case diagram generator ready.")

# ==============================================================================
# 3. SEQUENCE DIAGRAMS (3 CORE BUSINESS FLOWS)
# ==============================================================================
def generate_sequence_diagram():
    W, H = 2500, 2050
    img = Image.new("RGB", (W, H), CLR_BG)
    draw = ImageDraw.Draw(img)
    
    draw_top_banner(draw, W, 
                    "PHARMACY MANAGEMENT SYSTEM - SEQUENCE DIAGRAMS",
                    "Inter-Service & Client Workflows: Doctor Order & Pay | Admin Validation & Pickup | Sales Reporting")

    # ==========================
    # FLOW 1: DOCTOR WORKFLOW
    # ==========================
    draw_rounded_rect(draw, (40, 140, 2460, 750), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 155, "FLOW 1: DOCTOR USER - SIGNUP, LOGIN, BROWSE DRUGS, BUY DRUGS (ORDER) & COMPLETE PAYMENT", CLR_TEAL, CLR_TEXT_LIGHT)

    # Lifelines for Flow 1
    lifelines_1 = [
        ("Doctor User", 200, CLR_TEAL),
        ("AuthService (:5001)", 650, CLR_AMBER),
        ("InventoryService (:5002)", 1150, CLR_TEAL),
        ("OrderService (:5003)", 1650, CLR_BLUE_PRIMARY),
        ("PaymentService (:5004)", 2150, CLR_EMERALD)
    ]
    for name, x, color in lifelines_1:
        # Box header
        draw_rounded_rect(draw, (x - 120, 200, x + 120, 245), 8, color)
        draw.text((x - 80, 212), name, font=FONT_SMALL_BOLD, fill=CLR_TEXT_LIGHT)
        # Vertical lifeline
        draw.line([(x, 245), (x, 720)], fill=CLR_BORDER, width=2)

    # Messages Flow 1
    steps_1 = [
        # (y, from_x, to_x, text, is_return, color)
        (280, 200, 650, "1. POST /api/auth/login {email, password}", False, CLR_NAVY),
        (320, 650, 200, "2. 200 OK: Returns JWT Bearer Token (Role: Doctor)", True, CLR_AMBER),
        (370, 200, 1150, "3. GET /api/drugs?availableOnly=true (Header: Bearer Token)", False, CLR_NAVY),
        (410, 1150, 200, "4. 200 OK: List of available drugs with stock and selling price", True, CLR_TEAL),
        (470, 200, 1650, "5. POST /api/orders (Buy Drugs: DrugId, Qty, UnitPrice, Status: Pending)", False, CLR_BLUE_PRIMARY),
        (520, 1650, 1150, "6. Internal HTTP POST /api/drugs/deduct-stock (Atomic Stock Deduction)", False, CLR_ROSE),
        (560, 1150, 1650, "7. 200 OK: Stock deducted, IsAvailable updated if quantity reached 0", True, CLR_TEAL),
        (600, 1650, 200, "8. 201 Created: Order placed successfully (OrderId: #101, Status: Pending)", True, CLR_BLUE_PRIMARY),
        (650, 200, 2150, "9. POST /api/payments {OrderId: 101, Amount: $48.50, Method: CreditCard}", False, CLR_EMERALD),
        (690, 2150, 200, "10. 200 OK: Payment Completed, TxnRef: TXN-A83F91B2C4D5 (1:1 with Order)", True, CLR_EMERALD)
    ]
    for y, fx, tx, txt, is_ret, clr in steps_1:
        if is_ret:
            # dashed line
            for seg in range(min(fx, tx), max(fx, tx), 15):
                draw.line([(seg, y), (min(seg + 8, max(fx, tx)), y)], fill=clr, width=2)
            draw_arrow(draw, (fx + (10 if tx > fx else -10), y), (tx, y), clr, 2)
        else:
            draw_arrow(draw, (fx, y), (tx, y), clr, 2)
        
        # Label above arrow
        mid_x = (fx + tx) / 2
        draw_rounded_rect(draw, (mid_x - 180, y - 22, mid_x + 180, y - 2), 4, (255, 255, 255, 220), CLR_BORDER_LIGHT, 1)
        draw.text((mid_x - 170, y - 18), txt, font=FONT_TINY, fill=clr)

    # ==========================
    # FLOW 2: ADMIN ORDER WORKFLOW
    # ==========================
    draw_rounded_rect(draw, (40, 780, 2460, 1370), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 795, "FLOW 2: ADMIN - VIEW ALL DOCTOR ORDERS, VALIDATE, VERIFY & HANDOVER TO PICKED-UP SECTION", CLR_INDIGO, CLR_TEXT_LIGHT)

    lifelines_2 = [
        ("Admin User", 250, CLR_INDIGO),
        ("AuthService (:5001)", 800, CLR_AMBER),
        ("OrderService (:5003)", 1500, CLR_BLUE_PRIMARY),
        ("OrderDB (SQL Server)", 2150, CLR_TEAL)
    ]
    for name, x, color in lifelines_2:
        draw_rounded_rect(draw, (x - 120, 840, x + 120, 885), 8, color)
        draw.text((x - 80, 852), name, font=FONT_SMALL_BOLD, fill=CLR_TEXT_LIGHT)
        draw.line([(x, 885), (x, 1340)], fill=CLR_BORDER, width=2)

    steps_2 = [
        (920, 250, 800, "1. POST /api/auth/login {admin credentials}", False, CLR_NAVY),
        (960, 800, 250, "2. 200 OK: Returns Admin JWT Bearer Token (Role: Admin)", True, CLR_AMBER),
        (1010, 250, 1500, "3. GET /api/orders (View orders placed by all doctors)", False, CLR_BLUE_PRIMARY),
        (1050, 1500, 2150, "4. LINQ Query: _context.Orders.Include(o => o.OrderItems).ToListAsync()", False, CLR_TEAL),
        (1090, 2150, 1500, "5. Returns orders data across all clinics/doctors", True, CLR_TEAL),
        (1130, 1500, 250, "6. 200 OK: Orders list with DoctorId, OrderItems, Totals, and Status", True, CLR_BLUE_PRIMARY),
        (1180, 250, 1500, "7. GET /api/orders/{id}/validate (Check if order is valid)", False, CLR_NAVY),
        (1220, 1500, 250, "8. 200 OK: { isValid: true, details: 'Order has valid items and doctor' }", True, CLR_EMERALD),
        (1260, 250, 1500, "9. PUT /api/orders/{id}/verify (Verify validated order: Status -> 'Verified')", False, CLR_BLUE_PRIMARY),
        (1300, 250, 1500, "10. PUT /api/orders/{id}/pickup (Doctor picks up: Add order to PickedUp section)", False, CLR_INDIGO)
    ]
    for y, fx, tx, txt, is_ret, clr in steps_2:
        if is_ret:
            for seg in range(min(fx, tx), max(fx, tx), 15):
                draw.line([(seg, y), (min(seg + 8, max(fx, tx)), y)], fill=clr, width=2)
            draw_arrow(draw, (fx + (10 if tx > fx else -10), y), (tx, y), clr, 2)
        else:
            draw_arrow(draw, (fx, y), (tx, y), clr, 2)
        
        mid_x = (fx + tx) / 2
        draw_rounded_rect(draw, (mid_x - 180, y - 22, mid_x + 180, y - 2), 4, (255, 255, 255, 220), CLR_BORDER_LIGHT, 1)
        draw.text((mid_x - 170, y - 18), txt, font=FONT_TINY, fill=clr)

    # ==========================
    # FLOW 3: SALES REPORTING WORKFLOW
    # ==========================
    draw_rounded_rect(draw, (40, 1400, 2460, 2000), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 1415, "FLOW 3: ADMIN - GENERATE SALES REPORT, AGGREGATE REVENUE & PROFIT, DOWNLOAD CSV & PRINT", CLR_EMERALD, CLR_TEXT_LIGHT)

    lifelines_3 = [
        ("Admin User", 250, CLR_INDIGO),
        ("SaleReportService (:5005)", 900, CLR_INDIGO),
        ("OrderService (:5003)", 1600, CLR_BLUE_PRIMARY),
        ("SaleReportDB", 2200, CLR_TEAL)
    ]
    for name, x, color in lifelines_3:
        draw_rounded_rect(draw, (x - 120, 1460, x + 120, 1505), 8, color)
        draw.text((x - 90, 1472), name, font=FONT_SMALL_BOLD, fill=CLR_TEXT_LIGHT)
        draw.line([(x, 1505), (x, 1970)], fill=CLR_BORDER, width=2)

    steps_3 = [
        (1540, 250, 900, "1. POST /api/salereports/generate {ReportType: Monthly, FromDate, ToDate}", False, CLR_NAVY),
        (1590, 900, 1600, "2. Internal HTTP GET /api/orders (Fetch verified & picked-up orders for period)", False, CLR_BLUE_PRIMARY),
        (1640, 1600, 900, "3. 200 OK: Orders dataset (Order totals, items, dates)", True, CLR_BLUE_PRIMARY),
        (1690, 900, 2200, "4. Compute TotalRevenue, Profit (Revenue - COGS) & INSERT SaleReport record", False, CLR_TEAL),
        (1740, 900, 250, "5. 201 Created: Report summary {TotalOrders: 340, Revenue: $45,200, Profit: $14,464}", True, CLR_EMERALD),
        (1800, 250, 900, "6. GET /api/salereports/{id}/download (Download CSV spreadsheet)", False, CLR_NAVY),
        (1840, 900, 250, "7. 200 OK: File stream 'SaleReport_Monthly_2026.csv' (Content-Type: text/csv)", True, CLR_EMERALD),
        (1890, 250, 900, "8. GET /api/salereports/{id}/print (Retrieve formatted printable layout)", False, CLR_NAVY),
        (1930, 900, 250, "9. 200 OK: Official printable receipt view with ASCII borders and financial summary", True, CLR_INDIGO)
    ]
    for y, fx, tx, txt, is_ret, clr in steps_3:
        if is_ret:
            for seg in range(min(fx, tx), max(fx, tx), 15):
                draw.line([(seg, y), (min(seg + 8, max(fx, tx)), y)], fill=clr, width=2)
            draw_arrow(draw, (fx + (10 if tx > fx else -10), y), (tx, y), clr, 2)
        else:
            draw_arrow(draw, (fx, y), (tx, y), clr, 2)
        
        mid_x = (fx + tx) / 2
        draw_rounded_rect(draw, (mid_x - 180, y - 22, mid_x + 180, y - 2), 4, (255, 255, 255, 220), CLR_BORDER_LIGHT, 1)
        draw.text((mid_x - 170, y - 18), txt, font=FONT_TINY, fill=clr)

    save_image(img, "03_Sequence_Diagram.jpg")

print("Sequence diagram generator ready.")

# ==============================================================================
# 4. FLOW DIAGRAM (ORDER LIFECYCLE & INVENTORY MANAGEMENT)
# ==============================================================================
def generate_flow_diagram():
    W, H = 2500, 1750
    img = Image.new("RGB", (W, H), CLR_BG)
    draw = ImageDraw.Draw(img)
    
    draw_top_banner(draw, W, 
                    "PHARMACY MANAGEMENT SYSTEM - FLOW DIAGRAMS",
                    "End-to-End Business Logic: Order Lifecycle State Machine & Inventory Stock Allocation Flow")

    # Left Container: Order Lifecycle Flow
    draw_rounded_rect(draw, (40, 140, 1220, 1690), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 60, 155, "FLOW 1: ORDER LIFECYCLE STATE MACHINE (CART -> PENDING -> VERIFIED -> PICKED-UP)", CLR_BLUE_PRIMARY, CLR_TEXT_LIGHT)

    order_nodes = [
        # (type, x, y, w, h, text, sub, bg, border)
        ("oval", 500, 220, 260, 50, "Doctor Initiates Order", "Browse available drugs in InventoryService", CLR_TEAL_LIGHT, CLR_TEAL),
        ("rect", 450, 310, 360, 65, "Status: Cart", "Doctor adds drug items & quantities to temporary cart", (241, 245, 249), CLR_BORDER),
        ("rect", 450, 415, 360, 65, "Doctor Submits Order", "POST /api/orders (DoctorId, Items, Pricing)", CLR_BLUE_LIGHT, CLR_BLUE_PRIMARY),
        ("diamond", 470, 520, 320, 90, "Stock Available?", "Verify all items: Qty >= req & Expiry > now", CLR_AMBER_LIGHT, CLR_AMBER),
        ("rect", 100, 532, 280, 65, "Reject Order", "Return HTTP 400: Out of Stock Alert", CLR_ROSE_LIGHT, CLR_ROSE),
        ("rect", 450, 650, 360, 65, "Atomic Stock Deduction", "InventoryService: Deduct quantities from Drugs table", CLR_TEAL_LIGHT, CLR_TEAL),
        ("rect", 450, 755, 360, 65, "Status: Pending", "Order created in OrderDB with status 'Pending'", CLR_AMBER_LIGHT, CLR_AMBER),
        ("diamond", 470, 860, 320, 90, "Payment Processed?", "POST /api/payments {OrderId, Amount, Method}", CLR_INDIGO_LIGHT, CLR_INDIGO),
        ("rect", 100, 872, 280, 65, "Payment Pending / Retry", "Doctor can retry via credit card, UPI, etc.", (248, 250, 252), CLR_BORDER),
        ("rect", 450, 990, 360, 65, "Payment Completed", "1:1 Payment created with status 'Completed'", CLR_EMERALD_LIGHT, CLR_EMERALD),
        ("rect", 450, 1095, 360, 65, "Admin Order Review", "Admin calls GET /api/orders/{id}/validate", CLR_BLUE_LIGHT, CLR_BLUE_PRIMARY),
        ("diamond", 470, 1200, 320, 90, "Is Order Valid?", "Doctor verified, items valid, total > 0", CLR_AMBER_LIGHT, CLR_AMBER),
        ("rect", 100, 1212, 280, 65, "Flag / Cancel Order", "Admin rejects order or flags discrepancy", CLR_ROSE_LIGHT, CLR_ROSE),
        ("rect", 450, 1330, 360, 65, "Status: Verified", "Admin calls PUT /api/orders/{id}/verify", CLR_EMERALD_LIGHT, CLR_EMERALD),
        ("rect", 450, 1435, 360, 65, "Doctor Pickup Handover", "Medication packaged & handed over at counter", CLR_TEAL_LIGHT, CLR_TEAL),
        ("rect", 450, 1540, 360, 65, "Status: PickedUp", "Admin calls PUT /api/orders/{id}/pickup", CLR_INDIGO_LIGHT, CLR_INDIGO),
        ("oval", 500, 1630, 260, 45, "Order Completed", "Ready for Sales Report Aggregation", CLR_EMERALD_LIGHT, CLR_EMERALD)
    ]

    for ntype, x, y, w, h, t1, t2, bg, border in order_nodes:
        if ntype == "oval":
            draw.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg, outline=border, width=2)
            draw.text((x + 20, y + 8), t1, font=FONT_SMALL_BOLD, fill=border)
            draw.text((x + 20, y + 26), t2, font=FONT_TINY, fill=CLR_TEXT_MUTED)
        elif ntype == "diamond":
            # Diamond shape
            pts = [(x + w//2, y), (x + w, y + h//2), (x + w//2, y + h), (x, y + h//2)]
            draw.polygon(pts, fill=bg, outline=border)
            draw.text((x + w//2 - 60, y + 25), t1, font=FONT_SMALL_BOLD, fill=border)
            draw.text((x + w//2 - 110, y + 48), t2, font=FONT_TINY, fill=CLR_TEXT_DARK)
        else:
            draw_rounded_rect(draw, (x, y, x + w, y + h), 8, bg, border, 2)
            draw.text((x + 15, y + 12), t1, font=FONT_SMALL_BOLD, fill=border)
            draw.text((x + 15, y + 36), t2, font=FONT_TINY, fill=CLR_TEXT_DARK)

    # Order flow connectors
    draw_arrow(draw, (630, 270), (630, 310), CLR_NAVY, 2)
    draw_arrow(draw, (630, 375), (630, 415), CLR_NAVY, 2)
    draw_arrow(draw, (630, 480), (630, 520), CLR_NAVY, 2)
    # Diamond 1: No
    draw_arrow(draw, (470, 565), (380, 565), CLR_ROSE, 2, "No (Out of Stock)", "top")
    # Diamond 1: Yes
    draw_arrow(draw, (630, 610), (630, 650), CLR_EMERALD, 2, "Yes", "right")
    draw_arrow(draw, (630, 715), (630, 755), CLR_NAVY, 2)
    draw_arrow(draw, (630, 820), (630, 860), CLR_NAVY, 2)
    # Diamond 2: No
    draw_arrow(draw, (470, 905), (380, 905), CLR_AMBER, 2, "No / Pending", "top")
    # Diamond 2: Yes
    draw_arrow(draw, (630, 950), (630, 990), CLR_EMERALD, 2, "Yes (Completed)", "right")
    draw_arrow(draw, (630, 1055), (630, 1095), CLR_NAVY, 2)
    draw_arrow(draw, (630, 1160), (630, 1200), CLR_NAVY, 2)
    # Diamond 3: No
    draw_arrow(draw, (470, 1245), (380, 1245), CLR_ROSE, 2, "Invalid", "top")
    # Diamond 3: Yes
    draw_arrow(draw, (630, 1290), (630, 1330), CLR_EMERALD, 2, "Valid", "right")
    draw_arrow(draw, (630, 1395), (630, 1435), CLR_NAVY, 2)
    draw_arrow(draw, (630, 1500), (630, 1540), CLR_NAVY, 2)
    draw_arrow(draw, (630, 1605), (630, 1630), CLR_NAVY, 2)


    # Right Container: Inventory Stock Allocation & Restock Flow
    draw_rounded_rect(draw, (1280, 140, 2460, 1690), 16, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 1300, 155, "FLOW 2: INVENTORY STOCK MANAGEMENT (RESTOCK & ATOMIC DEDUCTION PIPELINE)", CLR_TEAL, CLR_TEXT_LIGHT)

    inv_nodes = [
        # (type, x, y, w, h, text, sub, bg, border)
        ("oval", 1750, 220, 280, 50, "Inventory Event Trigger", "Order Placement OR Admin Restock", CLR_TEAL_LIGHT, CLR_TEAL),
        ("diamond", 1720, 310, 340, 90, "Event Type?", "Stock Inward vs Order Stock Deduction", CLR_AMBER_LIGHT, CLR_AMBER),
        
        # Branch A: Restock (Left side of right container)
        ("rect", 1320, 440, 360, 65, "Admin Inward Stock", "POST /api/inventory (SupplierId, DrugId, Price, Qty)", CLR_INDIGO_LIGHT, CLR_INDIGO),
        ("rect", 1320, 545, 360, 65, "Insert Inventory Record", "Logs wholesale supplier, purchase price, and batch date", (240, 249, 255), CLR_BORDER),
        ("rect", 1320, 650, 360, 65, "Increment Drug Quantity", "drug.Quantity += QuantityAdded", CLR_EMERALD_LIGHT, CLR_EMERALD),
        ("rect", 1320, 755, 360, 65, "Set IsAvailable = true", "If quantity > 0 and expiry valid, activate drug listing", CLR_TEAL_LIGHT, CLR_TEAL),
        ("oval", 1360, 860, 280, 45, "Stock Inward Complete", "Drugs available for doctor purchasing", CLR_EMERALD_LIGHT, CLR_EMERALD),

        # Branch B: Deduction (Right side of right container)
        ("rect", 1980, 440, 380, 65, "Order Service Deduction", "POST /api/drugs/deduct-stock with items payload", CLR_BLUE_LIGHT, CLR_BLUE_PRIMARY),
        ("rect", 1980, 545, 380, 65, "Verify Expiry & Availability", "Ensure Drug.IsAvailable == true AND ExpiryDate > Now", (248, 250, 252), CLR_BORDER),
        ("diamond", 2000, 650, 340, 90, "Sufficient Stock?", "Check: Drug.Quantity >= Requested Quantity", CLR_AMBER_LIGHT, CLR_AMBER),
        ("rect", 1980, 780, 380, 65, "Deduct Drug Quantity", "Atomic update: drug.Quantity -= requestedQty", CLR_TEAL_LIGHT, CLR_TEAL),
        ("diamond", 2000, 885, 340, 90, "Remaining Qty == 0?", "Check if inventory depleted for this drug", CLR_AMBER_LIGHT, CLR_AMBER),
        ("rect", 1980, 1015, 380, 65, "Auto Deactivate Drug", "Set drug.IsAvailable = false (Out of Stock)", CLR_ROSE_LIGHT, CLR_ROSE),
        ("rect", 1980, 1120, 380, 65, "Save & Commit DbContext", "SaveChanges: Transaction committed to SQL Server", CLR_EMERALD_LIGHT, CLR_EMERALD),
        ("oval", 2030, 1225, 280, 45, "Stock Deducted OK", "Order Service confirms order placement", CLR_EMERALD_LIGHT, CLR_EMERALD)
    ]

    for ntype, x, y, w, h, t1, t2, bg, border in inv_nodes:
        if ntype == "oval":
            draw.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg, outline=border, width=2)
            draw.text((x + 20, y + 8), t1, font=FONT_SMALL_BOLD, fill=border)
            draw.text((x + 20, y + 26), t2, font=FONT_TINY, fill=CLR_TEXT_MUTED)
        elif ntype == "diamond":
            pts = [(x + w//2, y), (x + w, y + h//2), (x + w//2, y + h), (x, y + h//2)]
            draw.polygon(pts, fill=bg, outline=border)
            draw.text((x + w//2 - 50, y + 25), t1, font=FONT_SMALL_BOLD, fill=border)
            draw.text((x + w//2 - 120, y + 48), t2, font=FONT_TINY, fill=CLR_TEXT_DARK)
        else:
            draw_rounded_rect(draw, (x, y, x + w, y + h), 8, bg, border, 2)
            draw.text((x + 15, y + 12), t1, font=FONT_SMALL_BOLD, fill=border)
            draw.text((x + 15, y + 36), t2, font=FONT_TINY, fill=CLR_TEXT_DARK)

    # Right container connectors
    draw_arrow(draw, (1890, 270), (1890, 310), CLR_NAVY, 2)
    # Event Diamond branches
    draw_arrow(draw, (1720, 355), (1500, 440), CLR_INDIGO, 2, "Admin Restock", "left")
    draw_arrow(draw, (2060, 355), (2170, 440), CLR_BLUE_PRIMARY, 2, "Order Deduction", "right")

    # Restock path
    draw_arrow(draw, (1500, 505), (1500, 545), CLR_NAVY, 2)
    draw_arrow(draw, (1500, 610), (1500, 650), CLR_NAVY, 2)
    draw_arrow(draw, (1500, 715), (1500, 755), CLR_NAVY, 2)
    draw_arrow(draw, (1500, 820), (1500, 860), CLR_NAVY, 2)

    # Deduction path
    draw_arrow(draw, (2170, 505), (2170, 545), CLR_NAVY, 2)
    draw_arrow(draw, (2170, 610), (2170, 650), CLR_NAVY, 2)
    draw_arrow(draw, (2170, 740), (2170, 780), CLR_EMERALD, 2, "Yes", "right")
    draw_arrow(draw, (2170, 845), (2170, 885), CLR_NAVY, 2)
    draw_arrow(draw, (2170, 975), (2170, 1015), CLR_ROSE, 2, "Yes (Qty=0)", "right")
    draw_arrow(draw, (2170, 1080), (2170, 1120), CLR_NAVY, 2)
    draw_arrow(draw, (2170, 1185), (2170, 1225), CLR_NAVY, 2)

    save_image(img, "04_Flow_Diagram.jpg")

print("Flow diagram generator ready.")

# ==============================================================================
# 5. ENTITY-RELATIONSHIP (ER) DIAGRAM
# ==============================================================================
def generate_er_diagram():
    W, H = 2500, 1800
    img = Image.new("RGB", (W, H), CLR_BG)
    draw = ImageDraw.Draw(img)
    
    draw_top_banner(draw, W, 
                    "PHARMACY MANAGEMENT SYSTEM - ENTITY RELATIONSHIP (ER) DIAGRAM",
                    "Bounded Context Entities, Cross-Service Foreign Keys & Explicit Cardinalities (1:M, 1:1, Standalone)")

    # Entity definition helper
    def draw_entity_box(x, y, w, title, attrs, header_bg, border_color):
        h = 50 + len(attrs) * 32
        draw_rounded_rect(draw, (x, y, x + w, y + h), 10, CLR_CARD_BG, border_color, 2)
        # Header
        draw_rounded_rect(draw, (x, y, x + w, y + 45), 10, header_bg)
        draw.rectangle([x, y + 35, x + w, y + 45], fill=header_bg)
        draw.text((x + 15, y + 12), title, font=FONT_HEADER, fill=CLR_TEXT_LIGHT)

        for i, (is_pk, is_fk, name, dtype) in enumerate(attrs):
            row_y = y + 50 + i * 32
            # Zebra striping
            if i % 2 == 1:
                draw.rectangle([x + 1, row_y, x + w - 1, row_y + 30], fill=(248, 250, 252))
            
            # Key indicator
            if is_pk:
                draw_badge(draw, x + 10, row_y + 3, "PK", CLR_AMBER, CLR_TEXT_LIGHT, FONT_TINY)
            elif is_fk:
                draw_badge(draw, x + 10, row_y + 3, "FK", CLR_BLUE_PRIMARY, CLR_TEXT_LIGHT, FONT_TINY)
            else:
                draw.text((x + 15, row_y + 5), "•", font=FONT_BODY, fill=CLR_TEXT_MUTED)

            draw.text((x + 55, row_y + 5), name, font=FONT_BODY_BOLD, fill=CLR_TEXT_DARK)
            draw.text((x + w - 130, row_y + 5), dtype, font=FONT_SMALL, fill=CLR_TEXT_MUTED)

        return x, y, w, h

    # 1. USER entity (Auth Service)
    user_attrs = [
        (True, False, "UserId", "int [PK]"),
        (False, False, "Name", "nvarchar(100)"),
        (False, False, "Email", "nvarchar(150) [UQ]"),
        (False, False, "PhoneNumber", "nvarchar(20)"),
        (False, False, "PasswordHash", "nvarchar(255)"),
        (False, False, "Role", "nvarchar(20)"),
        (False, False, "IsActive", "bit [Default 1]"),
        (False, False, "CreatedDate", "datetime2")
    ]
    u_x, u_y, u_w, u_h = draw_entity_box(60, 200, 420, "USER (UserDB)", user_attrs, CLR_AMBER, CLR_AMBER)

    # 2. DRUGS entity (Inventory Service)
    drug_attrs = [
        (True, False, "DrugId", "int [PK]"),
        (False, False, "Name", "nvarchar(150)"),
        (False, False, "Description", "nvarchar(500)"),
        (False, False, "Price", "decimal(18,2)"),
        (False, False, "ExpiryDate", "datetime2"),
        (False, False, "Quantity", "int"),
        (False, False, "IsAvailable", "bit [Default 1]")
    ]
    d_x, d_y, d_w, d_h = draw_entity_box(720, 200, 420, "DRUG (InventoryDB)", drug_attrs, CLR_TEAL, CLR_TEAL)

    # 3. SUPPLIERS entity (Inventory Service)
    supplier_attrs = [
        (True, False, "SupplierId", "int [PK]"),
        (False, False, "SupplierName", "nvarchar(150)"),
        (False, False, "Email", "nvarchar(150)"),
        (False, False, "PhoneNumber", "nvarchar(20)"),
        (False, False, "Address", "nvarchar(300)")
    ]
    s_x, s_y, s_w, s_h = draw_entity_box(1380, 200, 420, "SUPPLIER (InventoryDB)", supplier_attrs, CLR_TEAL, CLR_TEAL)

    # 4. INVENTORY entity (Inventory Service)
    inv_attrs = [
        (True, False, "InventoryId", "int [PK]"),
        (False, True, "SupplierId", "int [FK Supplier]"),
        (False, True, "DrugId", "int [FK Drug]"),
        (False, False, "PurchasePrice", "decimal(18,2)"),
        (False, False, "QuantityAdded", "int"),
        (False, False, "StockReceivedDate", "datetime2")
    ]
    i_x, i_y, i_w, i_h = draw_entity_box(1050, 600, 440, "INVENTORY (InventoryDB)", inv_attrs, CLR_TEAL, CLR_TEAL)

    # 5. ORDER entity (Order Service)
    order_attrs = [
        (True, False, "OrderId", "int [PK]"),
        (False, True, "DoctorID", "int [Logical FK User]"),
        (False, False, "OrderDate", "datetime2"),
        (False, False, "TotalAmount", "decimal(18,2)"),
        (False, False, "Status", "nvarchar(20)")
    ]
    o_x, o_y, o_w, o_h = draw_entity_box(260, 800, 450, "ORDER (OrderDB)", order_attrs, CLR_BLUE_PRIMARY, CLR_BLUE_PRIMARY)

    # 6. ORDER ITEM entity (Order Service)
    item_attrs = [
        (True, False, "OrderItemId", "int [PK]"),
        (False, True, "OrderId", "int [FK Order]"),
        (False, True, "DrugId", "int [Logical FK Drug]"),
        (False, False, "DrugName", "nvarchar(150)"),
        (False, False, "Quantity", "int"),
        (False, False, "UnitPrice", "decimal(18,2)")
    ]
    oi_x, oi_y, oi_w, oi_h = draw_entity_box(260, 1150, 450, "ORDER_ITEM (OrderDB)", item_attrs, CLR_BLUE_PRIMARY, CLR_BLUE_PRIMARY)

    # 7. PAYMENT entity (Payment Service)
    payment_attrs = [
        (True, False, "PaymentId", "int [PK]"),
        (False, True, "OrderId", "int [UQ / 1:1 FK]"),
        (False, False, "Amount", "decimal(18,2)"),
        (False, False, "PaymentDate", "datetime2"),
        (False, False, "PaymentMethod", "nvarchar(50)"),
        (False, False, "PaymentStatus", "nvarchar(20)"),
        (False, False, "TransactionReference", "nvarchar(100)")
    ]
    p_x, p_y, p_w, p_h = draw_entity_box(920, 1000, 440, "PAYMENT (PaymentDB)", payment_attrs, CLR_EMERALD, CLR_EMERALD)

    # 8. SALE REPORT entity (SaleReport Service - Standalone)
    report_attrs = [
        (True, False, "SaleReportId", "int [PK]"),
        (False, False, "ReportType", "nvarchar(20) [Daily/Wk/Mo/Yr]"),
        (False, False, "FromDate", "datetime2"),
        (False, False, "ToDate", "datetime2"),
        (False, False, "TotalOrders", "int"),
        (False, False, "TotalRevenue", "decimal(18,2)"),
        (False, False, "GeneratedDate", "datetime2"),
        (False, False, "Profit", "decimal(18,2)")
    ]
    r_x, r_y, r_w, r_h = draw_entity_box(1600, 950, 480, "SALE_REPORT (SaleReportDB)", report_attrs, CLR_INDIGO, CLR_INDIGO)

    # RELATIONSHIP CONNECTORS & LABELS
    # 1. User to Order (1:M)
    draw_arrow(draw, (200, u_y + u_h), (350, o_y), CLR_AMBER, 3, "1 : M (User to Order)", "left")

    # 2. Order to OrderItem (1:M)
    draw_arrow(draw, (485, o_y + o_h), (485, oi_y), CLR_BLUE_PRIMARY, 3, "1 : M (Order to OrderItem)", "right")

    # 3. Drug to OrderItem (1:M)
    draw.line([(800, d_y + d_h), (800, 1250), (710, 1250)], fill=CLR_TEAL, width=2)
    draw_arrow(draw, (715, 1250), (710, 1250), CLR_TEAL, 2, "1 : M (Drug to OrderItem)", "bottom")

    # 4. Supplier to Inventory (1:M)
    draw_arrow(draw, (1500, s_y + s_h), (1350, i_y), CLR_TEAL, 3, "1 : M (Supplier to Inventory)", "right")

    # 5. Drug to Inventory (1:M)
    draw_arrow(draw, (980, d_y + d_h), (1150, i_y), CLR_TEAL, 3, "1 : M (Drug to Inventory)", "left")

    # 6. Order to Payment (1:1)
    draw_arrow(draw, (o_x + o_w, 950), (p_x, 1050), CLR_EMERALD, 3, "1 : 1 (Order to Payment)", "top")

    # 7. Standalone SaleReport annotation
    draw_rounded_rect(draw, (1600, 1350, 2300, 1500), 8, CLR_INDIGO_LIGHT, CLR_INDIGO, 1)
    draw.text((1620, 1365), "Standalone Aggregated Financial Entity:", font=FONT_SMALL_BOLD, fill=CLR_INDIGO)
    draw.text((1620, 1395), "• Aggregates total verified & picked-up orders from Order Service", font=FONT_SMALL, fill=CLR_TEXT_DARK)
    draw.text((1620, 1425), "• Calculates gross revenue and subtracts COGS purchase cost", font=FONT_SMALL, fill=CLR_TEXT_DARK)
    draw.text((1620, 1455), "• Maintains independent standalone audit history across financial periods", font=FONT_SMALL, fill=CLR_TEXT_DARK)

    save_image(img, "05_ER_Diagram.jpg")

print("ER diagram generator ready.")

# ==============================================================================
# 6. DATABASE SCHEMA DIAGRAM (5 PHYSICAL SQL SERVER DATABASES)
# ==============================================================================
def generate_database_diagram():
    W, H = 2600, 1900
    img = Image.new("RGB", (W, H), CLR_BG)
    draw = ImageDraw.Draw(img)
    
    draw_top_banner(draw, W, 
                    "PHARMACY MANAGEMENT SYSTEM - DATABASE SCHEMA DIAGRAM",
                    "Physical SQL Server Schemas: Tables, Primary Keys, Foreign Keys, Unique Indexes, Defaults & Column Types")

    def draw_db_box(x, y, w, title, color, light_color):
        draw_rounded_rect(draw, (x, y, x + w, y + 50), 10, color)
        draw.text((x + 20, y + 14), title, font=FONT_HEADER, fill=CLR_TEXT_LIGHT)
        return x, y

    def draw_table_card(x, y, w, tbl_name, cols, header_color):
        h = 45 + len(cols) * 28 + 15
        draw_rounded_rect(draw, (x, y, x + w, y + h), 8, CLR_CARD_BG, CLR_BORDER, 2)
        # Header
        draw_rounded_rect(draw, (x, y, x + w, y + 38), 8, header_color)
        draw.rectangle([x, y + 28, x + w, y + 38], fill=header_color)
        draw.text((x + 12, y + 8), tbl_name, font=FONT_SUBHEADER, fill=CLR_TEXT_LIGHT)

        for idx, (col_name, col_type, col_key, col_desc) in enumerate(cols):
            ry = y + 44 + idx * 28
            if idx % 2 == 1:
                draw.rectangle([x + 1, ry, x + w - 1, ry + 26], fill=(248, 250, 252))

            # Key icon
            if col_key == "PK":
                draw_badge(draw, x + 8, ry + 2, "PK", CLR_AMBER, CLR_TEXT_LIGHT, FONT_TINY)
            elif col_key == "FK":
                draw_badge(draw, x + 8, ry + 2, "FK", CLR_BLUE_PRIMARY, CLR_TEXT_LIGHT, FONT_TINY)
            elif col_key == "UQ":
                draw_badge(draw, x + 8, ry + 2, "UQ", CLR_EMERALD, CLR_TEXT_LIGHT, FONT_TINY)
            else:
                draw.text((x + 15, ry + 4), "•", font=FONT_TINY, fill=CLR_TEXT_MUTED)

            draw.text((x + 48, ry + 4), col_name, font=FONT_SMALL_BOLD, fill=CLR_TEXT_DARK)
            draw.text((x + 185, ry + 4), col_type, font=FONT_TINY, fill=CLR_TEXT_MUTED)
            draw.text((x + 325, ry + 4), col_desc, font=FONT_TINY, fill=CLR_NAVY)

        return x, y, w, h

    # -------------------------------------------------------------
    # DB 1: Pharmacy_UserDB (Top Left)
    # -------------------------------------------------------------
    draw_db_box(50, 140, 480, "1. Database: [Pharmacy_UserDB]", CLR_AMBER, CLR_AMBER_LIGHT)
    user_cols = [
        ("UserId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("Name", "NVARCHAR(100)", "", "NOT NULL, Full Name"),
        ("Email", "NVARCHAR(150)", "UQ", "NOT NULL, Unique Index"),
        ("PhoneNumber", "NVARCHAR(20)", "", "NOT NULL, Contact Phone"),
        ("PasswordHash", "NVARCHAR(255)", "", "NOT NULL, PBKDF2/Salt Hash"),
        ("Role", "NVARCHAR(20)", "", "NOT NULL ('Admin' | 'Doctor')"),
        ("IsActive", "BIT", "", "NOT NULL, Default (1)"),
        ("CreatedDate", "DATETIME2(7)", "", "NOT NULL, Default SYSUTCDATETIME()")
    ]
    draw_table_card(50, 210, 480, "dbo.Users", user_cols, CLR_AMBER)

    # -------------------------------------------------------------
    # DB 2: Pharmacy_InventoryDB (Top Center & Right)
    # -------------------------------------------------------------
    draw_db_box(570, 140, 1430, "2. Database: [Pharmacy_InventoryDB] (3 Tables: Drugs, Suppliers, Inventory)", CLR_TEAL, CLR_TEAL_LIGHT)
    
    # Table 2a: Drugs
    drug_cols = [
        ("DrugId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("Name", "NVARCHAR(150)", "", "NOT NULL, Brand / Generic Name"),
        ("Description", "NVARCHAR(500)", "", "NULL, Clinical details"),
        ("Price", "DECIMAL(18,2)", "", "NOT NULL, Selling Price"),
        ("ExpiryDate", "DATETIME2(7)", "", "NOT NULL, Shelf life limit"),
        ("Quantity", "INT", "", "NOT NULL, Available units"),
        ("IsAvailable", "BIT", "", "NOT NULL, Default (1)")
    ]
    draw_table_card(570, 210, 460, "dbo.Drugs", drug_cols, CLR_TEAL)

    # Table 2b: Suppliers
    supplier_cols = [
        ("SupplierId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("SupplierName", "NVARCHAR(150)", "", "NOT NULL, Distributor Name"),
        ("Email", "NVARCHAR(150)", "", "NOT NULL, Contact Email"),
        ("PhoneNumber", "NVARCHAR(20)", "", "NOT NULL, Phone Support"),
        ("Address", "NVARCHAR(300)", "", "NOT NULL, Warehouse Address")
    ]
    draw_table_card(1060, 210, 460, "dbo.Suppliers", supplier_cols, CLR_TEAL)

    # Table 2c: Inventory
    inv_cols = [
        ("InventoryId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("SupplierId", "INT", "FK", "FK -> dbo.Suppliers(SupplierId)"),
        ("DrugId", "INT", "FK", "FK -> dbo.Drugs(DrugId)"),
        ("PurchasePrice", "DECIMAL(18,2)", "", "NOT NULL, Wholesale Cost"),
        ("QuantityAdded", "INT", "", "NOT NULL, Units received"),
        ("StockReceivedDate", "DATETIME2(7)", "", "NOT NULL, Default SYSUTCDATETIME()")
    ]
    draw_table_card(1550, 210, 450, "dbo.Inventory", inv_cols, CLR_TEAL)

    # Foreign key connectors inside InventoryDB
    draw_arrow(draw, (1030, 320), (1550, 270), CLR_TEAL, 2, "FK_Inventory_Drugs (1:M)", "top")
    draw_arrow(draw, (1520, 320), (1550, 300), CLR_TEAL, 2, "FK_Inventory_Suppliers (1:M)", "bottom")

    # -------------------------------------------------------------
    # DB 3: Pharmacy_OrderDB (Bottom Left)
    # -------------------------------------------------------------
    draw_db_box(50, 680, 1020, "3. Database: [Pharmacy_OrderDB] (2 Tables: Orders, OrderItems)", CLR_BLUE_PRIMARY, CLR_BLUE_LIGHT)
    
    order_cols = [
        ("OrderId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("DoctorID", "INT", "FK", "Logical FK -> UserDB.Users.UserId"),
        ("OrderDate", "DATETIME2(7)", "", "NOT NULL, Default SYSUTCDATETIME()"),
        ("TotalAmount", "DECIMAL(18,2)", "", "NOT NULL, Sum(Quantity * UnitPrice)"),
        ("Status", "NVARCHAR(20)", "", "Cart | Pending | Verified | PickedUp")
    ]
    draw_table_card(50, 750, 490, "dbo.Orders", order_cols, CLR_BLUE_PRIMARY)

    item_cols = [
        ("OrderItemId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("OrderId", "INT", "FK", "FK -> dbo.Orders(OrderId) ON DELETE CASCADE"),
        ("DrugId", "INT", "FK", "Logical FK -> InventoryDB.Drugs.DrugId"),
        ("DrugName", "NVARCHAR(150)", "", "Cached snapshot for invoice / audit"),
        ("Quantity", "INT", "", "NOT NULL, Units ordered"),
        ("UnitPrice", "DECIMAL(18,2)", "", "NOT NULL, Price at time of order")
    ]
    draw_table_card(570, 750, 500, "dbo.OrderItems", item_cols, CLR_BLUE_PRIMARY)

    # FK inside OrderDB
    draw_arrow(draw, (540, 830), (570, 830), CLR_BLUE_PRIMARY, 3, "FK_OrderItems_Orders (1:M)", "top")

    # -------------------------------------------------------------
    # DB 4: Pharmacy_PaymentDB (Bottom Center)
    # -------------------------------------------------------------
    draw_db_box(1110, 680, 500, "4. Database: [Pharmacy_PaymentDB]", CLR_EMERALD, CLR_EMERALD_LIGHT)
    
    pay_cols = [
        ("PaymentId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("OrderId", "INT", "UQ", "Logical FK -> Orders.OrderId (1:1 UNIQUE)"),
        ("Amount", "DECIMAL(18,2)", "", "NOT NULL, Transaction Amount"),
        ("PaymentDate", "DATETIME2(7)", "", "NOT NULL, Default SYSUTCDATETIME()"),
        ("PaymentMethod", "NVARCHAR(50)", "", "CreditCard | DebitCard | UPI | NetBanking"),
        ("PaymentStatus", "NVARCHAR(20)", "", "Pending | Completed | Failed"),
        ("TransactionReference", "NVARCHAR(100)", "", "Unique Gateway Reference Code")
    ]
    draw_table_card(1110, 750, 500, "dbo.Payments", pay_cols, CLR_EMERALD)

    # 1:1 Arrow from Orders to Payments
    draw_arrow(draw, (540, 890), (1110, 820), CLR_EMERALD, 3, "1:1 Relationship (Unique OrderId)", "top")

    # -------------------------------------------------------------
    # DB 5: Pharmacy_SaleReportDB (Bottom Right)
    # -------------------------------------------------------------
    draw_db_box(1650, 680, 900, "5. Database: [Pharmacy_SaleReportDB] (Standalone Analytics)", CLR_INDIGO, CLR_INDIGO_LIGHT)

    report_cols = [
        ("SaleReportId", "INT IDENTITY(1,1)", "PK", "Primary Key, Auto-increment"),
        ("ReportType", "NVARCHAR(20)", "", "NOT NULL (Daily | Weekly | Monthly | Yearly)"),
        ("FromDate", "DATETIME2(7)", "", "NOT NULL, Start of reporting period"),
        ("ToDate", "DATETIME2(7)", "", "NOT NULL, End of reporting period"),
        ("TotalOrders", "INT", "", "NOT NULL, Count of verified/picked-up orders"),
        ("TotalRevenue", "DECIMAL(18,2)", "", "NOT NULL, Aggregate revenue of orders"),
        ("GeneratedDate", "DATETIME2(7)", "", "NOT NULL, Default SYSUTCDATETIME()"),
        ("Profit", "DECIMAL(18,2)", "", "NOT NULL, Net Margin (Revenue - PurchaseCost)")
    ]
    draw_table_card(1650, 750, 520, "dbo.SaleReports", report_cols, CLR_INDIGO)

    # Informational card for reporting
    draw_rounded_rect(draw, (2200, 750, 2550, 1020), 8, CLR_INDIGO_LIGHT, CLR_INDIGO, 1)
    draw.text((2220, 770), "Financial Computations:", font=FONT_SMALL_BOLD, fill=CLR_INDIGO)
    draw.text((2220, 805), "• Revenue = Sum(Order.TotalAmount)", font=FONT_SMALL, fill=CLR_TEXT_DARK)
    draw.text((2220, 835), "• Profit = Revenue - TotalCOGS", font=FONT_SMALL, fill=CLR_TEXT_DARK)
    draw.text((2220, 865), "• Margin % = (Profit / Revenue) * 100", font=FONT_SMALL, fill=CLR_TEXT_DARK)
    draw.text((2220, 895), "• Formats: JSON, CSV, Printable Text", font=FONT_SMALL, fill=CLR_TEXT_DARK)
    draw.text((2220, 925), "• SQL Index: IX_SaleReports_ReportType", font=FONT_TINY, fill=CLR_NAVY)

    # Section 6: Comprehensive Physical SQL Constraints Legend
    draw_rounded_rect(draw, (50, 1150, 2550, 1820), 12, CLR_CARD_BG, CLR_BORDER, 2)
    draw_badge(draw, 70, 1165, "PHYSICAL DATABASE CONSTRAINTS, INDEXES & MIGRATION RULES", CLR_NAVY, CLR_TEXT_LIGHT)

    rules = [
        ("Database Isolation Pattern", "Each of the 5 microservices owns its private database. Cross-database queries are strictly prohibited; inter-service communication is achieved via HTTP REST APIs.", CLR_BLUE_LIGHT, CLR_BLUE_PRIMARY),
        ("Primary Key Standard", "All relational tables utilize INT IDENTITY(1,1) clustered primary keys for high-performance B-tree indexing and optimal query traversal.", CLR_AMBER_LIGHT, CLR_AMBER),
        ("Foreign Key & Cascade Integrity", "Intra-service relations (Order -> OrderItem, Supplier -> Inventory, Drug -> Inventory) enforce strict relational foreign key constraints with ON DELETE CASCADE or RESTRICT.", CLR_TEAL_LIGHT, CLR_TEAL),
        ("1:1 Unique Constraint", "Payment table enforces a non-clustered UNIQUE INDEX on [OrderId] ensuring strict 1:1 business rules: each order can only have one payment transaction.", CLR_EMERALD_LIGHT, CLR_EMERALD),
        ("Monetary Precision", "All currency and financial figures (Price, PurchasePrice, TotalAmount, Amount, TotalRevenue, Profit) utilize DECIMAL(18,2) to eliminate floating-point rounding errors.", CLR_INDIGO_LIGHT, CLR_INDIGO),
        ("Automatic Timestamping", "Creation timestamps (Users.CreatedDate, Orders.OrderDate, Payments.PaymentDate, SaleReports.GeneratedDate) default to SYSUTCDATETIME() / UTC for timezone uniformity.", CLR_ROSE_LIGHT, CLR_ROSE)
    ]

    for i, (rtitle, rdesc, rbg, rborder) in enumerate(rules):
        col_x = 70 + (i % 3) * 820
        row_y = 1220 + (i // 3) * 280
        draw_rounded_rect(draw, (col_x, row_y, col_x + 800, row_y + 240), 10, rbg, rborder, 1)
        draw.text((col_x + 20, row_y + 20), f"✓ {rtitle}", font=FONT_HEADER, fill=rborder)
        # Word wrap text
        words = rdesc.split(" ")
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 42:
                lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))

        for l_idx, line in enumerate(lines):
            draw.text((col_x + 20, row_y + 65 + l_idx * 30), line, font=FONT_BODY, fill=CLR_TEXT_DARK)

    save_image(img, "06_Database_Schema_Diagram.jpg")

print("Database diagram generator ready.")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("Generating all 6 diagrams in high-resolution JPG format with professional colors...")
    generate_solution_diagram()
    generate_usecase_diagram()
    generate_sequence_diagram()
    generate_flow_diagram()
    generate_er_diagram()
    generate_database_diagram()
    print("All 6 diagrams generated successfully!")
