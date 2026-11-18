import os
import math
from PIL import Image, ImageDraw, ImageFont

# Output Directories
OUT_DIR_WORKSPACE = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"
OUT_DIR_ARTIFACT = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\diagrams"

os.makedirs(OUT_DIR_WORKSPACE, exist_ok=True)
os.makedirs(OUT_DIR_ARTIFACT, exist_ok=True)

# ==============================================================================
# SUBSTANTIALLY ENLARGED, ALL-BOLD HIGH-CONTRAST TYPOGRAPHY HIERARCHY
# Every single text element is strictly BOLD (Segoe UI Bold) for clear viewing
# ==============================================================================
FONT_PATH_BOLD = "C:/Windows/Fonts/segoeuib.ttf"

FONT_MAIN_TITLE    = ImageFont.truetype(FONT_PATH_BOLD, 42) # Big center pill header
FONT_TOP_SECTION   = ImageFont.truetype(FONT_PATH_BOLD, 32) # Top-left section capsule
FONT_SECTION_TITLE = ImageFont.truetype(FONT_PATH_BOLD, 28) # Group container & box titles
FONT_SERVICE_TITLE = ImageFont.truetype(FONT_PATH_BOLD, 26) # Microservice card titles
FONT_TABLE_NAME    = ImageFont.truetype(FONT_PATH_BOLD, 25) # Relational table headers
FONT_NODE_TITLE    = ImageFont.truetype(FONT_PATH_BOLD, 24) # Flow steps & Use case names
FONT_CONTENT_BOLD  = ImageFont.truetype(FONT_PATH_BOLD, 22) # Attribute names, lifelines, steps
FONT_ATTR_BOLD     = ImageFont.truetype(FONT_PATH_BOLD, 20) # Data types, subs, secondary labels
FONT_BADGE_BOLD    = ImageFont.truetype(FONT_PATH_BOLD, 19) # Badges, pills, numbers
FONT_NOTE_BOLD     = ImageFont.truetype(FONT_PATH_BOLD, 19) # Explanatory bullet points & notes

# Aliases for backward compatibility
FONT_HEADER        = FONT_SECTION_TITLE
FONT_CARD_HEADER   = FONT_SERVICE_TITLE
FONT_SUBHEADER     = FONT_TABLE_NAME
FONT_BOLD          = FONT_CONTENT_BOLD
FONT_REGULAR       = FONT_CONTENT_BOLD
FONT_SMALL_BOLD    = FONT_ATTR_BOLD
FONT_SMALL         = FONT_ATTR_BOLD
FONT_TINY_BOLD     = FONT_BADGE_BOLD
FONT_TINY          = FONT_BADGE_BOLD

# Color Palette (Crisp, High-Contrast Professional Colors Matching Reference Line Art)
CLR_WHITE         = (255, 255, 255)
CLR_BG_PAGE       = (253, 254, 255)
CLR_BLACK         = (15, 20, 28)
CLR_DARK_SLATE    = (30, 41, 59)
CLR_BORDER        = (71, 85, 105)       # Strong outer frame border
CLR_BORDER_THIN   = (148, 163, 184)
CLR_BORDER_LIGHT  = (203, 213, 225)

# Microservices Themed Colors
CLR_AUTH_MAIN     = (217, 119, 6)       # Amber / Orange
CLR_AUTH_BG       = (254, 243, 199)
CLR_AUTH_BORDER   = (245, 158, 11)

CLR_INV_MAIN      = (5, 150, 105)        # Emerald Green
CLR_INV_BG        = (236, 253, 245)
CLR_INV_BORDER    = (16, 185, 129)

CLR_ORDER_MAIN    = (29, 78, 216)       # Royal Blue
CLR_ORDER_BG      = (239, 246, 255)
CLR_ORDER_BORDER  = (59, 130, 246)

CLR_PAY_MAIN      = (124, 58, 237)      # Purple
CLR_PAY_BG        = (245, 243, 255)
CLR_PAY_BORDER    = (139, 92, 246)

CLR_REP_MAIN      = (225, 29, 72)       # Crimson / Rose
CLR_REP_BG        = (255, 241, 242)
CLR_REP_BORDER    = (244, 63, 94)

CLR_GATE_MAIN     = (15, 23, 42)        # Slate / Charcoal
CLR_GATE_BG       = (241, 245, 249)
CLR_GATE_BORDER   = (71, 85, 105)

