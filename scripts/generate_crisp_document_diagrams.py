import os
import math
from PIL import Image, ImageDraw, ImageFont

# Output Directories
OUT_DIR_WORKSPACE = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"
OUT_DIR_ARTIFACT = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\diagrams"

os.makedirs(OUT_DIR_WORKSPACE, exist_ok=True)
os.makedirs(OUT_DIR_ARTIFACT, exist_ok=True)

# ==============================================================================
# CALIBRATED HIGH-LEGIBILITY TYPOGRAPHY FOR WORD (.DOCX) & PDF EMBEDDING
# Standard Document Width: 1350-1400px. At 6.2 inches in Word, scaling is ~2.1x.
# A 16-18pt bold font here displays at a crisp ~8-9pt equivalent in Word/PDF!
# ==============================================================================
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG  = "C:/Windows/Fonts/segoeui.ttf"

F_TITLE     = ImageFont.truetype(FONT_BOLD, 26) # Main pill title
F_TOP_TAG   = ImageFont.truetype(FONT_BOLD, 20) # Top section tag
F_SEC_TITLE = ImageFont.truetype(FONT_BOLD, 18) # Section & container headers
F_CARD_NAME = ImageFont.truetype(FONT_BOLD, 17) # Card / Table names
F_NODE_TXT  = ImageFont.truetype(FONT_BOLD, 15.5) # Node, oval, bullet text
F_BODY_BOLD = ImageFont.truetype(FONT_BOLD, 14.5) # Column names & main text
F_ATTR_BOLD = ImageFont.truetype(FONT_BOLD, 13.5) # Subtext, data types, bullets
F_BADGE_TXT = ImageFont.truetype(FONT_BOLD, 13) # Numbers & step badges
F_NOTE_TXT  = ImageFont.truetype(FONT_BOLD, 12.5) # Explanatory footnotes

# Vibrant Color Palette (Distinct per microservice + high contrast)
CLR_WHITE         = (255, 255, 255)
CLR_BLACK         = (12, 18, 28)
CLR_DARK_SLATE    = (35, 45, 60)
CLR_BORDER        = (45, 60, 80)
CLR_BORDER_LIGHT  = (175, 190, 205)

# Microservice Themes
CLR_AUTH_MAIN     = (195, 95, 0)      # Warm Amber / Orange (Auth)
CLR_AUTH_BG       = (255, 247, 230)
CLR_AUTH_BORDER   = (225, 125, 10)

CLR_INV_MAIN      = (0, 135, 80)      # Emerald Green (Inventory)
CLR_INV_BG        = (232, 252, 240)
CLR_INV_BORDER    = (15, 165, 100)

CLR_ORDER_MAIN    = (15, 75, 200)     # Royal Blue (Order)
CLR_ORDER_BG      = (236, 244, 255)
CLR_ORDER_BORDER  = (40, 115, 235)

CLR_PAY_MAIN      = (115, 35, 215)    # Purple / Violet (Payment)
CLR_PAY_BG        = (247, 240, 255)
CLR_PAY_BORDER    = (140, 70, 230)

CLR_REP_MAIN      = (205, 20, 60)     # Crimson / Ruby (SaleReport)
CLR_REP_BG        = (255, 238, 242)
CLR_REP_BORDER    = (230, 45, 80)

CLR_GATE_MAIN     = (15, 23, 42)      # Dark Navy (Gateway)
CLR_GATE_BG       = (240, 244, 248)