def draw_reference_frame(draw, W, H, section_tag, main_title):
    # Outer frame
    draw.rounded_rectangle([18, 18, W - 18, H - 18], radius=20, outline=CLR_BORDER, width=3)
    
    # Top-left section capsule
    tag_bbox = FONT_TOP_SECTION.getbbox(section_tag)
    tag_w = tag_bbox[2] - tag_bbox[0] + 50
    draw.rounded_rectangle([32, 26, 32 + tag_w, 86], radius=12, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((54, 36), section_tag, font=FONT_TOP_SECTION, fill=CLR_BLACK)

    # Center main title pill
    title_bbox = FONT_MAIN_TITLE.getbbox(main_title)
    title_w = title_bbox[2] - title_bbox[0] + 70
    title_x = (W - title_w) // 2
    draw.rounded_rectangle([title_x, 82, title_x + title_w, 156], radius=30, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((title_x + 35, 94), main_title, font=FONT_MAIN_TITLE, fill=CLR_BLACK)

def draw_badge(draw, x, y, text, bg_color, text_color, font=FONT_BADGE_BOLD):
    bbox = font.getbbox(text)
    w = (bbox[2] - bbox[0]) + 22
    h = (bbox[3] - bbox[1]) + 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg_color)
    draw.text((x + 11, y + 5), text, font=font, fill=text_color)
    return w, h

def draw_cylinder_db(draw, x, y, w, h, db_name, tables_str, theme_color, bg_color):
    cap_h = 24
    draw.rectangle([x, y + cap_h//2, x + w, y + h - cap_h//2], fill=bg_color, outline=theme_color, width=3)
    draw.ellipse([x, y + h - cap_h, x + w, y + h], fill=bg_color, outline=theme_color, width=3)
    draw.arc([x, y + h//2 - cap_h//2, x + w, y + h//2 + cap_h//2], 0, 180, fill=theme_color, width=2)
    draw.ellipse([x, y, x + w, y + cap_h], fill=theme_color, outline=theme_color, width=3)
    
    draw.text((x + 20, y + 28), db_name, font=FONT_SERVICE_TITLE, fill=theme_color)
    draw.text((x + 20, y + 64), tables_str, font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

def draw_arrow_ref(draw, start, end, color=CLR_BLACK, width=3, label=None, label_above=True):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    hlen = 14
    p1 = (x2 - hlen * math.cos(angle - math.pi / 6), y2 - hlen * math.sin(angle - math.pi / 6))
    p2 = (x2 - hlen * math.cos(angle + math.pi / 6), y2 - hlen * math.sin(angle + math.pi / 6))
    draw.polygon([(x2, y2), p1, p2], fill=color)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ly = my - 28 if label_above else my + 10
        bbox = FONT_BADGE_BOLD.getbbox(label)
        lw = bbox[2] - bbox[0] + 20
        draw.rounded_rectangle([mx - lw//2, ly - 3, mx + lw//2, ly + 25], radius=6, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=2)
        draw.text((mx - lw//2 + 10, ly), label, font=FONT_BADGE_BOLD, fill=color)

def save_both(img, name):
    p1 = os.path.join(OUT_DIR_WORKSPACE, name)
    p2 = os.path.join(OUT_DIR_ARTIFACT, name)
    img.save(p1, "JPEG", quality=95)
    img.save(p2, "JPEG", quality=95)
    print(f"Generated Enlarged-Font JPG: {name} (Dimensions: {img.size[0]}x{img.size[1]})")

# ==============================================================================
# 1. ARCHITECTURE DIAGRAM (High Resolution 3200x2200, All-Bold Crisp Elements)
# ==============================================================================
def generate_ref_architecture_diagram():
    W, H = 3200, 2200
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "4.0 Architecture Diagram", "Pharmacy Management System – Microservices Architecture (5 Services)")

    # Left Column: Clients Box
    draw.rounded_rectangle([40, 175, 305, 1220], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((105, 195), "Clients", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(40, 245), (305, 245)], fill=CLR_BORDER, width=2)

    clients = [
        ("Web UI", "(Doctor / Admin)", 275, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Swagger UI", "(API Testing)", 585, CLR_INV_MAIN, CLR_INV_BG),
        ("Other Clients", "(Mobile / POS)", 895, CLR_AUTH_MAIN, CLR_AUTH_BG)
    ]
    for c_title, c_sub, cy, clr, bg in clients:
        draw.rounded_rectangle([55, cy, 290, cy + 245], radius=14, fill=bg, outline=clr, width=2)
        draw.rounded_rectangle([80, cy + 20, 265, cy + 135], radius=8, fill=CLR_WHITE, outline=clr, width=2)
        draw.line([(105, cy + 75), (240, cy + 75)], fill=clr, width=2)
        draw.line([(172, cy + 135), (172, cy + 158)], fill=clr, width=2)
        draw.line([(140, cy + 158), (205, cy + 158)], fill=clr, width=2)

        draw.text((95, cy + 172), c_title, font=FONT_NODE_TITLE, fill=CLR_BLACK)
        draw.text((72, cy + 205), c_sub, font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(305, 310), (345, 310)], fill=CLR_BLACK, width=3)

    # Center Big Dashed Box: Microservices Core
    draw.rounded_rectangle([345, 175, 2750, 1220], radius=20, outline=CLR_BORDER, width=3)

    # API Gateway Banner
    draw.rounded_rectangle([375, 200, 2720, 315], radius=18, fill=CLR_GATE_BG, outline=CLR_GATE_BORDER, width=3)
    draw.ellipse([410, 235, 455, 280], fill=CLR_WHITE, outline=CLR_GATE_MAIN, width=3)
    draw.line([(432, 235), (432, 280)], fill=CLR_GATE_MAIN, width=3)
    draw.line([(410, 257), (455, 257)], fill=CLR_GATE_MAIN, width=3)
    draw.text((480, 222), "API Gateway (YARP / Reverse Proxy)", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.text((480, 266), "Request Routing | Load Balancing | JWT Bearer Validation | Rate Limiting | Health Checks | Swagger Aggregation", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(1547, 315), (1547, 350)], fill=CLR_BLACK, width=3)
    draw.line([(595, 350), (2500, 350)], fill=CLR_BLACK, width=3)

    # 5 Microservices Cards
    services_data = [
        {
            "name": "Auth Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": [
                "• User Management",
                "• Role Management (Admin/Doc)",
                "• Authentication (JWT)",
                "• Authorization (RBAC)",
                "• Doctor Role Validation"
            ],
            "db_name": "AuthDB",
            "db_tables": "(Users Table)",
            "theme": CLR_AUTH_MAIN,
            "bg": CLR_AUTH_BG,
            "x": 375,
            "w": 440
        },
        {
            "name": "Inventory Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": [
                "• Drugs Catalog & Pricing",
                "• Supplier Management",
                "• Stock Inward & Tracking",
                "• Atomic Stock Deduction",
                "• Availability Management"
            ],
            "db_name": "InventoryDB",
            "db_tables": "(Drugs, Suppliers, Inv)",
            "theme": CLR_INV_MAIN,
            "bg": CLR_INV_BG,
            "x": 845,
            "w": 440
        },
        {
            "name": "Order Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": [
                "• Doctor Orders & Buying",
                "• Cart / Pending Processing",
                "• Admin Order Validation",
                "• Order Verification",
                "• Handover to PickedUp"
            ],
            "db_name": "OrderDB",
            "db_tables": "(Orders, OrderItems)",
            "theme": CLR_ORDER_MAIN,
            "bg": CLR_ORDER_BG,
            "x": 1315,
            "w": 440
        },
        {
            "name": "Payment Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": [
                "• Order Payment Checkout",
                "• 1:1 Order Transaction Rule",
                "• Multi-Payment (Card/UPI)",
                "• Transaction Reference Code",
                "• Payment Status Tracking"
            ],
            "db_name": "PaymentDB",
            "db_tables": "(Payments Table)",
            "theme": CLR_PAY_MAIN,
            "bg": CLR_PAY_BG,
            "x": 1785,
            "w": 440
        },
        {
            "name": "SaleReport Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": [
                "• Financial Reporting",
                "• Daily / Wk / Mo / Yr Range",
                "• Revenue & Profit Analytics",
                "• CSV Spreadsheet Export",
                "• Formatted Print Views"
            ],
            "db_name": "SaleReportDB",
            "db_tables": "(SaleReports Table)",
            "theme": CLR_REP_MAIN,
            "bg": CLR_REP_BG,
            "x": 2255,
            "w": 440
        }
    ]

    for svc in services_data:
        sx = svc["x"]
        sw = svc["w"]
        theme = svc["theme"]
        bg = svc["bg"]

        draw_arrow_ref(draw, (sx + sw//2, 350), (sx + sw//2, 385), CLR_BLACK, 3)

        # Microservice card box
        draw.rounded_rectangle([sx, 385, sx + sw, 840], radius=16, fill=CLR_WHITE, outline=theme, width=3)
        draw.rounded_rectangle([sx, 385, sx + sw, 475], radius=16, fill=bg, outline=theme, width=1)
        draw.rectangle([sx, 440, sx + sw, 475], fill=bg)

        draw.ellipse([sx + 18, 400, sx + 68, 450], fill=theme)
        draw.text((sx + 30, 408), "★", font=FONT_SERVICE_TITLE, fill=CLR_WHITE)

        draw.text((sx + 80, 400), svc["name"], font=FONT_SERVICE_TITLE, fill=CLR_BLACK)
        draw.text((sx + 80, 436), svc["tech"], font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

        draw.line([(sx, 475), (sx + sw, 475)], fill=theme, width=2)

        for b_idx, bullet in enumerate(svc["bullets"]):
            draw.text((sx + 20, 500 + b_idx * 64), bullet, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

        draw_arrow_ref(draw, (sx + sw//2, 840), (sx + sw//2, 905), theme, 3)
        draw_cylinder_db(draw, sx + 25, 905, sw - 50, 110, svc["db_name"], svc["db_tables"], theme, bg)

    # Bi-directional arrows between services
    draw_arrow_ref(draw, (1285, 560), (1315, 560), CLR_BLACK, 3)
    draw_arrow_ref(draw, (1315, 590), (1285, 590), CLR_BLACK, 3)

    draw_arrow_ref(draw, (1755, 560), (1785, 560), CLR_BLACK, 3)
    draw_arrow_ref(draw, (1785, 590), (1755, 590), CLR_BLACK, 3)

    # Bottom shared module
    draw.rounded_rectangle([600, 1075, 2350, 1185], radius=14, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rounded_rectangle([625, 1095, 680, 1150], radius=8, fill=CLR_GATE_BG, outline=CLR_GATE_MAIN, width=2)
    draw.text((642, 1105), "✉", font=FONT_SERVICE_TITLE, fill=CLR_GATE_MAIN)
    draw.text((700, 1092), "Common Infrastructure & Notification Module (Shared Library)", font=FONT_SERVICE_TITLE, fill=CLR_BLACK)
    draw.text((700, 1132), "(JWT Bearer Token Handler, PBKDF2 Password Hasher, ApiResponse Envelope, Order Verification & Stock Alerts)", font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(1535, 1015), (1535, 1075)], fill=CLR_BORDER, width=2)

    # Right Column: Technology Stack Box
    draw.rounded_rectangle([2775, 175, 3160, 1220], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((2845, 195), "Technology Stack", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(2775, 245), (3160, 245)], fill=CLR_BORDER, width=2)

    tech_items = [
        (".NET", "ASP.NET Core Web API\n(.NET 8 LTS)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("C#", "C# 12 Language\n(LINQ & Async)", CLR_INV_MAIN, CLR_INV_BG),
        ("SQL", "SQL Server 2022\n(5 Separate DBs)", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("YARP", "YARP / API Gateway\n(Reverse Proxy)", CLR_GATE_MAIN, CLR_GATE_BG),
        ("JWT", "JWT Authentication\n& RBAC (Role Claims)", CLR_PAY_MAIN, CLR_PAY_BG),
        ("EF", "Entity Framework Core 8\n(Code-First & LINQ)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("DOC", "Docker & Compose\n(Multi-Container)", CLR_REP_MAIN, CLR_REP_BG),
        ("SWAG", "Swagger / OpenAPI 3.0\n(Lock Authorize UI)", CLR_INV_MAIN, CLR_INV_BG)
    ]
    for idx, (badge, label, clr, bg) in enumerate(tech_items):
        ty = 265 + idx * 115
        draw.rounded_rectangle([2795, ty, 2875, ty + 70], radius=10, fill=bg, outline=clr, width=2)
        draw.text((2807, ty + 20), badge, font=FONT_CONTENT_BOLD, fill=clr)
        
        lines = label.split("\n")
        draw.text((2890, ty + 8), lines[0], font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        if len(lines) > 1:
            draw.text((2890, ty + 38), lines[1], font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Bottom Section: 3 Split Cards
    # Bottom Card 1: Service Interactions
    draw.rounded_rectangle([40, 1260, 1020, 2150], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((65, 1280), "Service Interactions – Order Flow (High Level)", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(40, 1325), (1020, 1325)], fill=CLR_BORDER, width=2)

    draw.ellipse([65, 1420, 140, 1495], fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=3)
    draw.text((80, 1440), "Dr", font=FONT_SERVICE_TITLE, fill=CLR_ORDER_MAIN)
    draw.text((55, 1510), "Doctor User", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    draw.rounded_rectangle([210, 1400, 440, 1530], radius=12, fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((235, 1430), "Order Service", font=FONT_NODE_TITLE, fill=CLR_ORDER_MAIN)
    draw.text((225, 1470), "(POST /api/orders)", font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)
    
    draw_arrow_ref(draw, (140, 1465), (210, 1465), CLR_BLACK, 3)
    draw.ellipse([160, 1425, 192, 1457], fill=CLR_BLACK)
    draw.text((170, 1428), "1", font=FONT_BADGE_BOLD, fill=CLR_WHITE)
    draw.text((140, 1395), "Create Order", font=FONT_ATTR_BOLD, fill=CLR_BLACK)

    draw.rounded_rectangle([640, 1400, 970, 1530], radius=12, fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((670, 1430), "Inventory Service", font=FONT_NODE_TITLE, fill=CLR_INV_MAIN)
    draw.text((660, 1470), "(Deduct Stock & Qty)", font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow_ref(draw, (440, 1445), (640, 1445), CLR_BLACK, 3)
    draw.ellipse([525, 1410, 557, 1442], fill=CLR_BLACK)
    draw.text((535, 1413), "2", font=FONT_BADGE_BOLD, fill=CLR_WHITE)
    draw.text((480, 1385), "Validate Stock", font=FONT_ATTR_BOLD, fill=CLR_BLACK)

    draw_arrow_ref(draw, (640, 1495), (440, 1495), CLR_BLACK, 3)
    draw.ellipse([525, 1505, 557, 1537], fill=CLR_BLACK)
    draw.text((535, 1508), "3", font=FONT_BADGE_BOLD, fill=CLR_WHITE)
    draw.text((475, 1545), "Stock Deducted OK", font=FONT_ATTR_BOLD, fill=CLR_BLACK)

    draw.rounded_rectangle([320, 1690, 600, 1810], radius=12, fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((350, 1715), "Payment Service", font=FONT_NODE_TITLE, fill=CLR_PAY_MAIN)
    draw.text((340, 1755), "(Process 1:1 Payment)", font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow_ref(draw, (325, 1530), (325, 1690), CLR_BLACK, 3)
    draw.ellipse([335, 1595, 367, 1627], fill=CLR_BLACK)
    draw.text((345, 1598), "4", font=FONT_BADGE_BOLD, fill=CLR_WHITE)
    draw.text((375, 1598), "Trigger Payment", font=FONT_ATTR_BOLD, fill=CLR_BLACK)

    draw.rounded_rectangle([680, 1690, 970, 1810], radius=12, fill=CLR_AUTH_BG, outline=CLR_AUTH_MAIN, width=2)
    draw.text((720, 1715), "Admin Handover", font=FONT_NODE_TITLE, fill=CLR_AUTH_MAIN)
    draw.text((700, 1755), "(Verify & Mark PickedUp)", font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow_ref(draw, (600, 1750), (680, 1750), CLR_BLACK, 3)
    draw.ellipse([625, 1720, 657, 1752], fill=CLR_BLACK)
    draw.text((635, 1723), "5", font=FONT_BADGE_BOLD, fill=CLR_WHITE)

    draw.rounded_rectangle([65, 1860, 995, 2120], radius=12, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((85, 1880), "Execution Details:", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
    draw.text((85, 1920), "• Doctor signs in and submits order through Swagger / API Gateway.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)
    draw.text((85, 1965), "• Order Service invokes Inventory Service to decrement quantities.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)
    draw.text((85, 2010), "• Payment Service confirms 1:1 transaction and writes Payment record.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)
    draw.text((85, 2055), "• Admin validates order items, marks 'Verified', and completes handover.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)

    # Bottom Card 2: Database Distribution Table
    draw.rounded_rectangle([1050, 1260, 2100, 2150], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1260, 1280), "Database Distribution Table", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(1050, 1325), (2100, 1325)], fill=CLR_BORDER, width=2)

    draw.rectangle([1075, 1350, 2075, 1415], fill=CLR_GATE_MAIN)
    draw.text((1100, 1370), "Microservice", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)
    draw.text((1375, 1370), "Dedicated Database", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)
    draw.text((1690, 1370), "Key Relational Tables", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)

    db_rows = [
        ("Auth Service", "Pharmacy_UserDB", "Users (UserId PK, Role, PasswordHash)", CLR_AUTH_BG, CLR_AUTH_MAIN),
        ("Inventory Service", "Pharmacy_InventoryDB", "Drugs, Suppliers, Inventory (1:M)", CLR_INV_BG, CLR_INV_MAIN),
        ("Order Service", "Pharmacy_OrderDB", "Orders, OrderItems (1:M)", CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Payment Service", "Pharmacy_PaymentDB", "Payments (1:1 with Orders.OrderId)", CLR_PAY_BG, CLR_PAY_MAIN),
        ("SaleReport Service", "Pharmacy_SaleReportDB", "SaleReports (Standalone Financials)", CLR_REP_BG, CLR_REP_MAIN)
    ]
    for r_idx, (s_name, db_name, tbls, row_bg, border_clr) in enumerate(db_rows):
        ry = 1425 + r_idx * 95
        draw.rectangle([1075, ry, 2075, ry + 90], fill=row_bg if r_idx % 2 == 1 else CLR_WHITE)
        draw.line([(1075, ry + 90), (2075, ry + 90)], fill=CLR_BORDER_LIGHT, width=1)
        
        draw.ellipse([1095, ry + 30, 1125, ry + 60], fill=border_clr)
        draw.text((1138, ry + 30), s_name, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        draw.text((1375, ry + 30), db_name, font=FONT_CONTENT_BOLD, fill=border_clr)
        draw.text((1690, ry + 30), tbls, font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(1350, 1350), (1350, 1900)], fill=CLR_BORDER_LIGHT, width=2)
    draw.line([(1665, 1350), (1665, 1900)], fill=CLR_BORDER_LIGHT, width=2)
    draw.rectangle([1075, 1350, 2075, 1900], outline=CLR_BORDER, width=2)

    draw.rounded_rectangle([1075, 1930, 2075, 2120], radius=12, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((1100, 1950), "Database Architecture Rules:", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
    draw.text((1100, 1990), "• Database-Per-Service pattern strictly enforced; zero cross-database access.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)
    draw.text((1100, 2035), "• Cross-service entity mapping handled via logical FKs and HTTP REST.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)
    draw.text((1100, 2080), "• Fully scripted via scripts/InitDatabases.sql with idempotent seeders.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)

    # Bottom Card 3: Key Highlights
    draw.rounded_rectangle([2130, 1260, 3160, 2150], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((2390, 1280), "Key Highlights", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(2130, 1325), (3160, 1325)], fill=CLR_BORDER, width=2)

    highlights = [
        ("5 Dedicated Microservices", "Decoupled services for Auth, Inventory, Orders, Payments, and Sales Reporting with zero cross-database query leakage.", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Internal MVC Architecture", "Each microservice follows internal MVC separation: Controllers expose REST APIs, Services enforce logic, Repositories run LINQ.", CLR_INV_MAIN, CLR_INV_BG),
        ("Role-Based Access Control", "JWT tokens carry role claims (Admin vs Doctor) enforcing endpoint access restrictions across Swagger and the API Gateway.", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Order Verification & PickedUp", "Admin validates doctor orders, updates status to 'Verified', and tracks final customer fulfillment via 'PickedUp' state.", CLR_PAY_MAIN, CLR_PAY_BG),
        ("Automated Financial Reports", "SaleReport Service aggregates order data, computes net profit over wholesale cost, and outputs CSV spreadsheets and print views.", CLR_REP_MAIN, CLR_REP_BG)
    ]
    for h_idx, (htitle, hdesc, clr, bg) in enumerate(highlights):
        hy = 1350 + h_idx * 155
        draw.rounded_rectangle([2155, hy, 3135, hy + 140], radius=12, fill=bg, outline=clr, width=2)
        draw.ellipse([2175, hy + 20, 2220, hy + 65], fill=clr)
        draw.text((2190, hy + 26), "✓", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)
        draw.text((2235, hy + 26), htitle, font=FONT_NODE_TITLE, fill=CLR_BLACK)
        
        words = hdesc.split(" ")
        l1, l2 = [], []
        for w in words:
            if len(" ".join(l1 + [w])) < 58:
                l1.append(w)
            else:
                l2.append(w)
        draw.text((2175, hy + 75), " ".join(l1), font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)
        if l2:
            draw.text((2175, hy + 105), " ".join(l2), font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

    save_both(img, "01_Solution_Architecture_Diagram.jpg")

# ==============================================================================
# 2. DATABASE DIAGRAM (High Resolution 3200x2400, All-Bold Headers & Columns)
# ==============================================================================
def generate_ref_database_diagram():
    W, H = 3200, 2400
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "2.0 Database Diagram", "Pharmacy Management System – Database Diagram")

    def draw_ref_table(x, y, w, tbl_name, cols, theme_clr, bg_clr):
        row_h = 48
        h = 60 + len(cols) * row_h + 10
        draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CLR_WHITE, outline=theme_clr, width=3)
        draw.rounded_rectangle([x, y, x + w, y + 54], radius=12, fill=bg_clr, outline=theme_clr, width=1)
        draw.rectangle([x, y + 40, x + w, y + 54], fill=bg_clr)
        draw.text((x + 20, y + 12), tbl_name, font=FONT_TABLE_NAME, fill=theme_clr)

        for idx, (key_type, col_name, data_type) in enumerate(cols):
            ry = y + 58 + idx * row_h
            draw.line([(x, ry), (x + w, ry)], fill=CLR_BORDER_LIGHT, width=1)
            draw.line([(x + 65, ry), (x + 65, ry + row_h)], fill=CLR_BORDER_LIGHT, width=1)

            if key_type == "PK":
                draw.text((x + 12, ry + 10), "PK", font=FONT_ATTR_BOLD, fill=CLR_AUTH_MAIN)
            elif key_type == "FK":
                draw.text((x + 12, ry + 10), "FK", font=FONT_ATTR_BOLD, fill=CLR_ORDER_MAIN)

            draw.text((x + 80, ry + 10), col_name, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
            draw.text((x + w - 240, ry + 10), data_type, font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

        return x, y, w, h

    # Group 1: Auth Service – AuthDB
    draw.rounded_rectangle([40, 175, 790, 720], radius=18, fill=CLR_WHITE, outline=CLR_AUTH_BORDER, width=3)
    draw.rounded_rectangle([70, 195, 480, 255], radius=10, fill=CLR_AUTH_BG, outline=CLR_AUTH_MAIN, width=2)
    draw.ellipse([82, 210, 115, 243], fill=CLR_AUTH_MAIN)
    draw.text((130, 212), "Auth Service – AuthDB", font=FONT_TABLE_NAME, fill=CLR_AUTH_MAIN)

    user_cols = [
        ("PK", "UserId", "int"),
        ("", "Name", "nvarchar(100)"),
        ("", "Email", "nvarchar(150)"),
        ("", "PhoneNumber", "nvarchar(20)"),
        ("", "PasswordHash", "nvarchar(255)"),
        ("", "Role", "nvarchar(20)"),
        ("", "IsActive", "bit"),
        ("", "CreatedDate", "datetime2")
    ]
    draw_ref_table(70, 275, 680, "Users", user_cols, CLR_AUTH_MAIN, CLR_AUTH_BG)

    # Group 2: Inventory Service – InventoryDB
    draw.rounded_rectangle([820, 175, 3160, 720], radius=18, fill=CLR_WHITE, outline=CLR_INV_BORDER, width=3)
    draw.rounded_rectangle([850, 195, 1370, 255], radius=10, fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.ellipse([862, 210, 895, 243], fill=CLR_INV_MAIN)
    draw.text((910, 212), "Inventory Service – InventoryDB", font=FONT_TABLE_NAME, fill=CLR_INV_MAIN)

    drug_cols = [
        ("PK", "DrugId", "int"),
        ("", "Name", "nvarchar(150)"),
        ("", "Description", "nvarchar(500)"),
        ("", "Price", "decimal(18,2)"),
        ("", "ExpiryDate", "datetime2"),
        ("", "Quantity", "int"),
        ("", "IsAvailable", "bit")
    ]
    draw_ref_table(850, 275, 710, "Drugs", drug_cols, CLR_INV_MAIN, CLR_INV_BG)

    supp_cols = [
        ("PK", "SupplierId", "int"),
        ("", "SupplierName", "nvarchar(150)"),
        ("", "Email", "nvarchar(150)"),
        ("", "PhoneNumber", "nvarchar(20)"),
        ("", "Address", "nvarchar(300)")
    ]
    draw_ref_table(1600, 275, 710, "Suppliers", supp_cols, CLR_INV_MAIN, CLR_INV_BG)

    inv_cols = [
        ("PK", "InventoryId", "int"),
        ("FK", "SupplierId", "int"),
        ("FK", "DrugId", "int"),
        ("", "PurchasePrice", "decimal(18,2)"),
        ("", "QuantityAdded", "int"),
        ("", "StockReceivedDate", "datetime2")
    ]
    draw_ref_table(2350, 275, 770, "Inventory", inv_cols, CLR_INV_MAIN, CLR_INV_BG)

    # Connectors inside InventoryDB
    draw.line([(1560, 315), (1580, 315), (1580, 660), (2325, 660), (2325, 390), (2350, 390)], fill=CLR_INV_MAIN, width=3)
    draw.text((1565, 280), "1", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((2330, 350), "N", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)

    draw.line([(2310, 315), (2350, 315)], fill=CLR_INV_MAIN, width=3)
    draw.text((2315, 280), "1", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((2335, 280), "N", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)

    # Group 3: Order Service – OrderDB
    draw.rounded_rectangle([40, 760, 1660, 1420], radius=18, fill=CLR_WHITE, outline=CLR_ORDER_BORDER, width=3)
    draw.rounded_rectangle([70, 780, 500, 840], radius=10, fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.ellipse([82, 795, 115, 828], fill=CLR_ORDER_MAIN)
    draw.text((130, 797), "Order Service – OrderDB", font=FONT_TABLE_NAME, fill=CLR_ORDER_MAIN)

    order_cols = [
        ("PK", "OrderId", "int"),
        ("FK", "DoctorID", "int"),
        ("", "OrderDate", "datetime2"),
        ("", "TotalAmount", "decimal(18,2)"),
        ("", "Status", "nvarchar(20)")
    ]
    draw_ref_table(70, 860, 720, "Orders", order_cols, CLR_ORDER_MAIN, CLR_ORDER_BG)

    item_cols = [
        ("PK", "OrderItemId", "int"),
        ("FK", "OrderId", "int"),
        ("FK", "DrugId", "int"),
        ("", "DrugName", "nvarchar(150)"),
        ("", "Quantity", "int"),
        ("", "UnitPrice", "decimal(18,2)")
    ]
    draw_ref_table(870, 860, 750, "OrderItems", item_cols, CLR_ORDER_MAIN, CLR_ORDER_BG)

    # Orders (1) to OrderItems (N)
    draw.line([(790, 910), (870, 910)], fill=CLR_ORDER_MAIN, width=3)
    draw.text((800, 875), "1", font=FONT_SERVICE_TITLE, fill=CLR_ORDER_MAIN)
    draw.text((850, 875), "N", font=FONT_SERVICE_TITLE, fill=CLR_ORDER_MAIN)

    # Group 4: Payment Service – PaymentDB
    draw.rounded_rectangle([1700, 760, 2410, 1420], radius=18, fill=CLR_WHITE, outline=CLR_PAY_BORDER, width=3)
    draw.rounded_rectangle([1730, 780, 2220, 840], radius=10, fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.ellipse([1742, 795, 1775, 828], fill=CLR_PAY_MAIN)
    draw.text((1790, 797), "Payment Service – PaymentDB", font=FONT_TABLE_NAME, fill=CLR_PAY_MAIN)

    pay_cols = [
        ("PK", "PaymentId", "int"),
        ("FK", "OrderId", "int (Unique - 1:1)"),
        ("", "Amount", "decimal(18,2)"),
        ("", "PaymentDate", "datetime2"),
        ("", "PaymentMethod", "nvarchar(50)"),
        ("", "PaymentStatus", "nvarchar(20)"),
        ("", "TransactionReference", "nvarchar(100)")
    ]
    draw_ref_table(1730, 860, 650, "Payments", pay_cols, CLR_PAY_MAIN, CLR_PAY_BG)

    # Group 5: SaleReport Service – SaleReportDB
    draw.rounded_rectangle([2450, 760, 3160, 1420], radius=18, fill=CLR_WHITE, outline=CLR_REP_BORDER, width=3)
    draw.rounded_rectangle([2480, 780, 3010, 840], radius=10, fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.ellipse([2492, 795, 2525, 828], fill=CLR_REP_MAIN)
    draw.text((2540, 797), "SaleReport – SaleReportDB", font=FONT_TABLE_NAME, fill=CLR_REP_MAIN)

    rep_cols = [
        ("PK", "SaleReportId", "int"),
        ("", "ReportType", "nvarchar(20)"),
        ("", "FromDate", "datetime2"),
        ("", "ToDate", "datetime2"),
        ("", "TotalOrders", "int"),
        ("", "TotalRevenue", "decimal(18,2)"),
        ("", "GeneratedDate", "datetime2"),
        ("", "Profit", "decimal(18,2)")
    ]
    draw_ref_table(2480, 860, 650, "SaleReports", rep_cols, CLR_REP_MAIN, CLR_REP_BG)

    # Bottom Section: 3 Boxes
    # Box 1: Summary Table
    draw.rounded_rectangle([40, 1460, 1180, 2350], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((65, 1480), "Database Summary", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(40, 1525), (1180, 1525)], fill=CLR_BORDER, width=2)

    draw.rectangle([65, 1550, 1155, 1615], fill=CLR_GATE_MAIN)
    draw.text((90, 1570), "Database (Service)", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)
    draw.text((540, 1570), "Contained Tables", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)

    summary_rows = [
        ("AuthDB (Auth Service)", "Users Table", CLR_AUTH_BG, CLR_AUTH_MAIN),
        ("InventoryDB (Inventory Service)", "Drugs, Suppliers, Inventory Tables", CLR_INV_BG, CLR_INV_MAIN),
        ("OrderDB (Order Service)", "Orders, OrderItems Tables", CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("PaymentDB (Payment Service)", "Payments Table (1:1 with Order)", CLR_PAY_BG, CLR_PAY_MAIN),
        ("SaleReportDB (SaleReport Service)", "SaleReports Table (Aggregated)", CLR_REP_BG, CLR_REP_MAIN)
    ]
    for idx, (db_title, tbl_str, bg_c, thm_c) in enumerate(summary_rows):
        ry = 1625 + idx * 95
        draw.rectangle([65, ry, 1155, ry + 90], fill=bg_c if idx % 2 == 1 else CLR_WHITE)
        draw.line([(65, ry + 90), (1155, ry + 90)], fill=CLR_BORDER_LIGHT, width=1)
        draw.ellipse([85, ry + 30, 112, ry + 57], fill=thm_c)
        draw.text((125, ry + 30), db_title, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        draw.text((540, ry + 30), tbl_str, font=FONT_CONTENT_BOLD, fill=thm_c)

    draw.rectangle([65, 1550, 1155, 2100], outline=CLR_BORDER, width=2)
    draw.line([(510, 1550), (510, 2100)], fill=CLR_BORDER, width=2)

    draw.rounded_rectangle([65, 2130, 1155, 2320], radius=12, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((85, 2150), "Schema Isolation Principle:", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
    draw.text((85, 2195), "• Each microservice controls its own isolated schema and migrations.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)
    draw.text((85, 2240), "• Cross-service foreign keys are logical, resolved via REST APIs.", font=FONT_NOTE_BOLD, fill=CLR_DARK_SLATE)

    # Box 2: Legend
    draw.rounded_rectangle([1210, 1460, 1880, 2350], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1235, 1480), "Legend", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(1210, 1525), (1880, 1525)], fill=CLR_BORDER, width=2)

    legends = [
        ("PK", "Primary Key (Clustered Index, Auto-Increment)", CLR_AUTH_MAIN),
        ("FK", "Foreign Key (Referential Constraint)", CLR_ORDER_MAIN),
        ("1", "One Side of Relationship (1)", CLR_BLACK),
        ("N", "Many Side of Relationship (N)", CLR_BLACK),
        ("▢", "Table Entity Structure with Typed Attributes", CLR_INV_MAIN),
        ("—", "One-to-Many Relationship Line (1:N)", CLR_ORDER_MAIN),
        ("==", "One-to-One Unique Relationship (1:1)", CLR_PAY_MAIN)
    ]
    for idx, (sym, desc, clr) in enumerate(legends):
        ly = 1560 + idx * 105
        draw.rounded_rectangle([1235, ly, 1315, ly + 65], radius=10, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
        draw.text((1255, ly + 18), sym, font=FONT_CONTENT_BOLD, fill=clr)
        draw.text((1340, ly + 20), desc, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    # Box 3: Key Notes
    draw.rounded_rectangle([1910, 1460, 3160, 2350], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1935, 1480), "Key Notes", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(1910, 1525), (3160, 1525)], fill=CLR_BORDER, width=2)

    notes = [
        "The system uses 5 independent Microsoft SQL Server databases, one dedicated database per microservice.",
        "User to Order is a 1:M relationship where Order.DoctorID logically references Users.UserId in AuthDB.",
        "Order to OrderItem is a strict 1:M relationship with ON DELETE CASCADE in OrderDB.",
        "Supplier to Inventory (1:M) and Drug to Inventory (1:M) maintain full referential integrity in InventoryDB.",
        "Order to Payment is a strict 1:1 relationship enforced via a UNIQUE INDEX on Payments.OrderId.",
        "SaleReport is a standalone reporting entity aggregating financial metrics from Order & Inventory services.",
        "All monetary values (prices, totals, revenue, profit) utilize DECIMAL(18,2) to eliminate rounding errors.",
        "Cross-service data consistency is orchestrated via typed HttpClient calls rather than cross-database joins."
    ]
    for idx, note in enumerate(notes):
        ny = 1555 + idx * 95
        draw.ellipse([1935, ny + 10, 1955, ny + 30], fill=CLR_ORDER_MAIN)
        words = note.split(" ")
        l1, l2 = [], []
        for w in words:
            if len(" ".join(l1 + [w])) < 76:
                l1.append(w)
            else:
                l2.append(w)
        draw.text((1975, ny + 4), " ".join(l1), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        if l2:
            draw.text((1975, ny + 36), " ".join(l2), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    save_both(img, "06_Database_Schema_Diagram.jpg")

# ==============================================================================
# 3. USE CASE DIAGRAM (High Resolution 3200x2450, All-Bold Ovals & Actors)
# ==============================================================================
def generate_ref_usecase_diagram():
    W, H = 3200, 2450
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "5.0 Use Case Diagram", "Pharmacy Management System – Use Case Diagram")

    def draw_actor_ref(x, y, name, color, role_badge):
        draw.ellipse([x - 35, y, x + 35, y + 70], fill=CLR_WHITE, outline=color, width=4)
        draw.line([(x, y + 70), (x, y + 160)], fill=color, width=4)
        draw.line([(x - 55, y + 100), (x + 55, y + 100)], fill=color, width=4)
        draw.line([(x, y + 160), (x - 45, y + 240)], fill=color, width=4)
        draw.line([(x, y + 160), (x + 45, y + 240)], fill=color, width=4)

        bbox = FONT_SERVICE_TITLE.getbbox(name)
        bw = bbox[2] - bbox[0] + 44
        draw.rounded_rectangle([x - bw//2, y + 250, x + bw//2, y + 305], radius=10, fill=CLR_WHITE, outline=color, width=3)
        draw.text((x - bw//2 + 22, y + 260), name, font=FONT_SERVICE_TITLE, fill=color)
        draw_badge(draw, x - 72, y + 318, role_badge, color, CLR_WHITE, FONT_CONTENT_BOLD)

    draw_actor_ref(150, 420, "Admin", CLR_AUTH_MAIN, "ROLE: ADMIN")
    draw_actor_ref(3040, 420, "Doctor", CLR_ORDER_MAIN, "ROLE: DOCTOR")

    # System Boundary Box
    draw.rounded_rectangle([320, 175, 2870, 2400], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((1280, 195), "Pharmacy Management System Boundary", font=FONT_SECTION_TITLE, fill=CLR_BLACK)

    def draw_usecase_oval(x, y, w, h, title, sub=None, theme_clr=CLR_BLACK, bg_clr=CLR_WHITE):
        draw.ellipse([x, y, x + w, y + h], fill=bg_clr, outline=theme_clr, width=3)
        if sub:
            draw.text((x + w//2 - FONT_NODE_TITLE.getbbox(title)[2]//2, y + h//2 - 20), title, font=FONT_NODE_TITLE, fill=CLR_BLACK)
            draw.text((x + w//2 - FONT_ATTR_BOLD.getbbox(sub)[2]//2, y + h//2 + 10), sub, font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)
        else:
            draw.text((x + w//2 - FONT_NODE_TITLE.getbbox(title)[2]//2, y + h//2 - 12), title, font=FONT_NODE_TITLE, fill=CLR_BLACK)
        return x, y, w, h

    draw_usecase_oval(1280, 250, 640, 100, "Login / Authenticate", "(JWT Token & Role Verification)", CLR_AUTH_MAIN, CLR_AUTH_BG)

    draw.line([(1600, 350), (1600, 430)], fill=CLR_BORDER, width=3)
    draw.text((1620, 375), "<<include>>", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

    admin_cases = [
        ("Manage Users & Roles", "View all accounts in AuthDB", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Manage Drugs", "Add / Update / Delete in InventoryDB", CLR_INV_MAIN, CLR_INV_BG),
        ("Manage Suppliers", "Add / Update / Delete wholesale vendors", CLR_INV_MAIN, CLR_INV_BG),
        ("Add Stock to Inventory", "Associate Supplier, Drug & PurchasePrice", CLR_INV_MAIN, CLR_INV_BG),
        ("View All Doctor Orders", "Inspect orders placed by all doctors", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Validate Doctor Orders", "Check order items, totals, and doctor", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Verify Orders", "Update order status: Pending -> Verified", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Add to PickedUp Section", "Medication handed over: Status -> PickedUp", CLR_PAY_MAIN, CLR_PAY_BG),
        ("View PickedUp Orders", "Query all fulfilled customer orders", CLR_PAY_MAIN, CLR_PAY_BG),
        ("Generate Sales Report", "Daily / Weekly / Monthly / Yearly Analytics", CLR_REP_MAIN, CLR_REP_BG),
        ("Download Sales Report (CSV)", "Export financial data as spreadsheet", CLR_REP_MAIN, CLR_REP_BG),
        ("Print Sales Report", "Official printable formatted summary view", CLR_REP_MAIN, CLR_REP_BG)
    ]

    for idx, (c_title, c_sub, clr, bg) in enumerate(admin_cases):
        oy = 410 + idx * 160
        draw_usecase_oval(400, oy, 620, 92, c_title, c_sub, clr, bg)

    draw.line([(370, 456), (370, 2220)], fill=CLR_AUTH_MAIN, width=3)
    draw.line([(220, 500), (370, 500)], fill=CLR_AUTH_MAIN, width=3)
    for idx in range(len(admin_cases)):
        oy = 410 + idx * 160 + 46
        draw.line([(370, oy), (400, oy)], fill=CLR_AUTH_MAIN, width=3)

    # Center Column Flows
    draw_usecase_oval(1280, 480, 640, 100, "Browse Available Drugs", "(Filter Available Stock & Prices)", CLR_INV_MAIN, CLR_INV_BG)
    draw_usecase_oval(1280, 660, 640, 100, "Buy Drugs (Create Order)", "(Cart / Pending Order Placement)", CLR_ORDER_MAIN, CLR_ORDER_BG)
    
    draw.line([(1600, 760), (1600, 850)], fill=CLR_BORDER, width=3)
    draw.text((1620, 790), "<<include>>", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

    draw_usecase_oval(1280, 850, 640, 105, "Manage Order Lifecycle", "(Cart -> Pending -> Verified -> PickedUp)", CLR_ORDER_MAIN, CLR_ORDER_BG)

    draw.line([(1280, 902), (1140, 902), (1140, 1082), (1280, 1082)], fill=CLR_BORDER, width=3)
    draw.text((1025, 980), "<<include>>", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)
    draw_usecase_oval(1280, 1030, 640, 100, "Deduct Drug Stock", "(Atomic Quantity Decrement)", CLR_INV_MAIN, CLR_INV_BG)

    draw.line([(1600, 1130), (1600, 1220)], fill=CLR_BORDER, width=3)
    draw.text((1620, 1160), "<<include>>", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)
    draw_usecase_oval(1280, 1220, 640, 100, "Process Payment", "(1:1 Order Payment: Card/UPI/Cash)", CLR_PAY_MAIN, CLR_PAY_BG)

    draw.line([(1600, 1320), (1600, 1410)], fill=CLR_BORDER, width=3)
    draw.text((1620, 1350), "<<include>>", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)
    draw_usecase_oval(1280, 1410, 640, 100, "Generate Order Invoice", "(Itemized Total Amount & Tax)", CLR_PAY_MAIN, CLR_PAY_BG)

    draw.line([(1920, 902), (2060, 902), (2060, 1070), (1920, 1070)], fill=CLR_BORDER, width=3)
    draw.text((2075, 975), "<<extend>>", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)
    draw_usecase_oval(1780, 1060, 560, 95, "Cancel / Restock Order", "(Reject Out of Stock)", CLR_REP_MAIN, CLR_REP_BG)

    # Right Column: Doctor User Cases
    doctor_cases = [
        ("Doctor Signup / Login", "Basic details: Name, Phone, Email, Password", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("View Drug Catalog", "Check details of each available medication", CLR_INV_MAIN, CLR_INV_BG),
        ("Check Drug Expiry & Qty", "Verify stock availability before buying", CLR_INV_MAIN, CLR_INV_BG),
        ("Place Medication Order", "Buy single or multiple prescription drugs", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("View Own Orders", "History of orders placed by this doctor", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Track Order Status", "Monitor Cart, Pending, Verified, PickedUp", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Submit Online Payment", "Complete payment for verified order items", CLR_PAY_MAIN, CLR_PAY_BG)
    ]

    for idx, (c_title, c_sub, clr, bg) in enumerate(doctor_cases):
        oy = 480 + idx * 260
        draw_usecase_oval(2160, oy, 660, 98, c_title, c_sub, clr, bg)

    draw.line([(2840, 529), (2840, 2089)], fill=CLR_ORDER_MAIN, width=3)
    draw.line([(2980, 500), (2840, 500)], fill=CLR_ORDER_MAIN, width=3)
    for idx in range(len(doctor_cases)):
        oy = 480 + idx * 260 + 49
        draw.line([(2820, oy), (2840, oy)], fill=CLR_ORDER_MAIN, width=3)

    draw.line([(2980, 500), (1920, 300)], fill=CLR_BORDER, width=2)
    draw.line([(220, 500), (1280, 300)], fill=CLR_BORDER, width=2)

    save_both(img, "02_Use_Case_Diagram.jpg")

# ==============================================================================
# 4. FLOW DIAGRAM (High Resolution 3200x2550, All-Bold Nodes & Decisions)
# ==============================================================================
def generate_ref_flow_diagram():
    W, H = 3200, 2550
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "6.0 Flow Diagram", "PHARMACY MANAGEMENT SYSTEM – FLOW DIAGRAM")

    def draw_flow_node(x, y, w, h, t1, t2=None, theme_clr=CLR_BLACK, bg_clr=CLR_WHITE):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=bg_clr, outline=theme_clr, width=3)
        if t2:
            draw.text((x + w//2 - FONT_NODE_TITLE.getbbox(t1)[2]//2, y + h//2 - 20), t1, font=FONT_NODE_TITLE, fill=CLR_BLACK)
            draw.text((x + w//2 - FONT_ATTR_BOLD.getbbox(t2)[2]//2, y + h//2 + 10), t2, font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)
        else:
            draw.text((x + w//2 - FONT_NODE_TITLE.getbbox(t1)[2]//2, y + h//2 - 12), t1, font=FONT_NODE_TITLE, fill=CLR_BLACK)

    def draw_decision_diamond(x, y, w, h, text, theme_clr=CLR_BLACK, bg_clr=CLR_WHITE):
        pts = [(x + w//2, y), (x + w, y + h//2), (x + w//2, y + h), (x, y + h//2)]
        draw.polygon(pts, fill=bg_clr, outline=theme_clr)
        draw.text((x + w//2 - FONT_SERVICE_TITLE.getbbox(text)[2]//2, y + h//2 - 14), text, font=FONT_SERVICE_TITLE, fill=CLR_BLACK)

    # 1. START Pill
    draw.rounded_rectangle([1380, 160, 1820, 240], radius=40, fill=CLR_WHITE, outline=CLR_BLACK, width=3)
    draw.text((1535, 182), "START", font=FONT_TOP_SECTION, fill=CLR_BLACK)

    draw_arrow_ref(draw, (1600, 240), (1600, 290), CLR_BLACK, 3)

    # 2. Registration / Login Node
    draw_flow_node(1100, 290, 1000, 88, "Customer Registration / Customer or Admin Login", "(Doctor / Admin Account Verification)", CLR_AUTH_MAIN, CLR_AUTH_BG)

    draw_arrow_ref(draw, (1600, 378), (1600, 430), CLR_BLACK, 3)

    # 3. Decision: Role?
    draw_decision_diamond(1420, 430, 360, 110, "Role?", CLR_AUTH_MAIN, CLR_AUTH_BG)

    draw.text((680, 440), "Admin / Owner", font=FONT_SECTION_TITLE, fill=CLR_AUTH_MAIN)
    draw.text((2260, 440), "Doctor User / Customer", font=FONT_SECTION_TITLE, fill=CLR_ORDER_MAIN)

    draw.line([(1420, 485), (480, 485)], fill=CLR_BLACK, width=3)
    draw_arrow_ref(draw, (480, 485), (480, 550), CLR_BLACK, 3)

    draw.line([(1780, 485), (2720, 485)], fill=CLR_BLACK, width=3)
    draw_arrow_ref(draw, (2720, 485), (2720, 550), CLR_BLACK, 3)

    draw_arrow_ref(draw, (1600, 540), (1600, 600), CLR_BLACK, 3)
    draw.text((1620, 558), "Receptionist / Clinic Counter", font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

    # Left Branch: Admin Workflow
    admin_steps = [
        ("Manage Users & Roles", "(AuthDB Accounts & Statuses)", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Manage Drugs & Pricing", "(Add / Edit / Delete in Drugs Table)", CLR_INV_MAIN, CLR_INV_BG),
        ("Manage Suppliers & Inventory", "(Stock Inward with Wholesale Price)", CLR_INV_MAIN, CLR_INV_BG),
        ("View Orders Placed by All Doctors", "(Inspect Order Items, Totals & DoctorID)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Validate Doctor Orders", "(Check If Order Has Valid Stock & Pricing)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Verify Orders", "(Update Status = Verified)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Customer Counter: Handover Order", "(Add Order to PickedUp Section)", CLR_PAY_MAIN, CLR_PAY_BG),
        ("View & Generate Sales Reports", "(Daily / Weekly / Monthly / Yearly Analytics)", CLR_REP_MAIN, CLR_REP_BG),
        ("Download CSV & Print Sales Report", "(Official Formatted Receipt View)", CLR_REP_MAIN, CLR_REP_BG)
    ]

    for idx, (t1, t2, clr, bg) in enumerate(admin_steps):
        ay = 550 + idx * 170
        draw_flow_node(180, ay, 600, 88, t1, t2, clr, bg)
        if idx < len(admin_steps) - 1:
            draw_arrow_ref(draw, (480, ay + 88), (480, ay + 170), CLR_BLACK, 3)

    draw.line([(480, 550 + (len(admin_steps) - 1) * 170 + 88), (480, 2450), (1400, 2450)], fill=CLR_BLACK, width=3)

    # Right Branch: Doctor / Customer Workflow
    doctor_steps = [
        ("Search / View Available Drugs", "(Check Details & Selling Price)", CLR_INV_MAIN, CLR_INV_BG),
        ("View Drug Details & Expiry Dates", "(Select Single or Multiple Drugs)", CLR_INV_MAIN, CLR_INV_BG),
        ("Select Drugs & Quantities", "(Cart / Pending Order Items Staged)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Buy Drugs / Place Order", "(POST /api/orders with Items Array)", CLR_ORDER_MAIN, CLR_ORDER_BG)
    ]

    for idx, (t1, t2, clr, bg) in enumerate(doctor_steps):
        dy = 550 + idx * 170
        draw_flow_node(2420, dy, 600, 88, t1, t2, clr, bg)
        draw_arrow_ref(draw, (2720, dy + 88), (2720, dy + 170), CLR_BLACK, 3)

    draw.line([(2720, 550 + len(doctor_steps) * 170), (2720, 1060), (1980, 1060)], fill=CLR_BLACK, width=3)
    draw_arrow_ref(draw, (2030, 1060), (1980, 1060), CLR_BLACK, 3)

    # Center Branch: Receptionist / Transaction Pipeline
    draw_flow_node(1250, 600, 700, 88, "Check Stock Availability", "(Verify: Quantity >= req & Expiry > now)", CLR_INV_MAIN, CLR_INV_BG)
    draw_arrow_ref(draw, (1600, 688), (1600, 750), CLR_BLACK, 3)

    draw_flow_node(1250, 750, 700, 88, "Create Order Record", "(DoctorID, OrderDate, Items, Status: Pending)", CLR_ORDER_MAIN, CLR_ORDER_BG)
    draw_arrow_ref(draw, (1600, 838), (1600, 900), CLR_BLACK, 3)

    draw_flow_node(1250, 900, 700, 88, "Deduct Stock Atomically", "(InventoryService: Decrement Quantities)", CLR_INV_MAIN, CLR_INV_BG)
    draw_arrow_ref(draw, (1600, 988), (1600, 1050), CLR_BLACK, 3)

    draw_flow_node(1250, 1050, 700, 88, "Calculate Total Amount", "(Sum of Quantity * UnitPrice + Taxes)", CLR_ORDER_MAIN, CLR_ORDER_BG)
    draw_arrow_ref(draw, (1600, 1138), (1600, 1200), CLR_BLACK, 3)

    draw_flow_node(1250, 1200, 700, 88, "Process Payment", "(Online / CreditCard / UPI / Cash / NetBanking)", CLR_PAY_MAIN, CLR_PAY_BG)
    draw_arrow_ref(draw, (1600, 1288), (1600, 1350), CLR_BLACK, 3)

    # Diamond: Payment Successful?
    draw_decision_diamond(1380, 1350, 440, 110, "Payment Successful?", CLR_PAY_MAIN, CLR_PAY_BG)

    draw.line([(1380, 1405), (1050, 1405)], fill=CLR_REP_MAIN, width=3)
    draw_arrow_ref(draw, (1080, 1405), (1050, 1405), CLR_REP_MAIN, 3)
    draw.text((1180, 1370), "No", font=FONT_SECTION_TITLE, fill=CLR_REP_MAIN)

    # Dashed container for Payment Failed
    draw.rounded_rectangle([780, 1470, 1320, 2180], radius=18, outline=CLR_REP_MAIN, width=3)
    draw_badge(draw, 820, 1490, "PAYMENT FAILED CONTAINER", CLR_REP_MAIN, CLR_WHITE, FONT_CONTENT_BOLD)

    draw_flow_node(810, 1560, 480, 85, "Show Failure Message", "(e.g., Timeout / Bank Declined)", CLR_REP_MAIN, CLR_REP_BG)
    draw_arrow_ref(draw, (1050, 1645), (1050, 1710), CLR_BLACK, 3)

    draw_flow_node(810, 1710, 480, 85, "Update Order Status", "(Status = PaymentFailed / Pending)", CLR_REP_MAIN, CLR_REP_BG)
    draw_arrow_ref(draw, (1050, 1795), (1050, 1860), CLR_BLACK, 3)

    draw_decision_diamond(860, 1860, 380, 100, "Retry Payment?", CLR_AUTH_MAIN, CLR_AUTH_BG)

    draw.line([(860, 1910), (740, 1910), (740, 1245), (1250, 1245)], fill=CLR_AUTH_MAIN, width=3)
    draw_arrow_ref(draw, (1190, 1245), (1250, 1245), CLR_AUTH_MAIN, 3)
    draw.text((760, 1875), "Yes", font=FONT_SECTION_TITLE, fill=CLR_AUTH_MAIN)

    draw.line([(1050, 1960), (1050, 2030)], fill=CLR_BLACK, width=3)
    draw_arrow_ref(draw, (1050, 1960), (1050, 2030), CLR_BLACK, 3)
    draw.text((1065, 1980), "No", font=FONT_SECTION_TITLE, fill=CLR_REP_MAIN)

    draw_flow_node(810, 2030, 480, 85, "Cancel Order & Restock", "(Release Reserved Drug Quantities)", CLR_REP_MAIN, CLR_REP_BG)
    draw.line([(1050, 2115), (1050, 2450), (1400, 2450)], fill=CLR_BLACK, width=3)

    # If Payment Successful -> Yes
    draw.line([(1820, 1405), (2050, 1405)], fill=CLR_INV_MAIN, width=3)
    draw.line([(2050, 1405), (2050, 1510)], fill=CLR_INV_MAIN, width=3)
    draw_arrow_ref(draw, (2050, 1460), (2050, 1510), CLR_INV_MAIN, 3)
    draw.text((1900, 1370), "Yes", font=FONT_SECTION_TITLE, fill=CLR_INV_MAIN)

    draw_flow_node(1700, 1510, 700, 88, "Confirm Order (Status = Verified)", "(1:1 Payment Record Saved in PaymentDB)", CLR_INV_MAIN, CLR_INV_BG)
    draw_arrow_ref(draw, (2050, 1598), (2050, 1660), CLR_BLACK, 3)

    draw_flow_node(1700, 1660, 700, 88, "Generate Order Invoice", "(Itemized Total Amount, Drug Names, Qty)", CLR_ORDER_MAIN, CLR_ORDER_BG)
    draw_arrow_ref(draw, (2050, 1748), (2050, 1810), CLR_BLACK, 3)

    draw_flow_node(1700, 1810, 700, 88, "Send Order Confirmation Alert", "(Prescription Ready for Pharmacy Pickup)", CLR_PAY_MAIN, CLR_PAY_BG)
    draw_arrow_ref(draw, (2050, 1898), (2050, 1960), CLR_BLACK, 3)

    draw_flow_node(1700, 1960, 700, 88, "Customer Pickup at Pharmacy", "(Medication Handover: Status -> PickedUp)", CLR_REP_MAIN, CLR_REP_BG)
    
    draw.line([(2050, 2048), (2050, 2450), (1800, 2450)], fill=CLR_BLACK, width=3)

    # 4. END Pill
    draw.rounded_rectangle([1380, 2410, 1820, 2490], radius=40, fill=CLR_WHITE, outline=CLR_BLACK, width=3)
    draw.text((1560, 2432), "END", font=FONT_TOP_SECTION, fill=CLR_BLACK)

    save_both(img, "04_Flow_Diagram.jpg")

# ==============================================================================
# 5. SEQUENCE DIAGRAM (High Resolution 3200x2550, All-Bold Lifelines & Messages)
# ==============================================================================
def generate_ref_sequence_diagram():
    W, H = 3200, 2550
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "3.0 Sequence Diagram", "Pharmacy Management System – Sequence Diagram (End-to-End Microservice Flows)")

    lifelines = [
        ("Doctor User", "(Clinic Portal)", 200, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Admin User", "(Operations)", 580, CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("API Gateway", "(YARP / Proxy)", 1020, CLR_GATE_MAIN, CLR_GATE_BG),
        ("Auth Service", "(Port 5001)", 1460, CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Inventory Service", "(Port 5002)", 1900, CLR_INV_MAIN, CLR_INV_BG),
        ("Order Service", "(Port 5003)", 2340, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Payment Service", "(Port 5004)", 2780, CLR_PAY_MAIN, CLR_PAY_BG)
    ]

    for title, sub, lx, clr, bg in lifelines:
        draw.rounded_rectangle([lx - 150, 175, lx + 150, 260], radius=12, fill=bg, outline=clr, width=3)
        draw.text((lx - 130, 188), title, font=FONT_SERVICE_TITLE, fill=CLR_BLACK)
        draw.text((lx - 130, 222), sub, font=FONT_ATTR_BOLD, fill=clr)
        for ly in range(260, 1960, 16):
            draw.line([(lx, ly), (lx, min(ly + 8, 1960))], fill=CLR_BORDER, width=2)

    seq_steps = [
        (300, 200, 1020, "1", "POST /api/auth/login {email, password}", False, CLR_BLACK),
        (360, 1020, 1460, "2", "Forward Login Request -> AuthDbContext", False, CLR_AUTH_MAIN),
        (420, 1460, 1020, "3", "200 OK: Validated (Generate JWT Bearer Token: Role=Doctor)", True, CLR_AUTH_MAIN),
        (480, 1020, 200, "4", "Return JWT Token to Doctor Client", True, CLR_BLACK),

        (550, 200, 1020, "5", "GET /api/drugs?availableOnly=true (Bearer Token)", False, CLR_BLACK),
        (610, 1020, 1900, "6", "Query Available Drugs & Prices (InventoryDB)", False, CLR_INV_MAIN),
        (670, 1900, 200, "7", "200 OK: Available Drugs List (Paracetamol, Amoxicillin, etc.)", True, CLR_INV_MAIN),

        (745, 200, 1020, "8", "POST /api/orders (Buy Drugs: DrugId, Quantity, UnitPrice)", False, CLR_ORDER_MAIN),
        (805, 1020, 2340, "9", "Create Order Record in OrderDB (Status: Pending)", False, CLR_ORDER_MAIN),
        (865, 2340, 1900, "10", "POST /api/drugs/deduct-stock (Atomic Stock Deduction)", False, CLR_INV_MAIN),
        (925, 1900, 2340, "11", "200 OK: Stock Deducted & IsAvailable Updated if Qty=0", True, CLR_INV_MAIN),
        (985, 2340, 200, "12", "201 Created: Order Confirmation (OrderId: #101, Total: $48.50)", True, CLR_ORDER_MAIN),

        (1060, 200, 1020, "13", "POST /api/payments {OrderId: 101, Amount: $48.50, Method: Card}", False, CLR_PAY_MAIN),
        (1120, 1020, 2780, "14", "Process 1:1 Payment (PaymentDB: Status=Completed)", False, CLR_PAY_MAIN),
        (1180, 2780, 200, "15", "200 OK: Payment Successful (TxnRef: TXN-A83F91B2C4D5)", True, CLR_PAY_MAIN),

        (1255, 580, 1020, "16", "GET /api/orders (Admin views orders placed by all doctors)", False, CLR_BLACK),
        (1315, 1020, 2340, "17", "Fetch Orders across all Clinics (Include OrderItems)", False, CLR_ORDER_MAIN),
        (1375, 2340, 580, "18", "200 OK: Orders List with Items and Status", True, CLR_ORDER_MAIN),

        (1445, 580, 2340, "19", "PUT /api/orders/101/verify (Admin verifies valid order)", False, CLR_ORDER_MAIN),
        (1505, 2340, 580, "20", "200 OK: Order Status updated to 'Verified'", True, CLR_ORDER_MAIN),

        (1575, 580, 2340, "21", "PUT /api/orders/101/pickup (Customer collection handover)", False, CLR_AUTH_MAIN),
        (1635, 2340, 580, "22", "200 OK: Order moved to 'PickedUp' section", True, CLR_AUTH_MAIN),

        (1710, 580, 1020, "23", "POST /api/salereports/generate (Daily / Weekly / Monthly)", False, CLR_REP_MAIN),
        (1770, 1020, 580, "24", "201 Created: Financial Report (Total Orders, Revenue & Profit)", True, CLR_REP_MAIN)
    ]

    for y, fx, tx, num, text, is_ret, clr in seq_steps:
        if is_ret:
            for seg in range(min(fx, tx), max(fx, tx), 16):
                draw.line([(seg, y), (min(seg + 8, max(fx, tx)), y)], fill=clr, width=3)
            draw_arrow_ref(draw, (fx + (10 if tx > fx else -10), y), (tx, y), clr, 3)
        else:
            draw_arrow_ref(draw, (fx, y), (tx, y), clr, 3)

        mid_x = (fx + tx) // 2
        bbox = FONT_CONTENT_BOLD.getbbox(text)
        bw = bbox[2] - bbox[0] + 66
        draw.rounded_rectangle([mid_x - bw//2, y - 24, mid_x + bw//2, y + 18], radius=8, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=2)
        
        draw.ellipse([mid_x - bw//2 + 8, y - 20, mid_x - bw//2 + 38, y + 10], fill=clr)
        draw.text((mid_x - bw//2 + 15, y - 18), num, font=FONT_BADGE_BOLD, fill=CLR_WHITE)
        draw.text((mid_x - bw//2 + 48, y - 16), text, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    # Bottom Summary Box
    draw.rounded_rectangle([40, 1980, 3160, 2480], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((65, 2000), "Sequence Workflow Summary", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(40, 2045), (3160, 2045)], fill=CLR_BORDER, width=2)

    seq_notes = [
        ("Authentication & RBAC", "Doctor authenticates via AuthService, obtaining an asymmetric JWT Bearer token encoding user ID and Doctor role claims.", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Order & Stock Coordination", "Order Service coordinates with Inventory Service via HTTP REST to decrement stock atomically before setting status to Pending.", CLR_INV_MAIN, CLR_INV_BG),
        ("Payment & Handover", "Payment Service records payment 1:1 against the Order; Admin inspects and verifies order, moving status to 'PickedUp'.", CLR_PAY_MAIN, CLR_PAY_BG)
    ]
    for idx, (stitle, sdesc, clr, bg) in enumerate(seq_notes):
        sx = 65 + idx * 1040
        draw.rounded_rectangle([sx, 2065, sx + 1010, 2450], radius=14, fill=bg, outline=clr, width=2)
        draw.text((sx + 25, 2090), stitle, font=FONT_SERVICE_TITLE, fill=clr)
        
        words = sdesc.split(" ")
        l1, l2, l3 = [], [], []
        for w in words:
            if len(" ".join(l1 + [w])) < 46:
                l1.append(w)
            elif len(" ".join(l2 + [w])) < 46:
                l2.append(w)
            else:
                l3.append(w)
        draw.text((sx + 25, 2140), " ".join(l1), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        if l2:
            draw.text((sx + 25, 2185), " ".join(l2), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        if l3:
            draw.text((sx + 25, 2230), " ".join(l3), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    save_both(img, "03_Sequence_Diagram.jpg")

# ==============================================================================
# 6. ENTITY-RELATIONSHIP (ER) DIAGRAM (High Resolution 3200x2450, All-Bold Entities)
# ==============================================================================
def generate_ref_er_diagram():
    W, H = 3200, 2450
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "1.0 ER Diagram", "Pharmacy Management System – Entity-Relationship (ER) Diagram")

    def draw_er_card(x, y, w, title, attrs, theme_clr, bg_clr):
        row_h = 48
        h = 60 + len(attrs) * row_h + 10
        draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CLR_WHITE, outline=theme_clr, width=3)
        draw.rounded_rectangle([x, y, x + w, y + 54], radius=12, fill=bg_clr, outline=theme_clr, width=1)
        draw.rectangle([x, y + 40, x + w, y + 54], fill=bg_clr)
        draw.text((x + 20, y + 12), title, font=FONT_TABLE_NAME, fill=theme_clr)

        for idx, (ktype, cname, dtype) in enumerate(attrs):
            ry = y + 58 + idx * row_h
            draw.line([(x, ry), (x + w, ry)], fill=CLR_BORDER_LIGHT, width=1)
            draw.line([(x + 65, ry), (x + 65, ry + row_h)], fill=CLR_BORDER_LIGHT, width=1)

            if ktype == "PK":
                draw.text((x + 12, ry + 10), "PK", font=FONT_ATTR_BOLD, fill=CLR_AUTH_MAIN)
            elif ktype == "FK":
                draw.text((x + 12, ry + 10), "FK", font=FONT_ATTR_BOLD, fill=CLR_ORDER_MAIN)

            draw.text((x + 80, ry + 10), cname, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
            draw.text((x + w - 240, ry + 10), dtype, font=FONT_CONTENT_BOLD, fill=CLR_DARK_SLATE)

        return x, y, w, h

    # 1. USER entity
    user_attrs = [
        ("PK", "UserId", "int"),
        ("", "Name", "nvarchar(100)"),
        ("", "Email", "nvarchar(150) [UQ]"),
        ("", "PhoneNumber", "nvarchar(20)"),
        ("", "PasswordHash", "nvarchar(255)"),
        ("", "Role", "nvarchar(20)"),
        ("", "IsActive", "bit"),
        ("", "CreatedDate", "datetime2")
    ]
    u_x, u_y, u_w, u_h = draw_er_card(70, 185, 620, "User (AuthDB)", user_attrs, CLR_AUTH_MAIN, CLR_AUTH_BG)

    # 2. DRUG entity
    drug_attrs = [
        ("PK", "DrugId", "int"),
        ("", "Name", "nvarchar(150)"),
        ("", "Description", "nvarchar(500)"),
        ("", "Price", "decimal(18,2)"),
        ("", "ExpiryDate", "datetime2"),
        ("", "Quantity", "int"),
        ("", "IsAvailable", "bit")
    ]
    d_x, d_y, d_w, d_h = draw_er_card(900, 185, 640, "Drug (InventoryDB)", drug_attrs, CLR_INV_MAIN, CLR_INV_BG)

    # 3. SUPPLIER entity
    supp_attrs = [
        ("PK", "SupplierId", "int"),
        ("", "SupplierName", "nvarchar(150)"),
        ("", "Email", "nvarchar(150)"),
        ("", "PhoneNumber", "nvarchar(20)"),
        ("", "Address", "nvarchar(300)")
    ]
    s_x, s_y, s_w, s_h = draw_er_card(1750, 185, 640, "Supplier (InventoryDB)", supp_attrs, CLR_INV_MAIN, CLR_INV_BG)

    # 4. INVENTORY entity
    inv_attrs = [
        ("PK", "InventoryId", "int"),
        ("FK", "SupplierId", "int [FK Supplier]"),
        ("FK", "DrugId", "int [FK Drug]"),
        ("", "PurchasePrice", "decimal(18,2)"),
        ("", "QuantityAdded", "int"),
        ("", "StockReceivedDate", "datetime2")
    ]
    i_x, i_y, i_w, i_h = draw_er_card(1330, 680, 680, "Inventory (InventoryDB)", inv_attrs, CLR_INV_MAIN, CLR_INV_BG)

    # 5. ORDER entity
    order_attrs = [
        ("PK", "OrderId", "int"),
        ("FK", "DoctorID", "int [Logical FK User]"),
        ("", "OrderDate", "datetime2"),
        ("", "TotalAmount", "decimal(18,2)"),
        ("", "Status", "nvarchar(20)")
    ]
    o_x, o_y, o_w, o_h = draw_er_card(70, 780, 620, "Order (OrderDB)", order_attrs, CLR_ORDER_MAIN, CLR_ORDER_BG)

    # 6. ORDER ITEM entity
    item_attrs = [
        ("PK", "OrderItemId", "int"),
        ("FK", "OrderId", "int [FK Order]"),
        ("FK", "DrugId", "int [Logical FK Drug]"),
        ("", "DrugName", "nvarchar(150)"),
        ("", "Quantity", "int"),
        ("", "UnitPrice", "decimal(18,2)")
    ]
    oi_x, oi_y, oi_w, oi_h = draw_er_card(70, 1180, 620, "OrderItem (OrderDB)", item_attrs, CLR_ORDER_MAIN, CLR_ORDER_BG)

    # 7. PAYMENT entity
    pay_attrs = [
        ("PK", "PaymentId", "int"),
        ("FK", "OrderId", "int [Unique - 1:1]"),
        ("", "Amount", "decimal(18,2)"),
        ("", "PaymentDate", "datetime2"),
        ("", "PaymentMethod", "nvarchar(50)"),
        ("", "PaymentStatus", "nvarchar(20)"),
        ("", "TransactionReference", "nvarchar(100)")
    ]
    p_x, p_y, p_w, p_h = draw_er_card(780, 780, 650, "Payment (PaymentDB)", pay_attrs, CLR_PAY_MAIN, CLR_PAY_BG)

    # 8. SALE REPORT entity
    rep_attrs = [
        ("PK", "SaleReportId", "int"),
        ("", "ReportType", "nvarchar(20)"),
        ("", "FromDate", "datetime2"),
        ("", "ToDate", "datetime2"),
        ("", "TotalOrders", "int"),
        ("", "TotalRevenue", "decimal(18,2)"),
        ("", "GeneratedDate", "datetime2"),
        ("", "Profit", "decimal(18,2)")
    ]
    r_x, r_y, r_w, r_h = draw_er_card(2480, 480, 640, "SaleReport (SaleReportDB)", rep_attrs, CLR_REP_MAIN, CLR_REP_BG)

    # RELATIONSHIP CONNECTORS & CARDINALITIES
    draw.line([(380, u_y + u_h), (380, o_y)], fill=CLR_AUTH_MAIN, width=4)
    draw.text((395, u_y + u_h + 10), "1", font=FONT_SERVICE_TITLE, fill=CLR_AUTH_MAIN)
    draw.text((395, o_y - 35), "M", font=FONT_SERVICE_TITLE, fill=CLR_AUTH_MAIN)
    draw.text((420, (u_y + u_h + o_y)//2 - 14), "1 : M (User to Order)", font=FONT_NODE_TITLE, fill=CLR_AUTH_MAIN)

    draw.line([(380, o_y + o_h), (380, oi_y)], fill=CLR_ORDER_MAIN, width=4)
    draw.text((395, o_y + o_h + 10), "1", font=FONT_SERVICE_TITLE, fill=CLR_ORDER_MAIN)
    draw.text((395, oi_y - 35), "M", font=FONT_SERVICE_TITLE, fill=CLR_ORDER_MAIN)
    draw.text((420, (o_y + o_h + oi_y)//2 - 14), "1 : M (Order to OrderItem)", font=FONT_NODE_TITLE, fill=CLR_ORDER_MAIN)

    draw.line([(1050, d_y + d_h), (1050, 1260), (690, 1260)], fill=CLR_INV_MAIN, width=4)
    draw.text((1065, d_y + d_h + 10), "1", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((705, 1220), "M", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((880, 1275), "1 : M (Drug to OrderItem)", font=FONT_NODE_TITLE, fill=CLR_INV_MAIN)

    draw.line([(1960, s_y + s_h), (1800, i_y)], fill=CLR_INV_MAIN, width=4)
    draw.text((1975, s_y + s_h + 10), "1", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((1815, i_y - 35), "M", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((1900, (s_y + s_h + i_y)//2 - 14), "1 : M (Supplier to Inv)", font=FONT_NODE_TITLE, fill=CLR_INV_MAIN)

    draw.line([(1250, d_y + d_h), (1420, i_y)], fill=CLR_INV_MAIN, width=4)
    draw.text((1230, d_y + d_h + 10), "1", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((1400, i_y - 35), "M", font=FONT_SERVICE_TITLE, fill=CLR_INV_MAIN)
    draw.text((1200, (d_y + d_h + i_y)//2 - 14), "1 : M (Drug to Inv)", font=FONT_NODE_TITLE, fill=CLR_INV_MAIN)

    draw.line([(o_x + o_w, o_y + 120), (p_x, o_y + 120)], fill=CLR_PAY_MAIN, width=4)
    draw.text((o_x + o_w + 12, o_y + 80), "1", font=FONT_SERVICE_TITLE, fill=CLR_PAY_MAIN)
    draw.text((p_x - 30, o_y + 80), "1", font=FONT_SERVICE_TITLE, fill=CLR_PAY_MAIN)
    draw.text((o_x + o_w + 15, o_y + 135), "1 : 1 (Unique OrderId)", font=FONT_NODE_TITLE, fill=CLR_PAY_MAIN)

    draw.rounded_rectangle([2480, 960, 3140, 1220], radius=14, fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((2505, 980), "Standalone Aggregated Financials:", font=FONT_NODE_TITLE, fill=CLR_REP_MAIN)
    draw.text((2505, 1025), "• Standalone Entity: Zero direct FK locks.", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
    draw.text((2505, 1070), "• Aggregates verified orders & revenue via REST.", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
    draw.text((2505, 1115), "• Computes Profit = TotalRevenue - COGS Purchase Cost.", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
    draw.text((2505, 1160), "• Exports CSV spreadsheets & formatted print receipts.", font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    # Bottom Section: 3 Boxes
    draw.rounded_rectangle([40, 1660, 1180, 2400], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((65, 1680), "Entity-Relationship Mapping", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(40, 1725), (1180, 1725)], fill=CLR_BORDER, width=2)

    draw.rectangle([65, 1750, 1155, 1815], fill=CLR_GATE_MAIN)
    draw.text((90, 1770), "Relationship", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)
    draw.text((440, 1770), "Cardinality", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)
    draw.text((680, 1770), "Implementation Mechanism", font=FONT_CONTENT_BOLD, fill=CLR_WHITE)

    rel_rows = [
        ("User to Order", "1 : M", "Logical DoctorID FK across microservices", CLR_AUTH_BG, CLR_AUTH_MAIN),
        ("Order to OrderItem", "1 : M", "Physical OrderId FK with CASCADE DELETE", CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Drug to OrderItem", "1 : M", "Logical DrugId FK across microservices", CLR_INV_BG, CLR_INV_MAIN),
        ("Supplier to Inventory", "1 : M", "Physical SupplierId FK in InventoryDB", CLR_INV_BG, CLR_INV_MAIN),
        ("Drug to Inventory", "1 : M", "Physical DrugId FK in InventoryDB", CLR_INV_BG, CLR_INV_MAIN),
        ("Order to Payment", "1 : 1", "Enforced via UNIQUE Index on Payments.OrderId", CLR_PAY_BG, CLR_PAY_MAIN),
        ("SaleReport", "Standalone", "Asynchronous reporting aggregation via HTTP", CLR_REP_BG, CLR_REP_MAIN)
    ]
    for idx, (rtitle, rcard, rdesc, bg_c, thm_c) in enumerate(rel_rows):
        ry = 1825 + idx * 78
        draw.rectangle([65, ry, 1155, ry + 74], fill=bg_c if idx % 2 == 1 else CLR_WHITE)
        draw.line([(65, ry + 74), (1155, ry + 74)], fill=CLR_BORDER_LIGHT, width=1)
        draw.text((90, ry + 24), rtitle, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        draw.text((450, ry + 24), rcard, font=FONT_SERVICE_TITLE, fill=thm_c)
        draw.text((680, ry + 24), rdesc, font=FONT_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.rectangle([65, 1750, 1155, 2371], outline=CLR_BORDER, width=2)
    draw.line([(420, 1750), (420, 2371)], fill=CLR_BORDER, width=2)
    draw.line([(650, 1750), (650, 2371)], fill=CLR_BORDER, width=2)

    # Box 2: Legend
    draw.rounded_rectangle([1210, 1660, 1880, 2400], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1235, 1680), "Legend", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(1210, 1725), (1880, 1725)], fill=CLR_BORDER, width=2)

    legends = [
        ("PK", "Primary Key (Auto-Increment / Identity)", CLR_AUTH_MAIN),
        ("FK", "Foreign Key (Referential Constraint)", CLR_ORDER_MAIN),
        ("1 : M", "One-to-Many Relationship", CLR_INV_MAIN),
        ("1 : 1", "One-to-One Strict Relationship (Unique FK)", CLR_PAY_MAIN),
        ("UQ", "Unique Constraint Index", CLR_AUTH_MAIN),
        ("▢", "Relational Entity / Domain Table", CLR_DARK_SLATE),
        ("—", "Referential Link Line", CLR_BORDER)
    ]
    for idx, (sym, desc, clr) in enumerate(legends):
        ly = 1755 + idx * 85
        draw.rounded_rectangle([1235, ly, 1325, ly + 60], radius=10, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
        draw.text((1255, ly + 16), sym, font=FONT_CONTENT_BOLD, fill=clr)
        draw.text((1350, ly + 18), desc, font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    # Box 3: Key Notes
    draw.rounded_rectangle([1910, 1660, 3160, 2400], radius=18, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1935, 1680), "Key Architectural Notes", font=FONT_SECTION_TITLE, fill=CLR_BLACK)
    draw.line([(1910, 1725), (3160, 1725)], fill=CLR_BORDER, width=2)

    er_notes = [
        "User to Order (1:M): Doctor ID links orders to users in AuthDB, allowing doctors to view only their own orders.",
        "Order to OrderItem (1:M): Deleting an order cascades and cleans up child order item records.",
        "Drug to OrderItem (1:M): DrugId is stored alongside a cached DrugName snapshot for billing immutability.",
        "Supplier to Inventory (1:M) & Drug to Inventory (1:M): Tracks wholesale supplier stock inwarding history.",
        "Order to Payment (1:1): Payments table enforces a unique index on OrderId, preventing double billing.",
        "SaleReport Standalone: Aggregates verified orders and computes profit without locking active order transactions.",
        "Data Types: Financial amounts use DECIMAL(18,2) and dates use DATETIME2(7) UTC for precision.",
        "Decoupled Microservices: Cross-database referential integrity is guaranteed through HTTP API orchestrations."
    ]
    for idx, note in enumerate(er_notes):
        ny = 1750 + idx * 78
        draw.ellipse([1935, ny + 10, 1955, ny + 30], fill=CLR_ORDER_MAIN)
        words = note.split(" ")
        l1, l2 = [], []
        for w in words:
            if len(" ".join(l1 + [w])) < 76:
                l1.append(w)
            else:
                l2.append(w)
        draw.text((1975, ny + 4), " ".join(l1), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)
        if l2:
            draw.text((1975, ny + 36), " ".join(l2), font=FONT_CONTENT_BOLD, fill=CLR_BLACK)

    save_both(img, "05_ER_Diagram.jpg")

# ==============================================================================
# MAIN RUNNER
# ==============================================================================
if __name__ == "__main__":
    print("Generating all 6 diagrams with ENLARGED ALL-BOLD FONTS & professional colors...")
    generate_ref_architecture_diagram()
    generate_ref_database_diagram()
    generate_ref_usecase_diagram()
    generate_ref_flow_diagram()
    generate_ref_sequence_diagram()
    generate_ref_er_diagram()
    print("ALL 6 ENLARGED ALL-BOLD DIAGRAMS GENERATED SUCCESSFULLY!")