def draw_reference_frame(draw, W, H, section_tag, main_title):
    # Outer frame
    draw.rounded_rectangle([8, 8, W - 8, H - 8], radius=12, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    
    # Top section tag (left)
    tag_bbox = F_TOP_TAG.getbbox(section_tag)
    tag_w = tag_bbox[2] - tag_bbox[0] + 30
    draw.rounded_rectangle([18, 14, 18 + tag_w, 52], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((32, 20), section_tag, font=F_TOP_TAG, fill=CLR_BLACK)

    # Center Main Title Pill
    title_bbox = F_TITLE.getbbox(main_title)
    title_w = title_bbox[2] - title_bbox[0] + 44
    title_x = (W - title_w) // 2
    draw.rounded_rectangle([title_x, 48, title_x + title_w, 98], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((title_x + 22, 56), main_title, font=F_TITLE, fill=CLR_BLACK)

def draw_arrow(draw, start, end, color=CLR_BLACK, width=2, label=None, label_above=True):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    hlen = 10
    p1 = (x2 - hlen * math.cos(angle - math.pi / 6), y2 - hlen * math.sin(angle - math.pi / 6))
    p2 = (x2 - hlen * math.cos(angle + math.pi / 6), y2 - hlen * math.sin(angle + math.pi / 6))
    draw.polygon([(x2, y2), p1, p2], fill=color)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ly = my - 18 if label_above else my + 6
        bbox = F_BADGE_TXT.getbbox(label)
        lw = bbox[2] - bbox[0] + 12
        draw.rounded_rectangle([mx - lw//2, ly - 2, mx + lw//2, ly + 16], radius=4, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((mx - lw//2 + 6, ly), label, font=F_BADGE_TXT, fill=color)

def draw_cylinder(draw, x, y, w, h, db_name, tables_str, theme, bg):
    cap = 14
    draw.rectangle([x, y + cap//2, x + w, y + h - cap//2], fill=bg, outline=theme, width=2)
    draw.ellipse([x, y + h - cap, x + w, y + h], fill=bg, outline=theme, width=2)
    draw.arc([x, y + h//2 - cap//2, x + w, y + h//2 + cap//2], 0, 180, fill=theme, width=1)
    draw.ellipse([x, y, x + w, y + cap], fill=theme, outline=theme, width=2)
    
    draw.text((x + 10, y + 16), db_name, font=F_CARD_NAME, fill=theme)
    draw.text((x + 10, y + 38), tables_str, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

def save_image(img, name):
    p1 = os.path.join(OUT_DIR_WORKSPACE, name)
    p2 = os.path.join(OUT_DIR_ARTIFACT, name)
    img.save(p1, "JPEG", quality=96)
    img.save(p2, "JPEG", quality=96)
    print(f"Generated High-Legibility Diagram: {name} ({img.size[0]}x{img.size[1]})")

# ==============================================================================
# 1. ARCHITECTURE DIAGRAM (1400 x 980)
# ==============================================================================
def generate_architecture_diagram():
    W, H = 1400, 980
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "4.0 Architecture Diagram", "Pharmacy Management System – Microservices Architecture (5 Services)")

    # Left Column: Clients Box (x: 20 to 160)
    draw.rounded_rectangle([20, 110, 160, 560], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((50, 120), "Clients", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(20, 148), (160, 148)], fill=CLR_BORDER, width=1)

    clients = [
        ("Web UI", "(Doctor/Admin)", 165, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Swagger UI", "(API Testing)", 295, CLR_INV_MAIN, CLR_INV_BG),
        ("Other Clients", "(Mobile/POS)", 425, CLR_AUTH_MAIN, CLR_AUTH_BG)
    ]
    for c_title, c_sub, cy, clr, bg in clients:
        draw.rounded_rectangle([30, cy, 150, cy + 115], radius=8, fill=bg, outline=clr, width=2)
        # Desktop icon
        draw.rounded_rectangle([42, cy + 10, 138, cy + 65], radius=4, fill=CLR_WHITE, outline=clr, width=2)
        draw.line([(55, cy + 38), (125, cy + 38)], fill=clr, width=2)
        draw.line([(90, cy + 65), (90, cy + 74)], fill=clr, width=2)
        draw.line([(75, cy + 74), (105, cy + 74)], fill=clr, width=2)

        draw.text((44, cy + 78), c_title, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.text((36, cy + 96), c_sub, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(160, 180), (180, 180)], fill=CLR_BLACK, width=2)

    # Center Dashed Core Box (x: 180 to 1210)
    draw.rounded_rectangle([180, 110, 1210, 560], radius=10, outline=CLR_BORDER, width=2)

    # API Gateway Box
    draw.rounded_rectangle([195, 125, 1195, 185], radius=8, fill=CLR_GATE_BG, outline=CLR_BORDER, width=2)
    draw.ellipse([210, 140, 240, 170], fill=CLR_WHITE, outline=CLR_GATE_MAIN, width=2)
    draw.text((220, 143), "⚙", font=F_SEC_TITLE, fill=CLR_GATE_MAIN)
    draw.text((255, 135), "API Gateway (YARP / Reverse Proxy)", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((255, 160), "Request Routing | Load Balancing | JWT Validation | Rate Limiting | Health Checks", font=F_BODY_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(695, 185), (695, 205)], fill=CLR_BLACK, width=2)
    draw.line([(290, 205), (1100, 205)], fill=CLR_BLACK, width=2)

    # 5 Microservices Cards
    svcs = [
        {
            "name": "Auth Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• User Management", "• Role (Admin/Doctor)", "• JWT Authentication", "• RBAC Authorization"],
            "db": "AuthDB",
            "db_sub": "(Users Table)",
            "theme": CLR_AUTH_MAIN, "bg": CLR_AUTH_BG, "x": 195, "w": 195
        },
        {
            "name": "Inventory Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Drugs Catalog", "• Supplier Mgmt", "• Stock Inwarding", "• Atomic Deduction"],
            "db": "InventoryDB",
            "db_sub": "(Drugs, Suppliers, Inv)",
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG, "x": 397, "w": 195
        },
        {
            "name": "Order Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Doctor Order Mgmt", "• Cart / Pending Flow", "• Admin Verification", "• Handover PickedUp"],
            "db": "OrderDB",
            "db_sub": "(Orders, OrderItems)",
            "theme": CLR_ORDER_MAIN, "bg": CLR_ORDER_BG, "x": 599, "w": 195
        },
        {
            "name": "Payment Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Order Checkout", "• 1:1 Transaction Rule", "• Card / UPI Gateways", "• Reference Tracking"],
            "db": "PaymentDB",
            "db_sub": "(Payments Table)",
            "theme": CLR_PAY_MAIN, "bg": CLR_PAY_BG, "x": 801, "w": 195
        },
        {
            "name": "SaleReport Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Financial Reports", "• Daily/Wk/Mo/Yr", "• Revenue & Profit", "• CSV Export & Print"],
            "db": "SaleReportDB",
            "db_sub": "(SaleReports Table)",
            "theme": CLR_REP_MAIN, "bg": CLR_REP_BG, "x": 1003, "w": 195
        }
    ]

    for s in svcs:
        sx = s["x"]
        sw = s["w"]
        clr = s["theme"]
        bg = s["bg"]

        draw_arrow(draw, (sx + sw//2, 205), (sx + sw//2, 225), CLR_BLACK, 2)

        # Microservice box
        draw.rounded_rectangle([sx, 225, sx + sw, 440], radius=8, fill=CLR_WHITE, outline=clr, width=2)
        draw.rounded_rectangle([sx, 225, sx + sw, 275], radius=8, fill=bg, outline=clr, width=1)
        draw.rectangle([sx, 255, sx + sw, 275], fill=bg)

        draw.text((sx + 10, 233), s["name"], font=F_CARD_NAME, fill=CLR_BLACK)
        draw.text((sx + 10, 255), s["tech"], font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.line([(sx, 275), (sx + sw, 275)], fill=clr, width=1)

        for b_i, b_t in enumerate(s["bullets"]):
            draw.text((sx + 8, 285 + b_i * 36), b_t, font=F_NODE_TXT, fill=CLR_BLACK)

        draw_arrow(draw, (sx + sw//2, 440), (sx + sw//2, 465), clr, 2)
        draw_cylinder(draw, sx + 8, 465, sw - 16, 60, s["db"], s["db_sub"], clr, bg)

    # Service to service arrows
    draw_arrow(draw, (592, 310), (599, 310), CLR_BLACK, 2)
    draw_arrow(draw, (794, 310), (801, 310), CLR_BLACK, 2)

    # Shared common infrastructure box
    draw.rounded_rectangle([300, 532, 1090, 555], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((310, 535), "✉ Common Library (Shared): JWT Validation | PBKDF2 Hasher | ApiResponse Envelope | DTOs", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Right Column: Technology Stack (x: 1225 to 1385)
    draw.rounded_rectangle([1225, 110, 1385, 560], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1240, 120), "Technology Stack", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(1225, 148), (1385, 148)], fill=CLR_BORDER, width=1)

    tech = [
        (".NET", "ASP.NET Core Web API", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("C#", "C# 12 (LINQ & Async)", CLR_INV_MAIN, CLR_INV_BG),
        ("SQL", "SQL Server 2022 (5 DBs)", CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("YARP", "YARP (Reverse Proxy)", CLR_GATE_MAIN, CLR_GATE_BG),
        ("JWT", "JWT & RBAC Claims", CLR_PAY_MAIN, CLR_PAY_BG),
        ("EF", "EF Core 8 (Code-First)", CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("DOC", "Docker Containers", CLR_REP_MAIN, CLR_REP_BG),
        ("SWAG", "Swagger / OpenAPI 3.0", CLR_INV_MAIN, CLR_INV_BG)
    ]
    for idx, (b_txt, l_txt, clr, bg) in enumerate(tech):
        ty = 160 + idx * 49
        draw.rounded_rectangle([1235, ty, 1278, ty + 36], radius=4, fill=bg, outline=clr, width=2)
        draw.text((1240, ty + 10), b_txt, font=F_BADGE_TXT, fill=clr)
        draw.text((1286, ty + 4), l_txt.split(" (")[0], font=F_BODY_BOLD, fill=CLR_BLACK)
        if "(" in l_txt:
            draw.text((1286, ty + 20), "(" + l_txt.split("(")[1], font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Bottom Area: 3 Split Cards (x: 20 to 1385, y: 575 to 965)
    # Card 1: Service Interactions (x: 20 to 455)
    draw.rounded_rectangle([20, 575, 455, 965], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((35, 585), "Service Interactions – Order Flow (High Level)", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(20, 615), (455, 615)], fill=CLR_BORDER, width=1)

    # Actor Doctor
    draw.ellipse([35, 630, 75, 670], fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((46, 642), "Dr", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)
    draw.text((32, 675), "Doctor", font=F_BODY_BOLD, fill=CLR_BLACK)

    draw_arrow(draw, (75, 650), (125, 650), CLR_BLACK, 2)
    draw.ellipse([92, 634, 110, 652], fill=CLR_BLACK)
    draw.text((98, 636), "1", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([125, 628, 255, 680], radius=6, fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((135, 638), "Order Service", font=F_NODE_TXT, fill=CLR_ORDER_MAIN)
    draw.text((135, 658), "(POST /orders)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow(draw, (255, 645), (315, 645), CLR_BLACK, 2)
    draw.ellipse([278, 632, 296, 650], fill=CLR_BLACK)
    draw.text((284, 634), "2", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([315, 628, 445, 680], radius=6, fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((322, 638), "Inventory Service", font=F_NODE_TXT, fill=CLR_INV_MAIN)
    draw.text((325, 658), "(Deduct Stock Qty)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow(draw, (315, 668), (255, 668), CLR_BLACK, 2)
    draw.ellipse([278, 672, 296, 690], fill=CLR_BLACK)
    draw.text((284, 674), "3", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw_arrow(draw, (190, 680), (190, 715), CLR_BLACK, 2)
    draw.ellipse([195, 690, 213, 708], fill=CLR_BLACK)
    draw.text((201, 692), "4", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([125, 715, 255, 765], radius=6, fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((135, 725), "Payment Service", font=F_NODE_TXT, fill=CLR_PAY_MAIN)
    draw.text((135, 745), "(1:1 Payment Record)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow(draw, (255, 740), (315, 740), CLR_BLACK, 2)
    draw.ellipse([278, 725, 296, 743], fill=CLR_BLACK)
    draw.text((284, 727), "5", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([315, 715, 445, 765], radius=6, fill=CLR_AUTH_BG, outline=CLR_AUTH_MAIN, width=2)
    draw.text((325, 725), "Admin Handover", font=F_NODE_TXT, fill=CLR_AUTH_MAIN)
    draw.text((325, 745), "(Verify & PickedUp)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Details
    draw.rounded_rectangle([30, 785, 445, 950], radius=6, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=1)
    draw.text((40, 792), "Execution Steps:", font=F_BODY_BOLD, fill=CLR_BLACK)
    draw.text((40, 818), "1. Doctor authenticates and places medicine order.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 844), "2. Order Service requests stock reservation from Inventory.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 870), "3. Inventory confirms stock availability and decrements units.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 896), "4. Payment Service records unique 1:1 transaction.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 922), "5. Admin verifies order contents and completes PickedUp handover.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Card 2: Database Distribution Table (x: 470 to 920)
    draw.rounded_rectangle([470, 575, 920, 965], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((580, 585), "Database Distribution", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(470, 615), (920, 615)], fill=CLR_BORDER, width=1)

    # Table Header
    draw.rectangle([480, 630, 910, 665], fill=CLR_GATE_MAIN)
    draw.text((490, 640), "Service", font=F_BODY_BOLD, fill=CLR_WHITE)
    draw.text((645, 640), "Database", font=F_BODY_BOLD, fill=CLR_WHITE)
    draw.text((790, 640), "Key Tables", font=F_BODY_BOLD, fill=CLR_WHITE)

    db_rows = [
        ("Auth Service", "Pharmacy_UserDB", "Users", CLR_AUTH_BG),
        ("Inventory Service", "Pharmacy_InventoryDB", "Drugs, Suppliers, Inv", CLR_INV_BG),
        ("Order Service", "Pharmacy_OrderDB", "Orders, OrderItems", CLR_ORDER_BG),
        ("Payment Service", "Pharmacy_PaymentDB", "Payments (1:1 Unique)", CLR_PAY_BG),
        ("SaleReport Service", "Pharmacy_SaleReportDB", "SaleReports", CLR_REP_BG)
    ]
    for r_i, (svc_col, db_col, tbl_col, bg_col) in enumerate(db_rows):
        ry = 670 + r_i * 56
        draw.rectangle([480, ry, 910, ry + 50], fill=bg_col, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((490, ry + 15), svc_col, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.text((645, ry + 15), db_col, font=F_BODY_BOLD, fill=CLR_DARK_SLATE)
        draw.text((790, ry + 15), tbl_col, font=F_ATTR_BOLD, fill=CLR_BLACK)

    # Card 3: Key Highlights (x: 935 to 1385)
    draw.rounded_rectangle([935, 575, 1385, 965], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1060, 585), "Key Highlights", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(935, 615), (1385, 615)], fill=CLR_BORDER, width=1)

    highlights = [
        "✔ 5 independent microservices with separate dedicated SQL Server databases.",
        "✔ YARP API Gateway for reverse proxy routing, security, and rate limiting.",
        "✔ 1:1 Payment-to-Order unique constraint preventing duplicate transactions.",
        "✔ Strict Role-Based Access Control (Admin and Doctor) via JWT claims.",
        "✔ Inventory Service handles atomic stock deduction to prevent overselling.",
        "✔ Full internal MVC design with Controllers, Services, and Repositories.",
        "✔ High performance LINQ & EF Core 8 queries with connection pooling."
    ]
    for h_i, h_txt in enumerate(highlights):
        hy = 640 + h_i * 45
        draw.ellipse([950, hy, 972, hy + 22], fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
        draw.text((956, hy + 2), "✔", font=F_BADGE_TXT, fill=CLR_INV_MAIN)
        
        words = h_txt[2:].split(" ")
        w1 = " ".join(words[:7])
        w2 = " ".join(words[7:])
        draw.text((982, hy), w1, font=F_BODY_BOLD, fill=CLR_BLACK)
        if w2:
            draw.text((982, hy + 20), w2, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "01_Solution_Architecture_Diagram.jpg")

# ==============================================================================
# 2. USE CASE DIAGRAM (1350 x 880)
# ==============================================================================
def generate_use_case_diagram():
    W, H = 1350, 880
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "5.0 Use Case Diagram", "Pharmacy Management System – Use Case Diagram")

    # Big Boundary Box (x: 180 to 1180, y: 110 to 860)
    draw.rounded_rectangle([180, 110, 1180, 860], radius=12, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((500, 125), "Pharmacy Management System Boundary", font=F_SEC_TITLE, fill=CLR_BLACK)

    # Actor 1: Admin / Pharmacist (Left: x = 90)
    ax, ay = 90, 380
    draw.ellipse([ax - 22, ay - 60, ax + 22, ay - 16], outline=CLR_BLACK, width=3) # Head
    draw.line([(ax, ay - 16), (ax, ay + 45)], fill=CLR_BLACK, width=3)            # Spine
    draw.line([(ax - 35, ay + 8), (ax + 35, ay + 8)], fill=CLR_BLACK, width=3)   # Arms
    draw.line([(ax, ay + 45), (ax - 28, ay + 105)], fill=CLR_BLACK, width=3)      # Left leg
    draw.line([(ax, ay + 45), (ax + 28, ay + 105)], fill=CLR_BLACK, width=3)      # Right leg
    draw.text((ax - 50, ay + 115), "Admin / Pharmacist", font=F_CARD_NAME, fill=CLR_AUTH_MAIN)

    # Actor 2: Doctor (Right: x = 1270)
    dx, dy = 1270, 380
    draw.ellipse([dx - 22, dy - 60, dx + 22, dy - 16], outline=CLR_BLACK, width=3)
    draw.line([(dx, dy - 16), (dx, dy + 45)], fill=CLR_BLACK, width=3)
    draw.line([(dx - 35, dy + 8), (dx + 35, dy + 8)], fill=CLR_BLACK, width=3)
    draw.line([(dx, dy + 45), (dx - 28, dy + 105)], fill=CLR_BLACK, width=3)
    draw.line([(dx, dy + 45), (dx + 28, dy + 105)], fill=CLR_BLACK, width=3)
    draw.text((dx - 28, dy + 115), "Doctor", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)

    # Top Shared Oval: Login / Authenticate
    draw.ellipse([530, 160, 830, 220], fill=CLR_GATE_BG, outline=CLR_BORDER, width=2)
    draw.text((580, 180), "Login / Authenticate (JWT)", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.line([(ax + 25, ay - 30), (530, 190)], fill=CLR_BLACK, width=2)
    draw.line([(dx - 25, dy - 30), (830, 190)], fill=CLR_BLACK, width=2)

    # Admin Left Use Cases (x: 210 to 480)
    admin_ucs = [
        ("Manage Users & Roles", 250, CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Manage Drugs Catalog", 335, CLR_INV_MAIN, CLR_INV_BG),
        ("Manage Suppliers & Orders", 420, CLR_INV_MAIN, CLR_INV_BG),
        ("Manage Inventory (Stock)", 505, CLR_INV_MAIN, CLR_INV_BG),
        ("Verify & Handover Orders", 590, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Generate Financial Reports", 675, CLR_REP_MAIN, CLR_REP_BG)
    ]
    for u_txt, uy, clr, bg in admin_ucs:
        draw.ellipse([210, uy, 490, uy + 58], fill=bg, outline=clr, width=2)
        draw.text((250, uy + 18), u_txt, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.line([(ax + 25, ay + 10), (210, uy + 29)], fill=CLR_BLACK, width=2)

    # Doctor Right Use Cases (x: 870 to 1150)
    doc_ucs = [
        ("Search Available Drugs", 250, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("View Drug Prices & Stock", 335, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Create Prescription Order", 420, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Process Payment (Card/UPI)", 505, CLR_PAY_MAIN, CLR_PAY_BG),
        ("View My Orders History", 590, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Cancel Order (Before Paid)", 675, CLR_REP_MAIN, CLR_REP_BG)
    ]
    for u_txt, uy, clr, bg in doc_ucs:
        draw.ellipse([870, uy, 1150, uy + 58], fill=bg, outline=clr, width=2)
        draw.text((905, uy + 18), u_txt, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.line([(dx - 25, dy + 10), (1150, uy + 29)], fill=CLR_BLACK, width=2)

    # Center Hub Use Cases
    # Create / Manage Order (center: 540 to 820)
    draw.ellipse([540, 310, 820, 370], fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((610, 330), "Manage Orders Flow", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)

    draw.ellipse([540, 430, 820, 490], fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((585, 450), "Deduct Stock & Reserve Qty", font=F_CARD_NAME, fill=CLR_INV_MAIN)

    draw.ellipse([540, 550, 820, 610], fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((595, 570), "Record 1:1 Payment Ref", font=F_CARD_NAME, fill=CLR_PAY_MAIN)

    draw.ellipse([540, 670, 820, 730], fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((590, 690), "Export CSV Sales Summary", font=F_CARD_NAME, fill=CLR_REP_MAIN)

    # <<include>> and <<extend>> dashed arrows
    draw_arrow(draw, (680, 370), (680, 430), CLR_BORDER, 2, "<<include>>", False)
    draw_arrow(draw, (680, 490), (680, 550), CLR_BORDER, 2, "<<include>>", False)
    draw_arrow(draw, (680, 730), (680, 670), CLR_BORDER, 2, "<<extend>>", True)

    draw_arrow(draw, (870, 449), (820, 345), CLR_ORDER_MAIN, 2, "<<include>>", True)
    draw_arrow(draw, (490, 619), (540, 350), CLR_ORDER_MAIN, 2, "<<include>>", True)
    draw_arrow(draw, (490, 704), (540, 700), CLR_REP_MAIN, 2, "<<extend>>", True)

    # Bottom notes
    draw.rounded_rectangle([250, 785, 1110, 845], radius=6, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=1)
    draw.text((270, 795), "Legend & Notes:", font=F_BODY_BOLD, fill=CLR_BLACK)
    draw.text((270, 818), "• <<include>>: Stock deduction and payment recording are mandatory during order placement.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((750, 818), "• <<extend>>: Order cancellation & CSV export are conditional actions.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "02_Use_Case_Diagram.jpg")

# ==============================================================================
# 3. SEQUENCE DIAGRAM (1350 x 1020)
# ==============================================================================
def generate_sequence_diagram():
    W, H = 1350, 1020
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "11.0 Sequence Diagram", "Pharmacy Management System – End-to-End Order & Handover Flow")

    # 6 Participants across the width
    participants = [
        ("Doctor User", "(Client)", 90, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("YARP Gateway", "(Reverse Proxy)", 310, CLR_GATE_MAIN, CLR_GATE_BG),
        ("Auth Service", "(Pharmacy_UserDB)", 530, CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Order Service", "(Pharmacy_OrderDB)", 750, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Inventory Svc", "(Pharmacy_InvDB)", 970, CLR_INV_MAIN, CLR_INV_BG),
        ("Payment Svc", "(Pharmacy_PayDB)", 1190, CLR_PAY_MAIN, CLR_PAY_BG)
    ]

    for name, sub, px, clr, bg in participants:
        # Header box
        draw.rounded_rectangle([px - 85, 120, px + 85, 175], radius=8, fill=bg, outline=clr, width=2)
        draw.text((px - 70, 130), name, font=F_CARD_NAME, fill=CLR_BLACK)
        draw.text((px - 70, 153), sub, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

        # Lifeline
        draw.line([(px, 175), (px, 940)], fill=CLR_BORDER_LIGHT, width=2)

        # Footer box
        draw.rounded_rectangle([px - 85, 940, px + 85, 990], radius=8, fill=bg, outline=clr, width=2)
        draw.text((px - 50, 955), name, font=F_BODY_BOLD, fill=CLR_BLACK)

    # Step Sequence
    steps = [
        # (y, from_x, to_x, label, is_return, status, clr)
        (205, 90, 310, "1: POST /api/auth/login {email, pwd}", False, "", CLR_BLACK),
        (240, 310, 530, "2: ValidateCredentials() & Hash Check", False, "", CLR_AUTH_MAIN),
        (275, 530, 310, "3: 200 OK + JWT Bearer Token (Role: Doctor)", True, "200 OK", CLR_AUTH_MAIN),
        (310, 310, 90, "4: Return AuthResponse Token to Client", True, "200 OK", CLR_BLACK),

        (360, 90, 310, "5: POST /api/orders [Bearer Token] {items}", False, "", CLR_ORDER_MAIN),
        (395, 310, 750, "6: Forward Order Payload to OrderService", False, "", CLR_ORDER_MAIN),
        (435, 750, 970, "7: POST /api/inventory/deduct {drugId, qty}", False, "", CLR_INV_MAIN),
        (475, 970, 750, "8: 200 OK Stock Deducted & Reserved", True, "200 OK", CLR_INV_MAIN),

        (525, 750, 1190, "9: POST /api/payments {orderId, amount, method}", False, "", CLR_PAY_MAIN),
        (565, 1190, 750, "10: 200 OK Payment Recorded [Unique TxRef]", True, "200 OK", CLR_PAY_MAIN),

        (615, 750, 310, "11: Order Created (Status: Pending) + OrderId", True, "201 Created", CLR_ORDER_MAIN),
        (650, 310, 90, "12: Return Order Confirmation & Invoice ID", True, "201 Created", CLR_BLACK),

        # Admin Phase
        (720, 90, 310, "13: Admin signs in & navigates to Pending Orders", False, "", CLR_AUTH_MAIN),
        (760, 310, 750, "14: PUT /api/orders/{id}/verify (Validate Prescriptions)", False, "", CLR_ORDER_MAIN),
        (800, 750, 310, "15: Status Updated: 'Verified'", True, "200 OK", CLR_ORDER_MAIN),

        (845, 90, 750, "16: Admin completes Handover -> PUT /api/orders/{id}/pickup", False, "", CLR_INV_MAIN),
        (885, 750, 90, "17: 200 OK Order Status = 'PickedUp' (Completed)", True, "200 OK", CLR_INV_MAIN)
    ]

    for y, fx, tx, lbl, is_ret, stat, clr in steps:
        if is_ret:
            # Dashed return line
            x_min, x_max = min(fx, tx), max(fx, tx)
            for dx in range(x_min, x_max, 12):
                draw.line([(dx, y), (min(dx + 6, x_max), y)], fill=clr, width=2)
            # Left or right arrow head
            if tx < fx:
                draw.polygon([(tx, y), (tx + 10, y - 5), (tx + 10, y + 5)], fill=clr)
            else:
                draw.polygon([(tx, y), (tx - 10, y - 5), (tx - 10, y + 5)], fill=clr)
        else:
            draw_arrow(draw, (fx, y), (tx, y), clr, 2)

        # Label badge
        mx = (fx + tx) // 2
        bbox = F_BODY_BOLD.getbbox(lbl)
        lw = bbox[2] - bbox[0] + 16
        draw.rounded_rectangle([mx - lw//2, y - 18, mx + lw//2, y + 2], radius=4, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((mx - lw//2 + 8, y - 16), lbl, font=F_BODY_BOLD, fill=clr)

    save_image(img, "03_Sequence_Diagram.jpg")

# ==============================================================================
# 4. FLOW DIAGRAM (1150 x 1350)
# ==============================================================================
def generate_flow_diagram():
    W, H = 1150, 1350
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "6.0 Flow Diagram", "PHARMACY MANAGEMENT SYSTEM - FLOW DIAGRAM")

    # START Pill
    draw.rounded_rectangle([485, 120, 665, 165], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((545, 130), "START", font=F_CARD_NAME, fill=CLR_BLACK)
    draw_arrow(draw, (575, 165), (575, 195), CLR_BLACK, 2)

    # Login Box
    draw.rounded_rectangle([330, 195, 820, 245], radius=8, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((365, 208), "User Registration / Customer or Admin Login", font=F_CARD_NAME, fill=CLR_BLACK)
    draw_arrow(draw, (575, 245), (575, 280), CLR_BLACK, 2)

    # Role Diamond
    # Diamond at (575, 315)
    dw = 85
    dh = 40
    pts = [(575, 280), (575 + dw, 315), (575, 350), (575 - dw, 315)]
    draw.polygon(pts, fill=CLR_WHITE, outline=CLR_BORDER)
    draw.line(pts + [pts[0]], fill=CLR_BORDER, width=2)
    draw.text((552, 303), "Role?", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2 Branching Arrows: Admin (Left) & Doctor (Right)
    # Left Branch: Admin / Pharmacist
    draw.line([(575 - dw, 315), (240, 315)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (240, 315), (240, 360), CLR_BLACK, 2)
    draw.text((290, 290), "Admin / Pharmacist", font=F_BODY_BOLD, fill=CLR_AUTH_MAIN)

    # Right Branch: Doctor / Customer
    draw.line([(575 + dw, 315), (910, 315)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (910, 315), (910, 360), CLR_BLACK, 2)
    draw.text((710, 290), "Doctor / Customer", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)

    # Admin Lane (Left Column: x: 80 to 400)
    admin_boxes = [
        ("Manage Users & Roles", 360, CLR_AUTH_BG, CLR_AUTH_MAIN),
        ("Manage Drugs Catalog (Price & Qty)", 445, CLR_INV_BG, CLR_INV_MAIN),
        ("Manage Suppliers & Stock Inward", 530, CLR_INV_BG, CLR_INV_MAIN),
        ("Verify Orders & Check Prescriptions", 615, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Handover Medicine (Mark PickedUp)", 700, CLR_INV_BG, CLR_INV_MAIN),
        ("View Sales Reports (Revenue & Profit)", 785, CLR_REP_BG, CLR_REP_MAIN)
    ]
    for b_t, by, bg, clr in admin_boxes:
        draw.rounded_rectangle([80, by, 400, by + 55], radius=8, fill=bg, outline=clr, width=2)
        draw.text((105, by + 16), b_t, font=F_NODE_TXT, fill=CLR_BLACK)
        if by < 785:
            draw_arrow(draw, (240, by + 55), (240, by + 85), CLR_BLACK, 2)

    # Doctor Lane (Right Column: x: 750 to 1070)
    doc_boxes = [
        ("Search Available Drugs & Stock", 360, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("View Drug Details & Unit Price", 445, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Select Quantities & Add to Cart", 530, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Create Order (Enter Prescription)", 615, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Calculate Total Amount (Qty * Price)", 700, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Proceed to Payment (Card / UPI)", 785, CLR_PAY_BG, CLR_PAY_MAIN)
    ]
    for b_t, by, bg, clr in doc_boxes:
        draw.rounded_rectangle([750, by, 1070, by + 55], radius=8, fill=bg, outline=clr, width=2)
        draw.text((770, by + 16), b_t, font=F_NODE_TXT, fill=CLR_BLACK)
        draw_arrow(draw, (910, by + 55), (910, by + 85), CLR_BLACK, 2)

    # Center Flow: Payment Decision Diamond
    # Connected from Doctor Step 6 (y = 840) to Center Diamond (y = 880)
    draw.line([(910, 840), (910, 865)], fill=CLR_BLACK, width=2)
    draw.line([(910, 865), (575, 865)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (575, 865), (575, 890), CLR_BLACK, 2)

    # Payment Successful? Diamond
    p_dw = 100
    p_dh = 45
    p_pts = [(575, 890), (575 + p_dw, 935), (575, 980), (575 - p_dw, 935)]
    draw.polygon(p_pts, fill=CLR_WHITE, outline=CLR_BORDER)
    draw.line(p_pts + [p_pts[0]], fill=CLR_BORDER, width=2)
    draw.text((505, 922), "Payment Successful?", font=F_CARD_NAME, fill=CLR_BLACK)

    # Branch NO (Left to Dashed Box)
    draw.line([(575 - p_dw, 935), (380, 935)], fill=CLR_REP_MAIN, width=2)
    draw_arrow(draw, (380, 935), (350, 935), CLR_REP_MAIN, 2)
    draw.text((410, 910), "No", font=F_CARD_NAME, fill=CLR_REP_MAIN)

    # Payment Failed Box (Dashed: x: 100 to 350, y: 890 to 1180)
    draw.rounded_rectangle([100, 890, 350, 1180], radius=10, fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((140, 905), "Payment Failed Subflow", font=F_CARD_NAME, fill=CLR_REP_MAIN)
    draw.line([(100, 935), (350, 935)], fill=CLR_REP_BORDER, width=1)

    fail_steps = [
        ("Show Failure Message", 950),
        ("Update Order Status = 'Failed'", 1010),
        ("Release Reserved Drug Stock", 1070)
    ]
    for ft, fy in fail_steps:
        draw.rounded_rectangle([115, fy, 335, fy + 44], radius=6, fill=CLR_WHITE, outline=CLR_REP_BORDER, width=2)
        draw.text((130, fy + 12), ft, font=F_NODE_TXT, fill=CLR_BLACK)
        if fy < 1070:
            draw_arrow(draw, (225, fy + 44), (225, fy + 60), CLR_REP_MAIN, 2)

    draw.rounded_rectangle([115, 1130, 335, 1170], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((145, 1140), "Cancel Order Record", font=F_BODY_BOLD, fill=CLR_BLACK)

    # Branch YES (Down to Success Flow)
    draw_arrow(draw, (575, 980), (575, 1015), CLR_INV_MAIN, 2)
    draw.text((585, 990), "Yes", font=F_CARD_NAME, fill=CLR_INV_MAIN)

    success_boxes = [
        ("Confirm Order (Status = 'Pending' / 'Paid')", 1015, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Generate Invoice & Trans Reference", 1085, CLR_PAY_BG, CLR_PAY_MAIN),
        ("Notify Pharmacist for Pickup Handover", 1155, CLR_INV_BG, CLR_INV_MAIN)
    ]
    for st, sy, sbg, sclr in success_boxes:
        draw.rounded_rectangle([420, sy, 880, sy + 50], radius=8, fill=sbg, outline=sclr, width=2)
        draw.text((455, sy + 15), st, font=F_CARD_NAME, fill=CLR_BLACK)
        if sy < 1155:
            draw_arrow(draw, (650, sy + 50), (650, sy + 70), CLR_BLACK, 2)

    # Connect Admin 6, Payment Failed, and Success to END Pill
    draw_arrow(draw, (650, 1205), (650, 1245), CLR_BLACK, 2)
    draw.line([(225, 1170), (225, 1225)], fill=CLR_BLACK, width=2)
    draw.line([(225, 1225), (550, 1225)], fill=CLR_BLACK, width=2)
    draw.line([(240, 840), (240, 860)], fill=CLR_BLACK, width=2)

    # END Pill
    draw.rounded_rectangle([560, 1245, 740, 1290], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((625, 1255), "END", font=F_CARD_NAME, fill=CLR_BLACK)

    save_image(img, "04_Flow_Diagram.jpg")

# ==============================================================================
# 5. ER DIAGRAM (1380 x 950)
# ==============================================================================
def generate_er_diagram():
    W, H = 1380, 950
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "9.0 ER Diagram", "Pharmacy Management System – Entity-Relationship (ER) Diagram")

    # Entities definitions
    # Top Row: Users (x: 50), Orders (x: 480), OrderItems (x: 930)
    # Middle Row: Payments (x: 480), Drugs (x: 930)
    # Bottom Row: SaleReports (x: 50), Suppliers (x: 480), Inventory (x: 930)

    entities = [
        {
            "name": "Users", "tag": "(AuthDB)", "x": 60, "y": 130, "w": 260, "h": 220,
            "theme": CLR_AUTH_MAIN, "bg": CLR_AUTH_BG,
            "attrs": ["PK UserId (int)", "Name (nvarchar)", "Email (nvarchar)", "PhoneNumber (nvarchar)", "PasswordHash (nvarchar)", "Role (Admin/Doctor)", "IsActive (bit)"]
        },
        {
            "name": "Orders", "tag": "(OrderDB)", "x": 520, "y": 130, "w": 260, "h": 200,
            "theme": CLR_ORDER_MAIN, "bg": CLR_ORDER_BG,
            "attrs": ["PK OrderId (int)", "FK DoctorID (int)", "OrderDate (datetime2)", "TotalAmount (decimal)", "Status (nvarchar)"]
        },
        {
            "name": "OrderItems", "tag": "(OrderDB)", "x": 980, "y": 130, "w": 270, "h": 200,
            "theme": CLR_ORDER_MAIN, "bg": CLR_ORDER_BG,
            "attrs": ["PK OrderItemId (int)", "FK OrderId (int)", "FK DrugId (int)", "DrugName (nvarchar)", "Quantity (int)", "UnitPrice (decimal)"]
        },
        {
            "name": "Payments", "tag": "(PaymentDB)", "x": 520, "y": 420, "w": 260, "h": 220,
            "theme": CLR_PAY_MAIN, "bg": CLR_PAY_BG,
            "attrs": ["PK PaymentId (int)", "FK OrderId (int) [UNIQUE]", "Amount (decimal)", "PaymentDate (datetime2)", "PaymentMethod (nvarchar)", "PaymentStatus (nvarchar)", "TxReference (nvarchar)"]
        },
        {
            "name": "Drugs", "tag": "(InventoryDB)", "x": 980, "y": 420, "w": 270, "h": 220,
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG,
            "attrs": ["PK DrugId (int)", "Name (nvarchar)", "Description (nvarchar)", "Price (decimal)", "ExpiryDate (date)", "Quantity (int)", "IsAvailable (bit)"]
        },
        {
            "name": "SaleReports", "tag": "(SaleReportDB)", "x": 60, "y": 420, "w": 260, "h": 220,
            "theme": CLR_REP_MAIN, "bg": CLR_REP_BG,
            "attrs": ["PK SaleReportId (int)", "ReportType (nvarchar)", "FromDate (datetime2)", "ToDate (datetime2)", "TotalOrders (int)", "TotalRevenue (decimal)", "Profit (decimal)"]
        },
        {
            "name": "Suppliers", "tag": "(InventoryDB)", "x": 520, "y": 700, "w": 260, "h": 200,
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG,
            "attrs": ["PK SupplierId (int)", "SupplierName (nvarchar)", "Email (nvarchar)", "PhoneNumber (nvarchar)", "Address (nvarchar)"]
        },
        {
            "name": "Inventory", "tag": "(InventoryDB)", "x": 980, "y": 700, "w": 270, "h": 200,
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG,
            "attrs": ["PK InventoryId (int)", "FK SupplierId (int)", "FK DrugId (int)", "PurchasePrice (decimal)", "QuantityAdded (int)", "StockReceivedDate"]
        }
    ]

    for ent in entities:
        ex, ey, ew, eh = ent["x"], ent["y"], ent["w"], ent["h"]
        clr, bg = ent["theme"], ent["bg"]

        draw.rounded_rectangle([ex, ey, ex + ew, ey + eh], radius=8, fill=CLR_WHITE, outline=clr, width=2)
        draw.rounded_rectangle([ex, ey, ex + ew, ey + 40], radius=8, fill=bg, outline=clr, width=1)
        draw.rectangle([ex, ey + 25, ex + ew, ey + 40], fill=bg)

        draw.text((ex + 12, ey + 8), ent["name"], font=F_CARD_NAME, fill=CLR_BLACK)
        draw.text((ex + ew - 100, ey + 10), ent["tag"], font=F_ATTR_BOLD, fill=clr)
        draw.line([(ex, ey + 40), (ex + ew, ey + 40)], fill=clr, width=1)

        for a_i, a_t in enumerate(ent["attrs"]):
            ay = ey + 48 + a_i * 24
            if a_t.startswith("PK"):
                draw.text((ex + 10, ay), "🔑 " + a_t, font=F_BODY_BOLD, fill=CLR_AUTH_MAIN)
            elif a_t.startswith("FK"):
                draw.text((ex + 10, ay), "🔗 " + a_t, font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            else:
                draw.text((ex + 10, ay), "• " + a_t, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Relationship Diamonds & Connector Lines
    def draw_rel_diamond(cx, cy, label):
        rw, rh = 48, 24
        draw.polygon([(cx, cy - rh), (cx + rw, cy), (cx, cy + rh), (cx - rw, cy)], fill=CLR_GATE_BG, outline=CLR_BORDER)
        draw.line([(cx, cy - rh), (cx + rw, cy), (cx, cy + rh), (cx - rw, cy), (cx, cy - rh)], fill=CLR_BORDER, width=2)
        bbox = F_BADGE_TXT.getbbox(label)
        draw.text((cx - (bbox[2]-bbox[0])//2, cy - 8), label, font=F_BADGE_TXT, fill=CLR_BLACK)

    # 1. Users --- places ---> Orders (1 : N)
    draw.line([(320, 220), (520, 220)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(420, 220, "places")
    draw.text((330, 195), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((495, 195), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2. Orders --- contains ---> OrderItems (1 : N)
    draw.line([(780, 220), (980, 220)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(880, 220, "has")
    draw.text((795, 195), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((955, 195), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 3. Orders --- paid by ---> Payments (1 : 1 UNIQUE)
    draw.line([(650, 330), (650, 420)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(650, 375, "paid by")
    draw.text((660, 335), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((660, 395), "1 (Unique)", font=F_ATTR_BOLD, fill=CLR_PAY_MAIN)

    # 4. Drugs --- refers ---> OrderItems (1 : N)
    draw.line([(1115, 420), (1115, 330)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(1115, 375, "item")
    draw.text((1125, 400), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1125, 335), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 5. Suppliers --- supplies ---> Inventory (1 : N)
    draw.line([(780, 780), (980, 780)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(880, 780, "supplies")
    draw.text((795, 755), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((955, 755), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 6. Drugs --- stocked ---> Inventory (1 : N)
    draw.line([(1115, 640), (1115, 700)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(1115, 670, "stocked")
    draw.text((1125, 642), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1125, 680), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # Bottom Legend
    draw.rounded_rectangle([60, 680, 440, 920], radius=8, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((75, 695), "Cardinality & Architecture Rules:", font=F_BODY_BOLD, fill=CLR_BLACK)
    draw.text((75, 725), "• 1 : N = One-to-Many Relationship.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((75, 755), "• 1 : 1 Unique = Exact single Payment per Order (Enforced).", font=F_ATTR_BOLD, fill=CLR_PAY_MAIN)
    draw.text((75, 785), "• Cross-service foreign keys are logical (Zero direct SQL joins).", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((75, 815), "• All cross-database consistency verified via REST API contracts.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "05_ER_Diagram.jpg")

# ==============================================================================
# 6. DATABASE SCHEMA DIAGRAM (1400 x 960)
# ==============================================================================
def generate_database_schema_diagram():
    W, H = 1400, 960
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "2.0 Database Diagram", "Pharmacy Management System – Database Diagram (5 Databases)")

    # 5 Containers representing each microservice DB
    # Container 1: Auth Service - AuthDB (x: 20 to 450, y: 110 to 420)
    draw.rounded_rectangle([20, 110, 450, 420], radius=10, fill=CLR_WHITE, outline=CLR_AUTH_BORDER, width=2)
    draw.rounded_rectangle([35, 120, 435, 155], radius=6, fill=CLR_AUTH_BG, outline=CLR_AUTH_MAIN, width=2)
    draw.text((45, 128), "🛢 Auth Service – Pharmacy_UserDB", font=F_CARD_NAME, fill=CLR_AUTH_MAIN)

    # Users Table
    draw.rounded_rectangle([40, 170, 430, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([40, 170, 430, 205], fill=CLR_GATE_MAIN)
    draw.text((50, 178), "Users", font=F_CARD_NAME, fill=CLR_WHITE)
    draw.text((330, 180), "Table (Entity)", font=F_ATTR_BOLD, fill=CLR_BORDER_LIGHT)

    u_cols = [
        ("PK", "UserId", "int", True),
        ("", "Name", "nvarchar(100)", False),
        ("", "Email", "nvarchar(100)", False),
        ("", "PhoneNumber", "nvarchar(20)", False),
        ("", "PasswordHash", "nvarchar(255)", False),
        ("", "Role", "nvarchar(20)", False),
        ("", "IsActive", "bit", False),
        ("", "CreatedDate", "datetime2", False)
    ]
    for ci, (pk, cname, ctype, is_pk) in enumerate(u_cols):
        cy = 212 + ci * 23
        if is_pk:
            draw.text((50, cy), "PK", font=F_BODY_BOLD, fill=CLR_AUTH_MAIN)
            draw.text((85, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((85, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((280, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Container 2: Inventory Service - InventoryDB (x: 470 to 1380, y: 110 to 420)
    draw.rounded_rectangle([470, 110, 1380, 420], radius=10, fill=CLR_WHITE, outline=CLR_INV_BORDER, width=2)
    draw.rounded_rectangle([485, 120, 1365, 155], radius=6, fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((495, 128), "🛢 Inventory Service – Pharmacy_InventoryDB", font=F_CARD_NAME, fill=CLR_INV_MAIN)

    # Drugs Table (x: 485 to 765)
    draw.rounded_rectangle([485, 170, 765, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([485, 170, 765, 205], fill=CLR_GATE_MAIN)
    draw.text((495, 178), "Drugs", font=F_CARD_NAME, fill=CLR_WHITE)
    d_cols = [
        ("PK", "DrugId", "int", True),
        ("", "Name", "nvarchar(100)", False),
        ("", "Description", "nvarchar(255)", False),
        ("", "Price", "decimal(18,2)", False),
        ("", "ExpiryDate", "date", False),
        ("", "Quantity", "int", False),
        ("", "IsAvailable", "bit", False)
    ]
    for ci, (pk, cname, ctype, is_pk) in enumerate(d_cols):
        cy = 212 + ci * 25
        if is_pk:
            draw.text((495, cy), "PK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((530, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((530, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((660, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Suppliers Table (x: 785 to 1065)
    draw.rounded_rectangle([785, 170, 1065, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([785, 170, 1065, 205], fill=CLR_GATE_MAIN)
    draw.text((795, 178), "Suppliers", font=F_CARD_NAME, fill=CLR_WHITE)
    s_cols = [
        ("PK", "SupplierId", "int", True),
        ("", "SupplierName", "nvarchar(100)", False),
        ("", "Email", "nvarchar(100)", False),
        ("", "PhoneNumber", "nvarchar(20)", False),
        ("", "Address", "nvarchar(255)", False)
    ]
    for ci, (pk, cname, ctype, is_pk) in enumerate(s_cols):
        cy = 212 + ci * 28
        if is_pk:
            draw.text((795, cy), "PK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((830, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((830, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((945, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Inventory Table (x: 1085 to 1365)
    draw.rounded_rectangle([1085, 170, 1365, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([1085, 170, 1365, 205], fill=CLR_GATE_MAIN)
    draw.text((1095, 178), "Inventory", font=F_CARD_NAME, fill=CLR_WHITE)
    i_cols = [
        ("PK", "InventoryId", "int", True, False),
        ("FK", "SupplierId", "int", False, True),
        ("FK", "DrugId", "int", False, True),
        ("", "PurchasePrice", "decimal(18,2)", False, False),
        ("", "QuantityAdded", "int", False, False),
        ("", "StockReceived", "datetime2", False, False)
    ]
    for ci, (tag, cname, ctype, is_pk, is_fk) in enumerate(i_cols):
        cy = 212 + ci * 28
        if is_pk:
            draw.text((1095, cy), "PK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((1130, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        elif is_fk:
            draw.text((1095, cy), "FK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((1130, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((1130, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((1255, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Relationship connectors inside InventoryDB
    draw.line([(765, 225), (785, 225)], fill=CLR_BLACK, width=2)
    draw.line([(1065, 225), (1085, 225)], fill=CLR_BLACK, width=2)
    draw.text((1070, 205), "1:N", font=F_BADGE_TXT, fill=CLR_BLACK)

    # Row 2: OrderDB (x: 20 to 680, y: 435 to 690)
    draw.rounded_rectangle([20, 435, 680, 690], radius=10, fill=CLR_WHITE, outline=CLR_ORDER_BORDER, width=2)
    draw.rounded_rectangle([35, 445, 665, 480], radius=6, fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((45, 453), "🛢 Order Service – Pharmacy_OrderDB", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)

    # Orders Table (x: 40 to 340)
    draw.rounded_rectangle([40, 495, 340, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([40, 495, 340, 528], fill=CLR_GATE_MAIN)
    draw.text((50, 502), "Orders", font=F_CARD_NAME, fill=CLR_WHITE)
    o_cols = [
        ("PK", "OrderId", "int", True),
        ("", "DoctorID", "int", False),
        ("", "OrderDate", "datetime2", False),
        ("", "TotalAmount", "decimal(18,2)", False),
        ("", "Status", "nvarchar(20)", False)
    ]
    for ci, (pk, cname, ctype, is_pk) in enumerate(o_cols):
        cy = 538 + ci * 26
        if is_pk:
            draw.text((50, cy), "PK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((85, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((85, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((215, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # OrderItems Table (x: 360 to 660)
    draw.rounded_rectangle([360, 495, 660, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([360, 495, 660, 528], fill=CLR_GATE_MAIN)
    draw.text((370, 502), "OrderItems", font=F_CARD_NAME, fill=CLR_WHITE)
    oi_cols = [
        ("PK", "OrderItemId", "int", True, False),
        ("FK", "OrderId", "int", False, True),
        ("FK", "DrugId", "int", False, True),
        ("", "DrugName", "nvarchar(100)", False, False),
        ("", "Quantity", "int", False, False),
        ("", "UnitPrice", "decimal(18,2)", False, False)
    ]
    for ci, (tag, cname, ctype, is_pk, is_fk) in enumerate(oi_cols):
        cy = 535 + ci * 23
        if is_pk:
            draw.text((370, cy), "PK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((405, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        elif is_fk:
            draw.text((370, cy), "FK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((405, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((405, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((545, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(340, 545), (360, 545)], fill=CLR_BLACK, width=2)
    draw.text((345, 525), "1:N", font=F_BADGE_TXT, fill=CLR_BLACK)

    # Container 4: PaymentDB (x: 700 to 1030, y: 435 to 690)
    draw.rounded_rectangle([700, 435, 1030, 690], radius=10, fill=CLR_WHITE, outline=CLR_PAY_BORDER, width=2)
    draw.rounded_rectangle([715, 445, 1015, 480], radius=6, fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((725, 453), "🛢 Payment Service – PaymentDB", font=F_CARD_NAME, fill=CLR_PAY_MAIN)

    draw.rounded_rectangle([715, 495, 1015, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([715, 495, 1015, 528], fill=CLR_GATE_MAIN)
    draw.text((725, 502), "Payments", font=F_CARD_NAME, fill=CLR_WHITE)
    p_cols = [
        ("PK", "PaymentId", "int", True, False),
        ("FK", "OrderId (1:1 Unique)", "int", False, True),
        ("", "Amount", "decimal(18,2)", False, False),
        ("", "PaymentDate", "datetime2", False, False),
        ("", "PaymentMethod", "nvarchar(50)", False, False),
        ("", "PaymentStatus", "nvarchar(20)", False, False),
        ("", "TxReference", "nvarchar(100)", False, False)
    ]
    for ci, (tag, cname, ctype, is_pk, is_fk) in enumerate(p_cols):
        cy = 533 + ci * 20
        if is_pk:
            draw.text((725, cy), "PK", font=F_BODY_BOLD, fill=CLR_PAY_MAIN)
            draw.text((760, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        elif is_fk:
            draw.text((725, cy), "FK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((760, cy), cname, font=F_BODY_BOLD, fill=CLR_PAY_MAIN)
        else:
            draw.text((760, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((920, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Container 5: SaleReportDB (x: 1050 to 1380, y: 435 to 690)
    draw.rounded_rectangle([1050, 435, 1380, 690], radius=10, fill=CLR_WHITE, outline=CLR_REP_BORDER, width=2)
    draw.rounded_rectangle([1065, 445, 1365, 480], radius=6, fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((1075, 453), "🛢 SaleReport Service – DB", font=F_CARD_NAME, fill=CLR_REP_MAIN)

    draw.rounded_rectangle([1065, 495, 1365, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([1065, 495, 1365, 528], fill=CLR_GATE_MAIN)
    draw.text((1075, 502), "SaleReports", font=F_CARD_NAME, fill=CLR_WHITE)
    sr_cols = [
        ("PK", "SaleReportId", "int", True),
        ("", "ReportType", "nvarchar(20)", False),
        ("", "FromDate", "datetime2", False),
        ("", "ToDate", "datetime2", False),
        ("", "TotalOrders", "int", False),
        ("", "TotalRevenue", "decimal(18,2)", False),
        ("", "Profit", "decimal(18,2)", False)
    ]
    for ci, (pk, cname, ctype, is_pk) in enumerate(sr_cols):
        cy = 533 + ci * 20
        if is_pk:
            draw.text((1075, cy), "PK", font=F_BODY_BOLD, fill=CLR_REP_MAIN)
            draw.text((1110, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((1110, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((1260, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Bottom Area: 3 Summary Panels (y: 705 to 945)
    # Panel 1: Database Summary (x: 20 to 500)
    draw.rounded_rectangle([20, 705, 500, 945], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((35, 715), "Database Summary", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(20, 742), (500, 742)], fill=CLR_BORDER, width=1)

    draw.rectangle([30, 752, 490, 780], fill=CLR_GATE_MAIN)
    draw.text((38, 758), "Database (Service)", font=F_BODY_BOLD, fill=CLR_WHITE)
    draw.text((270, 758), "Key Tables", font=F_BODY_BOLD, fill=CLR_WHITE)

    d_summary = [
        ("Pharmacy_UserDB (Auth)", "Users Table", CLR_AUTH_BG),
        ("Pharmacy_InventoryDB (Inv)", "Drugs, Suppliers, Inventory", CLR_INV_BG),
        ("Pharmacy_OrderDB (Order)", "Orders, OrderItems", CLR_ORDER_BG),
        ("Pharmacy_PaymentDB (Pay)", "Payments (1:1 Unique)", CLR_PAY_BG),
        ("Pharmacy_SaleReportDB (Rep)", "SaleReports", CLR_REP_BG)
    ]
    for si, (d_name, d_tbls, bg_col) in enumerate(d_summary):
        sy = 784 + si * 30
        draw.rectangle([30, sy, 490, sy + 27], fill=bg_col, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((38, sy + 6), d_name, font=F_ATTR_BOLD, fill=CLR_BLACK)
        draw.text((270, sy + 6), d_tbls, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Panel 2: Legend (x: 515 to 880)
    draw.rounded_rectangle([515, 705, 880, 945], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((530, 715), "Legend", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(515, 742), (880, 742)], fill=CLR_BORDER, width=1)

    legend_items = [
        ("PK", "Primary Key (Unique Identifier)", CLR_AUTH_MAIN),
        ("FK", "Foreign Key (Cross-Table Reference)", CLR_ORDER_MAIN),
        ("1 : N", "One-to-Many Relationship", CLR_BLACK),
        ("1 : 1", "One-to-One Unique Relationship", CLR_PAY_MAIN),
        ("Entity", "Table Box with Typed Attributes", CLR_DARK_SLATE),
        ("Index", "Unique Index on Payments.OrderId", CLR_INV_MAIN)
    ]
    for li, (ltag, ldesc, lclr) in enumerate(legend_items):
        ly = 758 + li * 29
        draw.rounded_rectangle([530, ly, 580, ly + 22], radius=4, fill=CLR_GATE_BG, outline=lclr, width=2)
        draw.text((538, ly + 2), ltag, font=F_BODY_BOLD, fill=lclr)
        draw.text((592, ly + 2), ldesc, font=F_ATTR_BOLD, fill=CLR_BLACK)

    # Panel 3: Key Notes (x: 895 to 1380)
    draw.rounded_rectangle([895, 705, 1380, 945], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((910, 715), "Key Architectural Notes", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(895, 742), (1380, 742)], fill=CLR_BORDER, width=1)

    k_notes = [
        "• 5 independent databases completely isolate data per microservice.",
        "• Strict 1:1 Unique Constraint on Payments.OrderId prevents duplicate payments.",
        "• Cross-service references (DrugId in OrderItems) validated via REST APIs.",
        "• Zero direct cross-database SQL joins (adhering to Microservices pattern).",
        "• Sensitive credentials hashed using PBKDF2 with SHA-256 and salt.",
        "• EF Core 8 Code-First migrations manage schema evolution cleanly."
    ]
    for ni, nt in enumerate(k_notes):
        ny = 755 + ni * 29
        draw.text((910, ny), nt, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "06_Database_Schema_Diagram.jpg")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_use_case_diagram()
    generate_sequence_diagram()
    generate_flow_diagram()
    generate_er_diagram()
    generate_database_schema_diagram()
    print("ALL 6 DIAGRAMS SUCCESSFULLY GENERATED AT OPTIMAL DOCUMENT LEGIBILITY!")
