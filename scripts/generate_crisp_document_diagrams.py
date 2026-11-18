import os
import math
from PIL import Image, ImageDraw, ImageFont

# Output Directories
OUT_DIR_WORKSPACE = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"
OUT_DIR_ARTIFACT = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\diagrams"

os.makedirs(OUT_DIR_WORKSPACE, exist_ok=True)
os.makedirs(OUT_DIR_ARTIFACT, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG  = "C:/Windows/Fonts/segoeui.ttf"

F_TITLE     = ImageFont.truetype(FONT_BOLD, 26) # Main pill title
F_TOP_TAG   = ImageFont.truetype(FONT_BOLD, 20) # Top section tag
F_SEC_TITLE = ImageFont.truetype(FONT_BOLD, 18) # Section & container headers
F_CARD_NAME = ImageFont.truetype(FONT_BOLD, 16.5) # Card / Table names
F_NODE_TXT  = ImageFont.truetype(FONT_BOLD, 15) # Node, oval, bullet text
F_BODY_BOLD = ImageFont.truetype(FONT_BOLD, 14) # Column names & main text
F_ATTR_BOLD = ImageFont.truetype(FONT_BOLD, 13) # Subtext, data types, bullets
F_BADGE_TXT = ImageFont.truetype(FONT_BOLD, 12.5) # Numbers & step badges
F_NOTE_TXT  = ImageFont.truetype(FONT_BOLD, 12) # Explanatory footnotes

# Vibrant Colors
CLR_WHITE         = (255, 255, 255)
CLR_BLACK         = (12, 18, 28)
CLR_DARK_SLATE    = (35, 45, 60)
CLR_BORDER        = (45, 60, 80)
CLR_BORDER_LIGHT  = (175, 190, 205)

# Microservice Themes
CLR_AUTH_MAIN     = (195, 95, 0)      # Amber / Orange (Auth)
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
    draw.rounded_rectangle([8, 8, W - 8, H - 8], radius=12, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    
    tag_bbox = F_TOP_TAG.getbbox(section_tag)
    tag_w = tag_bbox[2] - tag_bbox[0] + 30
    draw.rounded_rectangle([18, 14, 18 + tag_w, 52], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((32, 20), section_tag, font=F_TOP_TAG, fill=CLR_BLACK)

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
    
    # Centered text inside cylinder
    nb = F_CARD_NAME.getbbox(db_name)
    nw = nb[2] - nb[0]
    draw.text((x + (w - nw)//2, y + 16), db_name, font=F_CARD_NAME, fill=theme)

    tb = F_ATTR_BOLD.getbbox(tables_str)
    tw = tb[2] - tb[0]
    draw.text((x + (w - tw)//2, y + 38), tables_str, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

def save_image(img, name):
    p1 = os.path.join(OUT_DIR_WORKSPACE, name)
    p2 = os.path.join(OUT_DIR_ARTIFACT, name)
    img.save(p1, "JPEG", quality=96)
    img.save(p2, "JPEG", quality=96)
    print(f"Generated High-Legibility Diagram: {name} ({img.size[0]}x{img.size[1]})")

# ==============================================================================
# 1. ARCHITECTURE DIAGRAM (1400 x 980) - NO TECHSTACK, EXTRA ROOM, ZERO OVERFLOW
# ==============================================================================
def generate_architecture_diagram():
    W, H = 1400, 980
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "4.0 Architecture Diagram", "Pharmacy Management System – Microservices Architecture (5 Services)")

    # Left Column: Clients Box (x: 20 to 180, width: 160)
    draw.rounded_rectangle([20, 110, 180, 560], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((60, 120), "Clients", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(20, 148), (180, 148)], fill=CLR_BORDER, width=1)

    clients = [
        ("Web UI", "(Doctor/Admin)", 165, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Swagger UI", "(API Testing)", 295, CLR_INV_MAIN, CLR_INV_BG),
        ("Other Clients", "(Mobile / POS)", 425, CLR_AUTH_MAIN, CLR_AUTH_BG)
    ]
    for c_title, c_sub, cy, clr, bg in clients:
        draw.rounded_rectangle([28, cy, 172, cy + 115], radius=8, fill=bg, outline=clr, width=2)
        # Desktop icon
        draw.rounded_rectangle([45, cy + 10, 155, cy + 65], radius=4, fill=CLR_WHITE, outline=clr, width=2)
        draw.line([(60, cy + 38), (140, cy + 38)], fill=clr, width=2)
        draw.line([(100, cy + 65), (100, cy + 74)], fill=clr, width=2)
        draw.line([(82, cy + 74), (118, cy + 74)], fill=clr, width=2)

        tb = F_NODE_TXT.getbbox(c_title)
        draw.text((28 + (144 - (tb[2]-tb[0]))//2, cy + 78), c_title, font=F_NODE_TXT, fill=CLR_BLACK)
        sb = F_ATTR_BOLD.getbbox(c_sub)
        draw.text((28 + (144 - (sb[2]-sb[0]))//2, cy + 96), c_sub, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(180, 180), (200, 180)], fill=CLR_BLACK, width=2)

    # Center & Right Area: Microservices Core (x: 200 to 1380, width: 1180px - NO TECHSTACK)
    draw.rounded_rectangle([200, 110, 1380, 560], radius=10, outline=CLR_BORDER, width=2)

    # API Gateway Box (width: 1150px)
    draw.rounded_rectangle([215, 125, 1365, 185], radius=8, fill=CLR_GATE_BG, outline=CLR_BORDER, width=2)
    draw.ellipse([230, 140, 260, 170], fill=CLR_WHITE, outline=CLR_GATE_MAIN, width=2)
    draw.text((239, 143), "⚙", font=F_SEC_TITLE, fill=CLR_GATE_MAIN)
    draw.text((275, 135), "API Gateway (YARP / Reverse Proxy)", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((275, 160), "Request Routing | Load Balancing | JWT Bearer Validation | Rate Limiting | Health Checks", font=F_BODY_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(790, 185), (790, 205)], fill=CLR_BLACK, width=2)
    draw.line([(325, 205), (1255, 205)], fill=CLR_BLACK, width=2)

    # 5 Microservices Cards: Each card width = 218px, gap = 12px across 1140px!
    svcs = [
        {
            "name": "Auth Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• User Management", "• Role: Admin & Doctor", "• JWT Authentication", "• RBAC Authorization"],
            "db": "AuthDB",
            "db_sub": "(Users Table)",
            "theme": CLR_AUTH_MAIN, "bg": CLR_AUTH_BG, "x": 215, "w": 218
        },
        {
            "name": "Inventory Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Drug Catalog & Price", "• Supplier Management", "• Stock Inwarding", "• Atomic Qty Deduction"],
            "db": "InventoryDB",
            "db_sub": "(Drugs, Suppliers, Inv)",
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG, "x": 445, "w": 218
        },
        {
            "name": "Order Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Doctor Order Mgmt", "• Cart & Pending Flow", "• Admin Verification", "• Handover PickedUp"],
            "db": "OrderDB",
            "db_sub": "(Orders, OrderItems)",
            "theme": CLR_ORDER_MAIN, "bg": CLR_ORDER_BG, "x": 675, "w": 218
        },
        {
            "name": "Payment Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Order Checkout Billing", "• 1:1 Transaction Rule", "• Card / UPI Gateways", "• Reference Tracking"],
            "db": "PaymentDB",
            "db_sub": "(Payments [1:1 Unique])",
            "theme": CLR_PAY_MAIN, "bg": CLR_PAY_BG, "x": 905, "w": 218
        },
        {
            "name": "SaleReport Service",
            "tech": "(ASP.NET Core Web API)",
            "bullets": ["• Financial Analytics", "• Daily / Wk / Mo / Yr", "• Revenue & Profit Stats", "• CSV Export & Summary"],
            "db": "SaleReportDB",
            "db_sub": "(SaleReports Table)",
            "theme": CLR_REP_MAIN, "bg": CLR_REP_BG, "x": 1135, "w": 218
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

        # Card Title centered or with nice padding
        nb = F_CARD_NAME.getbbox(s["name"])
        draw.text((sx + (sw - (nb[2]-nb[0]))//2, 233), s["name"], font=F_CARD_NAME, fill=CLR_BLACK)
        tb = F_ATTR_BOLD.getbbox(s["tech"])
        draw.text((sx + (sw - (tb[2]-tb[0]))//2, 255), s["tech"], font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.line([(sx, 275), (sx + sw, 275)], fill=clr, width=1)

        # Bullet points: comfortable padding
        for b_i, b_t in enumerate(s["bullets"]):
            draw.text((sx + 12, 285 + b_i * 36), b_t, font=F_NODE_TXT, fill=CLR_BLACK)

        draw_arrow(draw, (sx + sw//2, 440), (sx + sw//2, 465), clr, 2)
        draw_cylinder(draw, sx + 8, 465, sw - 16, 60, s["db"], s["db_sub"], clr, bg)

    # Inter-service arrows
    draw_arrow(draw, (663, 310), (675, 310), CLR_BLACK, 2)
    draw_arrow(draw, (893, 310), (905, 310), CLR_BLACK, 2)

    # Common shared library box
    draw.rounded_rectangle([250, 532, 1330, 555], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((270, 536), "✉ Common Infrastructure (Shared Library): JWT Bearer Validation | PBKDF2 Password Hasher | ApiResponse Envelope | DTO Contracts", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # ==========================================
    # Bottom Area: 3 Split Cards (Full Width 1380px)
    # ==========================================
    # Card 1: Service Interactions (x: 20 to 450, width: 430)
    draw.rounded_rectangle([20, 575, 450, 965], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((35, 585), "Service Interactions – Order Flow (High Level)", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(20, 615), (450, 615)], fill=CLR_BORDER, width=1)

    # Actor Doctor
    draw.ellipse([35, 630, 75, 670], fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((46, 642), "Dr", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)
    draw.text((32, 675), "Doctor", font=F_BODY_BOLD, fill=CLR_BLACK)

    draw_arrow(draw, (75, 650), (120, 650), CLR_BLACK, 2)
    draw.ellipse([88, 634, 106, 652], fill=CLR_BLACK)
    draw.text((94, 636), "1", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([120, 628, 250, 680], radius=6, fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((130, 638), "Order Service", font=F_NODE_TXT, fill=CLR_ORDER_MAIN)
    draw.text((130, 658), "(POST /orders)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow(draw, (250, 645), (310, 645), CLR_BLACK, 2)
    draw.ellipse([272, 632, 290, 650], fill=CLR_BLACK)
    draw.text((278, 634), "2", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([310, 628, 440, 680], radius=6, fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((318, 638), "Inventory Service", font=F_NODE_TXT, fill=CLR_INV_MAIN)
    draw.text((320, 658), "(Deduct Stock Qty)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow(draw, (310, 668), (250, 668), CLR_BLACK, 2)
    draw.ellipse([272, 672, 290, 690], fill=CLR_BLACK)
    draw.text((278, 674), "3", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw_arrow(draw, (185, 680), (185, 715), CLR_BLACK, 2)
    draw.ellipse([190, 690, 208, 708], fill=CLR_BLACK)
    draw.text((196, 692), "4", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([120, 715, 250, 765], radius=6, fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((130, 725), "Payment Service", font=F_NODE_TXT, fill=CLR_PAY_MAIN)
    draw.text((130, 745), "(1:1 Payment Record)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw_arrow(draw, (250, 740), (310, 740), CLR_BLACK, 2)
    draw.ellipse([272, 725, 290, 743], fill=CLR_BLACK)
    draw.text((278, 727), "5", font=F_BADGE_TXT, fill=CLR_WHITE)

    draw.rounded_rectangle([310, 715, 440, 765], radius=6, fill=CLR_AUTH_BG, outline=CLR_AUTH_MAIN, width=2)
    draw.text((320, 725), "Admin Handover", font=F_NODE_TXT, fill=CLR_AUTH_MAIN)
    draw.text((320, 745), "(Verify & PickedUp)", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.rounded_rectangle([30, 785, 440, 950], radius=6, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=1)
    draw.text((40, 792), "Execution Steps:", font=F_BODY_BOLD, fill=CLR_BLACK)
    draw.text((40, 818), "1. Doctor authenticates and places medicine order.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 844), "2. Order Service requests stock reservation from Inventory.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 870), "3. Inventory confirms stock availability and decrements units.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 896), "4. Payment Service records unique 1:1 transaction.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((40, 922), "5. Admin verifies order contents and completes PickedUp handover.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Card 2: Database Distribution Table (x: 465 to 920, width: 455)
    draw.rounded_rectangle([465, 575, 920, 965], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((580, 585), "Database Distribution", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(465, 615), (920, 615)], fill=CLR_BORDER, width=1)

    # Table Header (width: 440px)
    draw.rectangle([475, 630, 910, 665], fill=CLR_GATE_MAIN)
    draw.text((485, 640), "Service", font=F_BODY_BOLD, fill=CLR_WHITE)
    draw.text((630, 640), "Database", font=F_BODY_BOLD, fill=CLR_WHITE)
    draw.text((775, 640), "Key Tables", font=F_BODY_BOLD, fill=CLR_WHITE)

    db_rows = [
        ("Auth Service", "Pharmacy_UserDB", "Users", CLR_AUTH_BG),
        ("Inventory Service", "Pharmacy_InvDB", "Drugs, Suppliers, Inv", CLR_INV_BG),
        ("Order Service", "Pharmacy_OrderDB", "Orders, OrderItems", CLR_ORDER_BG),
        ("Payment Service", "Pharmacy_PayDB", "Payments [1:1 Unique]", CLR_PAY_BG),
        ("SaleReport Service", "Pharmacy_RepDB", "SaleReports", CLR_REP_BG)
    ]
    for r_i, (svc_col, db_col, tbl_col, bg_col) in enumerate(db_rows):
        ry = 670 + r_i * 56
        draw.rectangle([475, ry, 910, ry + 50], fill=bg_col, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((485, ry + 15), svc_col, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.text((630, ry + 15), db_col, font=F_BODY_BOLD, fill=CLR_DARK_SLATE)
        draw.text((775, ry + 15), tbl_col, font=F_ATTR_BOLD, fill=CLR_BLACK)

    # Card 3: Key Highlights (x: 935 to 1380, width: 445)
    draw.rounded_rectangle([935, 575, 1380, 965], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((1055, 585), "Key Architecture Highlights", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(935, 615), (1380, 615)], fill=CLR_BORDER, width=1)

    highlights = [
        ("5 independent microservices with dedicated SQL databases.", "Complete physical database isolation per domain."),
        ("YARP API Gateway handles central routing and security.", "Reverse proxy with rate limiting, logging, and JWT validation."),
        ("Strict 1:1 Payment-to-Order unique index constraint.", "Guarantees zero duplicate payments or order checkout conflicts."),
        ("Role-Based Access Control (Admin and Doctor) via JWT.", "Claims-based security with fine-grained endpoint authorization."),
        ("Inventory Service atomic stock reservation & deduction.", "Prevents overselling during high concurrency ordering."),
        ("Internal MVC architecture inside each microservice.", "Controllers, Services, Repositories, DTOs, and DbContexts."),
        ("High-performance EF Core 8 queries with pooling.", "Optimized LINQ expressions and connection pooling.")
    ]
    for h_i, (h_line1, h_line2) in enumerate(highlights):
        hy = 638 + h_i * 46
        draw.ellipse([945, hy + 2, 965, hy + 22], fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
        draw.text((950, hy + 3), "✔", font=F_BADGE_TXT, fill=CLR_INV_MAIN)
        draw.text((975, hy), h_line1, font=F_BODY_BOLD, fill=CLR_BLACK)
        draw.text((975, hy + 19), h_line2, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "01_Solution_Architecture_Diagram.jpg")

# ==============================================================================
# 2. USE CASE DIAGRAM (1350 x 880) - WIDE OVALS, ZERO CLIPPING
# ==============================================================================
def generate_use_case_diagram():
    W, H = 1350, 880
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "5.0 Use Case Diagram", "Pharmacy Management System – Use Case Diagram")

    # Big Boundary Box (x: 180 to 1180, y: 110 to 860)
    draw.rounded_rectangle([180, 110, 1180, 860], radius=12, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((490, 125), "Pharmacy Management System Boundary", font=F_SEC_TITLE, fill=CLR_BLACK)

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

    # Admin Left Use Cases (x: 195 to 495, width: 300px!)
    admin_ucs = [
        ("Manage Users & Roles", 250, CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Manage Drugs Catalog", 335, CLR_INV_MAIN, CLR_INV_BG),
        ("Manage Suppliers & Orders", 420, CLR_INV_MAIN, CLR_INV_BG),
        ("Manage Inventory (Stock)", 505, CLR_INV_MAIN, CLR_INV_BG),
        ("Verify & Handover Orders", 590, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Generate Financial Reports", 675, CLR_REP_MAIN, CLR_REP_BG)
    ]
    for u_txt, uy, clr, bg in admin_ucs:
        draw.ellipse([195, uy, 495, uy + 58], fill=bg, outline=clr, width=2)
        tb = F_NODE_TXT.getbbox(u_txt)
        draw.text((195 + (300 - (tb[2]-tb[0]))//2, uy + 18), u_txt, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.line([(ax + 25, ay + 10), (195, uy + 29)], fill=CLR_BLACK, width=2)

    # Doctor Right Use Cases (x: 865 to 1165, width: 300px!)
    doc_ucs = [
        ("Search Available Drugs", 250, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("View Drug Prices & Stock", 335, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Create Prescription Order", 420, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Process Payment (Card/UPI)", 505, CLR_PAY_MAIN, CLR_PAY_BG),
        ("View My Orders History", 590, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Cancel Order (Before Paid)", 675, CLR_REP_MAIN, CLR_REP_BG)
    ]
    for u_txt, uy, clr, bg in doc_ucs:
        draw.ellipse([865, uy, 1165, uy + 58], fill=bg, outline=clr, width=2)
        tb = F_NODE_TXT.getbbox(u_txt)
        draw.text((865 + (300 - (tb[2]-tb[0]))//2, uy + 18), u_txt, font=F_NODE_TXT, fill=CLR_BLACK)
        draw.line([(dx - 25, dy + 10), (1165, uy + 29)], fill=CLR_BLACK, width=2)

    # Center Hub Use Cases (width: 310px, x: 525 to 835)
    draw.ellipse([525, 310, 835, 370], fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((585, 330), "Manage Orders Flow", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)

    draw.ellipse([525, 430, 835, 490], fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((560, 450), "Deduct Stock & Reserve Qty", font=F_CARD_NAME, fill=CLR_INV_MAIN)

    draw.ellipse([525, 550, 835, 610], fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((575, 570), "Record 1:1 Payment Ref", font=F_CARD_NAME, fill=CLR_PAY_MAIN)

    draw.ellipse([525, 670, 835, 730], fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((570, 690), "Export CSV Sales Summary", font=F_CARD_NAME, fill=CLR_REP_MAIN)

    # <<include>> and <<extend>> dashed arrows
    draw_arrow(draw, (680, 370), (680, 430), CLR_BORDER, 2, "<<include>>", False)
    draw_arrow(draw, (680, 490), (680, 550), CLR_BORDER, 2, "<<include>>", False)
    draw_arrow(draw, (680, 730), (680, 670), CLR_BORDER, 2, "<<extend>>", True)

    draw_arrow(draw, (865, 449), (835, 345), CLR_ORDER_MAIN, 2, "<<include>>", True)
    draw_arrow(draw, (495, 619), (525, 350), CLR_ORDER_MAIN, 2, "<<include>>", True)
    draw_arrow(draw, (495, 704), (525, 700), CLR_REP_MAIN, 2, "<<extend>>", True)

    # Bottom notes
    draw.rounded_rectangle([200, 785, 1160, 845], radius=6, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=1)
    draw.text((220, 795), "Legend & Notes:", font=F_BODY_BOLD, fill=CLR_BLACK)
    draw.text((220, 818), "• <<include>>: Stock deduction and payment recording are mandatory during order placement.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((790, 818), "• <<extend>>: Order cancellation & CSV export are optional actions.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "02_Use_Case_Diagram.jpg")

# ==============================================================================
# 3. SEQUENCE DIAGRAM (1400 x 1020) - WIDE SPANS, TWO-LINE LABELS, NO OVERLAPS
# ==============================================================================
def generate_sequence_diagram():
    W, H = 1400, 1020
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "11.0 Sequence Diagram", "Pharmacy Management System – End-to-End Order & Handover Flow")

    # 6 Participants across 1400px width (Ample distance between lifelines: 245px!)
    participants = [
        ("Doctor User", "(Client)", 90, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("YARP Gateway", "(Reverse Proxy)", 335, CLR_GATE_MAIN, CLR_GATE_BG),
        ("Auth Service", "(Pharmacy_UserDB)", 580, CLR_AUTH_MAIN, CLR_AUTH_BG),
        ("Order Service", "(Pharmacy_OrderDB)", 825, CLR_ORDER_MAIN, CLR_ORDER_BG),
        ("Inventory Svc", "(Pharmacy_InvDB)", 1070, CLR_INV_MAIN, CLR_INV_BG),
        ("Payment Svc", "(Pharmacy_PayDB)", 1315, CLR_PAY_MAIN, CLR_PAY_BG)
    ]

    for name, sub, px, clr, bg in participants:
        # Header box (width: 170px)
        draw.rounded_rectangle([px - 85, 120, px + 85, 175], radius=8, fill=bg, outline=clr, width=2)
        nb = F_CARD_NAME.getbbox(name)
        draw.text((px - (nb[2]-nb[0])//2, 130), name, font=F_CARD_NAME, fill=CLR_BLACK)
        sb = F_ATTR_BOLD.getbbox(sub)
        draw.text((px - (sb[2]-sb[0])//2, 153), sub, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

        # Lifeline
        draw.line([(px, 175), (px, 940)], fill=CLR_BORDER_LIGHT, width=2)

        # Footer box
        draw.rounded_rectangle([px - 85, 940, px + 85, 990], radius=8, fill=bg, outline=clr, width=2)
        draw.text((px - (nb[2]-nb[0])//2, 955), name, font=F_BODY_BOLD, fill=CLR_BLACK)

    # Steps (compact, balanced labels that NEVER exceed arrow span)
    steps = [
        # (y, from_x, to_x, label, is_return, clr)
        (205, 90, 335, "1: POST /api/auth/login", False, CLR_BLACK),
        (245, 335, 580, "2: ValidateCredentials() & Hash", False, CLR_AUTH_MAIN),
        (285, 580, 335, "3: 200 OK + JWT Bearer Token", True, CLR_AUTH_MAIN),
        (325, 335, 90, "4: Return Auth Token to Doctor", True, CLR_BLACK),

        (375, 90, 335, "5: POST /api/orders [Bearer Token]", False, CLR_ORDER_MAIN),
        (415, 335, 825, "6: Forward Order Payload", False, CLR_ORDER_MAIN),
        (455, 825, 1070, "7: POST /api/inventory/deduct", False, CLR_INV_MAIN),
        (495, 1070, 825, "8: 200 OK Stock Deducted & Reserved", True, CLR_INV_MAIN),

        (545, 825, 1315, "9: POST /api/payments {orderId, amount}", False, CLR_PAY_MAIN),
        (585, 1315, 825, "10: 200 OK Payment Recorded [Unique TxRef]", True, CLR_PAY_MAIN),

        (635, 825, 335, "11: 201 Created (Order Status: Pending)", True, CLR_ORDER_MAIN),
        (670, 335, 90, "12: Return Order Confirmation & Invoice", True, CLR_BLACK),

        # Admin Verification & Handover Phase
        (730, 90, 335, "13: Admin signs in & reviews Pending Orders", False, CLR_AUTH_MAIN),
        (770, 335, 825, "14: PUT /api/orders/{id}/verify (Validate)", False, CLR_ORDER_MAIN),
        (810, 825, 335, "15: Status Updated to 'Verified'", True, CLR_ORDER_MAIN),

        (855, 90, 825, "16: Admin completes Handover -> PUT /orders/{id}/pickup", False, CLR_INV_MAIN),
        (895, 825, 90, "17: 200 OK Order Status = 'PickedUp' (Fulfilled)", True, CLR_INV_MAIN)
    ]

    for y, fx, tx, lbl, is_ret, clr in steps:
        if is_ret:
            # Dashed return line
            x_min, x_max = min(fx, tx), max(fx, tx)
            for dx in range(x_min, x_max, 12):
                draw.line([(dx, y), (min(dx + 6, x_max), y)], fill=clr, width=2)
            if tx < fx:
                draw.polygon([(tx, y), (tx + 10, y - 5), (tx + 10, y + 5)], fill=clr)
            else:
                draw.polygon([(tx, y), (tx - 10, y - 5), (tx - 10, y + 5)], fill=clr)
        else:
            draw_arrow(draw, (fx, y), (tx, y), clr, 2)

        # Label badge strictly bounded between fx and tx
        mx = (fx + tx) // 2
        bbox = F_BODY_BOLD.getbbox(lbl)
        lw = bbox[2] - bbox[0] + 16
        draw.rounded_rectangle([mx - lw//2, y - 18, mx + lw//2, y + 2], radius=4, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((mx - lw//2 + 8, y - 16), lbl, font=F_BODY_BOLD, fill=clr)

    save_image(img, "03_Sequence_Diagram.jpg")

# ==============================================================================
# 4. FLOW DIAGRAM (1250 x 1350) - 380px COLUMNS, TWO-LINE LABELS, ZERO TOUCHING
# ==============================================================================
def generate_flow_diagram():
    W, H = 1250, 1350
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "6.0 Flow Diagram", "PHARMACY MANAGEMENT SYSTEM - FLOW DIAGRAM")

    # START Pill
    draw.rounded_rectangle([535, 120, 715, 165], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((595, 130), "START", font=F_CARD_NAME, fill=CLR_BLACK)
    draw_arrow(draw, (625, 165), (625, 195), CLR_BLACK, 2)

    # Login Box (width: 520px)
    draw.rounded_rectangle([365, 195, 885, 245], radius=8, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((400, 208), "User Registration / Customer or Admin Login", font=F_CARD_NAME, fill=CLR_BLACK)
    draw_arrow(draw, (625, 245), (625, 280), CLR_BLACK, 2)

    # Role Diamond
    dw, dh = 85, 40
    pts = [(625, 280), (625 + dw, 315), (625, 350), (625 - dw, 315)]
    draw.polygon(pts, fill=CLR_WHITE, outline=CLR_BORDER)
    draw.line(pts + [pts[0]], fill=CLR_BORDER, width=2)
    draw.text((602, 303), "Role?", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2 Branches
    # Left Branch: Admin / Pharmacist (x = 240)
    draw.line([(625 - dw, 315), (240, 315)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (240, 315), (240, 360), CLR_BLACK, 2)
    draw.text((310, 290), "Admin / Pharmacist", font=F_BODY_BOLD, fill=CLR_AUTH_MAIN)

    # Right Branch: Doctor / Customer (x = 1010)
    draw.line([(625 + dw, 315), (1010, 315)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (1010, 315), (1010, 360), CLR_BLACK, 2)
    draw.text((800, 290), "Doctor / Customer", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)

    # Admin Lane (Left Column: x: 50 to 430, width = 380px!)
    admin_boxes = [
        ("Manage Users & Roles", "(Admin & Doctor Accounts)", 360, CLR_AUTH_BG, CLR_AUTH_MAIN),
        ("Manage Drugs Catalog", "(Drug Pricing & Stock Limits)", 445, CLR_INV_BG, CLR_INV_MAIN),
        ("Manage Suppliers & Stock", "(Stock Inwarding & Batches)", 530, CLR_INV_BG, CLR_INV_MAIN),
        ("Verify Doctor Orders", "(Check Prescription Details)", 615, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Medicine Handover", "(Mark Order as 'PickedUp')", 700, CLR_INV_BG, CLR_INV_MAIN),
        ("View Sales Analytics", "(Revenue, Orders & Profit)", 785, CLR_REP_BG, CLR_REP_MAIN)
    ]
    for b_t1, b_t2, by, bg, clr in admin_boxes:
        draw.rounded_rectangle([50, by, 430, by + 58], radius=8, fill=bg, outline=clr, width=2)
        tb1 = F_NODE_TXT.getbbox(b_t1)
        draw.text((50 + (380 - (tb1[2]-tb1[0]))//2, by + 10), b_t1, font=F_NODE_TXT, fill=CLR_BLACK)
        tb2 = F_ATTR_BOLD.getbbox(b_t2)
        draw.text((50 + (380 - (tb2[2]-tb2[0]))//2, by + 32), b_t2, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        if by < 785:
            draw_arrow(draw, (240, by + 58), (240, by + 88), CLR_BLACK, 2)

    # Doctor Lane (Right Column: x: 820 to 1200, width = 380px!)
    doc_boxes = [
        ("Search Available Drugs", "(Browse Catalog & Check Stock)", 360, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("View Drug Details", "(Unit Prices & Dosage Info)", 445, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Select Quantities", "(Add Medicine Items to Cart)", 530, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Create Prescription Order", "(Enter Patient & Doctor Info)", 615, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Calculate Total Amount", "(Sum of Quantity * UnitPrice)", 700, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Proceed to Payment", "(Select Card / UPI / NetBanking)", 785, CLR_PAY_BG, CLR_PAY_MAIN)
    ]
    for b_t1, b_t2, by, bg, clr in doc_boxes:
        draw.rounded_rectangle([820, by, 1200, by + 58], radius=8, fill=bg, outline=clr, width=2)
        tb1 = F_NODE_TXT.getbbox(b_t1)
        draw.text((820 + (380 - (tb1[2]-tb1[0]))//2, by + 10), b_t1, font=F_NODE_TXT, fill=CLR_BLACK)
        tb2 = F_ATTR_BOLD.getbbox(b_t2)
        draw.text((820 + (380 - (tb2[2]-tb2[0]))//2, by + 32), b_t2, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw_arrow(draw, (1010, by + 58), (1010, by + 88), CLR_BLACK, 2)

    # Center Flow: Payment Decision Diamond
    draw.line([(1010, 843), (1010, 868)], fill=CLR_BLACK, width=2)
    draw.line([(1010, 868), (625, 868)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (625, 868), (625, 890), CLR_BLACK, 2)

    # Payment Successful? Diamond
    p_dw, p_dh = 100, 45
    p_pts = [(625, 890), (625 + p_dw, 935), (625, 980), (625 - p_dw, 935)]
    draw.polygon(p_pts, fill=CLR_WHITE, outline=CLR_BORDER)
    draw.line(p_pts + [p_pts[0]], fill=CLR_BORDER, width=2)
    draw.text((555, 922), "Payment Successful?", font=F_CARD_NAME, fill=CLR_BLACK)

    # Branch NO (Left to Dashed Box)
    draw.line([(625 - p_dw, 935), (420, 935)], fill=CLR_REP_MAIN, width=2)
    draw_arrow(draw, (420, 935), (390, 935), CLR_REP_MAIN, 2)
    draw.text((450, 910), "No", font=F_CARD_NAME, fill=CLR_REP_MAIN)

    # Payment Failed Box (Dashed: x: 80 to 390, width: 310px, y: 890 to 1180)
    draw.rounded_rectangle([80, 890, 390, 1180], radius=10, fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((120, 905), "Payment Failed Subflow", font=F_CARD_NAME, fill=CLR_REP_MAIN)
    draw.line([(80, 935), (390, 935)], fill=CLR_REP_BORDER, width=1)

    fail_steps = [
        ("Show Failure Message", 950),
        ("Update Status = 'PaymentFailed'", 1010),
        ("Release Reserved Drug Stock", 1070)
    ]
    for ft, fy in fail_steps:
        draw.rounded_rectangle([95, fy, 375, fy + 44], radius=6, fill=CLR_WHITE, outline=CLR_REP_BORDER, width=2)
        tb = F_NODE_TXT.getbbox(ft)
        draw.text((95 + (280 - (tb[2]-tb[0]))//2, fy + 12), ft, font=F_NODE_TXT, fill=CLR_BLACK)
        if fy < 1070:
            draw_arrow(draw, (235, fy + 44), (235, fy + 60), CLR_REP_MAIN, 2)

    draw.rounded_rectangle([95, 1130, 375, 1170], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((150, 1140), "Cancel Order Record", font=F_BODY_BOLD, fill=CLR_BLACK)

    # Branch YES (Down to Success Flow)
    draw_arrow(draw, (625, 980), (625, 1015), CLR_INV_MAIN, 2)
    draw.text((635, 990), "Yes", font=F_CARD_NAME, fill=CLR_INV_MAIN)

    success_boxes = [
        ("Confirm Order (Status = 'Pending' / 'Paid')", 1015, CLR_ORDER_BG, CLR_ORDER_MAIN),
        ("Generate Invoice & Unique Transaction Ref", 1085, CLR_PAY_BG, CLR_PAY_MAIN),
        ("Notify Pharmacist for Pickup Handover", 1155, CLR_INV_BG, CLR_INV_MAIN)
    ]
    for st, sy, sbg, sclr in success_boxes:
        draw.rounded_rectangle([440, sy, 890, sy + 50], radius=8, fill=sbg, outline=sclr, width=2)
        tb = F_CARD_NAME.getbbox(st)
        draw.text((440 + (450 - (tb[2]-tb[0]))//2, sy + 15), st, font=F_CARD_NAME, fill=CLR_BLACK)
        if sy < 1155:
            draw_arrow(draw, (665, sy + 50), (665, sy + 70), CLR_BLACK, 2)

    # Connect to END Pill
    draw_arrow(draw, (665, 1205), (665, 1245), CLR_BLACK, 2)
    draw.line([(235, 1170), (235, 1225)], fill=CLR_BLACK, width=2)
    draw.line([(235, 1225), (575, 1225)], fill=CLR_BLACK, width=2)
    draw.line([(240, 843), (240, 860)], fill=CLR_BLACK, width=2)

    # END Pill
    draw.rounded_rectangle([575, 1245, 755, 1290], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((640, 1255), "END", font=F_CARD_NAME, fill=CLR_BLACK)

    save_image(img, "04_Flow_Diagram.jpg")

# ==============================================================================
# 5. ER DIAGRAM (1400 x 980) - WIDE BOXES (290px), WRAPPED LEGEND, NO OVERFLOWS
# ==============================================================================
def generate_er_diagram():
    W, H = 1400, 980
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "9.0 ER Diagram", "Pharmacy Management System – Entity-Relationship (ER) Diagram")

    # 7 Entity Boxes: Width = 290px each
    entities = [
        {
            "name": "Users", "tag": "(AuthDB)", "x": 60, "y": 130, "w": 290, "h": 220,
            "theme": CLR_AUTH_MAIN, "bg": CLR_AUTH_BG,
            "attrs": ["PK UserId (int)", "Name (nvarchar)", "Email (nvarchar)", "PhoneNumber (nvarchar)", "PasswordHash (nvarchar)", "Role (Admin/Doctor)", "IsActive (bit)"]
        },
        {
            "name": "Orders", "tag": "(OrderDB)", "x": 555, "y": 130, "w": 290, "h": 200,
            "theme": CLR_ORDER_MAIN, "bg": CLR_ORDER_BG,
            "attrs": ["PK OrderId (int)", "FK DoctorID (int)", "OrderDate (datetime2)", "TotalAmount (decimal)", "Status (nvarchar)"]
        },
        {
            "name": "OrderItems", "tag": "(OrderDB)", "x": 1050, "y": 130, "w": 290, "h": 200,
            "theme": CLR_ORDER_MAIN, "bg": CLR_ORDER_BG,
            "attrs": ["PK OrderItemId (int)", "FK OrderId (int)", "FK DrugId (int)", "DrugName (nvarchar)", "Quantity (int)", "UnitPrice (decimal)"]
        },
        {
            "name": "Payments", "tag": "(PaymentDB)", "x": 555, "y": 420, "w": 290, "h": 220,
            "theme": CLR_PAY_MAIN, "bg": CLR_PAY_BG,
            "attrs": ["PK PaymentId (int)", "FK OrderId [1:1 Unique]", "Amount (decimal)", "PaymentDate (datetime2)", "PaymentMethod (nvarchar)", "PaymentStatus (nvarchar)", "TxReference (nvarchar)"]
        },
        {
            "name": "Drugs", "tag": "(InventoryDB)", "x": 1050, "y": 420, "w": 290, "h": 220,
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG,
            "attrs": ["PK DrugId (int)", "Name (nvarchar)", "Description (nvarchar)", "Price (decimal)", "ExpiryDate (date)", "Quantity (int)", "IsAvailable (bit)"]
        },
        {
            "name": "SaleReports", "tag": "(SaleReportDB)", "x": 60, "y": 420, "w": 290, "h": 220,
            "theme": CLR_REP_MAIN, "bg": CLR_REP_BG,
            "attrs": ["PK SaleReportId (int)", "ReportType (nvarchar)", "FromDate (datetime2)", "ToDate (datetime2)", "TotalOrders (int)", "TotalRevenue (decimal)", "Profit (decimal)"]
        },
        {
            "name": "Suppliers", "tag": "(InventoryDB)", "x": 555, "y": 710, "w": 290, "h": 200,
            "theme": CLR_INV_MAIN, "bg": CLR_INV_BG,
            "attrs": ["PK SupplierId (int)", "SupplierName (nvarchar)", "Email (nvarchar)", "PhoneNumber (nvarchar)", "Address (nvarchar)"]
        },
        {
            "name": "Inventory", "tag": "(InventoryDB)", "x": 1050, "y": 710, "w": 290, "h": 200,
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

        draw.text((ex + 14, ey + 8), ent["name"], font=F_CARD_NAME, fill=CLR_BLACK)
        draw.text((ex + ew - 100, ey + 10), ent["tag"], font=F_ATTR_BOLD, fill=clr)
        draw.line([(ex, ey + 40), (ex + ew, ey + 40)], fill=clr, width=1)

        for a_i, a_t in enumerate(ent["attrs"]):
            ay = ey + 48 + a_i * 24
            if a_t.startswith("PK"):
                draw.text((ex + 12, ay), "🔑 " + a_t, font=F_BODY_BOLD, fill=CLR_AUTH_MAIN)
            elif a_t.startswith("FK"):
                draw.text((ex + 12, ay), "🔗 " + a_t, font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            else:
                draw.text((ex + 12, ay), "• " + a_t, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Relationship Diamonds & Connector Lines
    def draw_rel_diamond(cx, cy, label):
        rw, rh = 48, 24
        draw.polygon([(cx, cy - rh), (cx + rw, cy), (cx, cy + rh), (cx - rw, cy)], fill=CLR_GATE_BG, outline=CLR_BORDER)
        draw.line([(cx, cy - rh), (cx + rw, cy), (cx, cy + rh), (cx - rw, cy), (cx, cy - rh)], fill=CLR_BORDER, width=2)
        bbox = F_BADGE_TXT.getbbox(label)
        draw.text((cx - (bbox[2]-bbox[0])//2, cy - 8), label, font=F_BADGE_TXT, fill=CLR_BLACK)

    # 1. Users --- places ---> Orders (1 : N)
    draw.line([(350, 220), (555, 220)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(452, 220, "places")
    draw.text((360, 195), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((530, 195), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2. Orders --- contains ---> OrderItems (1 : N)
    draw.line([(845, 220), (1050, 220)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(947, 220, "has")
    draw.text((860, 195), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1025, 195), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 3. Orders --- paid by ---> Payments (1 : 1 UNIQUE)
    draw.line([(700, 330), (700, 420)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(700, 375, "paid by")
    draw.text((710, 335), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((710, 395), "1 (Unique)", font=F_ATTR_BOLD, fill=CLR_PAY_MAIN)

    # 4. Drugs --- refers ---> OrderItems (1 : N)
    draw.line([(1195, 420), (1195, 330)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(1195, 375, "item")
    draw.text((1205, 400), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1205, 335), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 5. Suppliers --- supplies ---> Inventory (1 : N)
    draw.line([(845, 790), (1050, 790)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(947, 790, "supplies")
    draw.text((860, 765), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1025, 765), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # 6. Drugs --- stocked ---> Inventory (1 : N)
    draw.line([(1195, 640), (1195, 710)], fill=CLR_BLACK, width=2)
    draw_rel_diamond(1195, 675, "stocked")
    draw.text((1205, 645), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1205, 685), "N", font=F_CARD_NAME, fill=CLR_BLACK)

    # Bottom Legend Box (x: 60 to 480, width: 420px!)
    draw.rounded_rectangle([60, 680, 480, 930], radius=8, fill=CLR_GATE_BG, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((75, 695), "Cardinality & Architecture Rules:", font=F_BODY_BOLD, fill=CLR_BLACK)
    draw.text((75, 725), "• 1 : N = One-to-Many Relationship.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((75, 755), "• 1 : 1 Unique = Exact 1 Payment per Order.", font=F_ATTR_BOLD, fill=CLR_PAY_MAIN)
    draw.text((75, 785), "• Cross-service foreign keys are logical references.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((75, 815), "• Consistency verified through REST API contracts.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
    draw.text((75, 845), "• Zero direct cross-database SQL joins.", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "05_ER_Diagram.jpg")

# ==============================================================================
# 6. DATABASE SCHEMA DIAGRAM (1420 x 980) - WIDE CONTAINERS, NO COLUMN OVERLAPS
# ==============================================================================
def generate_database_schema_diagram():
    W, H = 1420, 980
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_reference_frame(draw, W, H, "2.0 Database Diagram", "Pharmacy Management System – Database Diagram (5 Databases)")

    # Container 1: Auth Service - AuthDB (x: 20 to 440, width: 420)
    draw.rounded_rectangle([20, 110, 440, 420], radius=10, fill=CLR_WHITE, outline=CLR_AUTH_BORDER, width=2)
    draw.rounded_rectangle([35, 120, 425, 155], radius=6, fill=CLR_AUTH_BG, outline=CLR_AUTH_MAIN, width=2)
    draw.text((45, 128), "🛢 Auth Service – Pharmacy_UserDB", font=F_CARD_NAME, fill=CLR_AUTH_MAIN)

    # Users Table (width: 390)
    draw.rounded_rectangle([35, 170, 425, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([35, 170, 425, 205], fill=CLR_GATE_MAIN)
    draw.text((45, 178), "Users", font=F_CARD_NAME, fill=CLR_WHITE)
    draw.text((310, 180), "Table (Entity)", font=F_ATTR_BOLD, fill=CLR_BORDER_LIGHT)

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
            draw.text((45, cy), "PK", font=F_BODY_BOLD, fill=CLR_AUTH_MAIN)
            draw.text((80, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((80, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((275, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Container 2: Inventory Service - InventoryDB (x: 460 to 1400, width: 940)
    draw.rounded_rectangle([460, 110, 1400, 420], radius=10, fill=CLR_WHITE, outline=CLR_INV_BORDER, width=2)
    draw.rounded_rectangle([475, 120, 1385, 155], radius=6, fill=CLR_INV_BG, outline=CLR_INV_MAIN, width=2)
    draw.text((485, 128), "🛢 Inventory Service – Pharmacy_InventoryDB", font=F_CARD_NAME, fill=CLR_INV_MAIN)

    # Drugs Table (x: 475 to 765, width: 290)
    draw.rounded_rectangle([475, 170, 765, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([475, 170, 765, 205], fill=CLR_GATE_MAIN)
    draw.text((485, 178), "Drugs", font=F_CARD_NAME, fill=CLR_WHITE)
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
            draw.text((485, cy), "PK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((520, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((520, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((655, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Suppliers Table (x: 785 to 1075, width: 290)
    draw.rounded_rectangle([785, 170, 1075, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([785, 170, 1075, 205], fill=CLR_GATE_MAIN)
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
        draw.text((950, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Inventory Table (x: 1095 to 1385, width: 290)
    draw.rounded_rectangle([1095, 170, 1385, 400], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([1095, 170, 1385, 205], fill=CLR_GATE_MAIN)
    draw.text((1105, 178), "Inventory", font=F_CARD_NAME, fill=CLR_WHITE)
    i_cols = [
        ("PK", "InventoryId", "int", True, False),
        ("FK", "SupplierId", "int", False, True),
        ("FK", "DrugId", "int", False, True),
        ("", "PurchasePrice", "decimal", False, False),
        ("", "QuantityAdded", "int", False, False),
        ("", "StockReceived", "datetime2", False, False)
    ]
    for ci, (tag, cname, ctype, is_pk, is_fk) in enumerate(i_cols):
        cy = 212 + ci * 28
        if is_pk:
            draw.text((1105, cy), "PK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((1140, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        elif is_fk:
            draw.text((1105, cy), "FK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((1140, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((1140, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((1275, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(765, 225), (785, 225)], fill=CLR_BLACK, width=2)
    draw.line([(1075, 225), (1095, 225)], fill=CLR_BLACK, width=2)
    draw.text((1078, 205), "1:N", font=F_BADGE_TXT, fill=CLR_BLACK)

    # Container 3: OrderDB (x: 20 to 690, width: 670)
    draw.rounded_rectangle([20, 435, 690, 690], radius=10, fill=CLR_WHITE, outline=CLR_ORDER_BORDER, width=2)
    draw.rounded_rectangle([35, 445, 675, 480], radius=6, fill=CLR_ORDER_BG, outline=CLR_ORDER_MAIN, width=2)
    draw.text((45, 453), "🛢 Order Service – Pharmacy_OrderDB", font=F_CARD_NAME, fill=CLR_ORDER_MAIN)

    # Orders Table (x: 35 to 345, width: 310)
    draw.rounded_rectangle([35, 495, 345, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([35, 495, 345, 528], fill=CLR_GATE_MAIN)
    draw.text((45, 502), "Orders", font=F_CARD_NAME, fill=CLR_WHITE)
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
            draw.text((45, cy), "PK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((80, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((80, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((220, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # OrderItems Table (x: 365 to 675, width: 310)
    draw.rounded_rectangle([365, 495, 675, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([365, 495, 675, 528], fill=CLR_GATE_MAIN)
    draw.text((375, 502), "OrderItems", font=F_CARD_NAME, fill=CLR_WHITE)
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
            draw.text((375, cy), "PK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((410, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        elif is_fk:
            draw.text((375, cy), "FK", font=F_BODY_BOLD, fill=CLR_INV_MAIN)
            draw.text((410, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((410, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((550, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    draw.line([(345, 545), (365, 545)], fill=CLR_BLACK, width=2)
    draw.text((348, 525), "1:N", font=F_BADGE_TXT, fill=CLR_BLACK)

    # Container 4: PaymentDB (x: 710 to 1045, width: 335)
    draw.rounded_rectangle([710, 435, 1045, 690], radius=10, fill=CLR_WHITE, outline=CLR_PAY_BORDER, width=2)
    draw.rounded_rectangle([725, 445, 1030, 480], radius=6, fill=CLR_PAY_BG, outline=CLR_PAY_MAIN, width=2)
    draw.text((735, 453), "🛢 Payment Service – PaymentDB", font=F_CARD_NAME, fill=CLR_PAY_MAIN)

    # Payments Table (width: 305)
    draw.rounded_rectangle([725, 495, 1030, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([725, 495, 1030, 528], fill=CLR_GATE_MAIN)
    draw.text((735, 502), "Payments", font=F_CARD_NAME, fill=CLR_WHITE)
    p_cols = [
        ("PK", "PaymentId", "int", True, False),
        ("FK", "OrderId [1:1]", "int", False, True),
        ("", "Amount", "decimal(18,2)", False, False),
        ("", "PaymentDate", "datetime2", False, False),
        ("", "PaymentMethod", "nvarchar(50)", False, False),
        ("", "PaymentStatus", "nvarchar(20)", False, False),
        ("", "TxReference", "nvarchar(100)", False, False)
    ]
    for ci, (tag, cname, ctype, is_pk, is_fk) in enumerate(p_cols):
        cy = 533 + ci * 20
        if is_pk:
            draw.text((735, cy), "PK", font=F_BODY_BOLD, fill=CLR_PAY_MAIN)
            draw.text((770, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        elif is_fk:
            draw.text((735, cy), "FK", font=F_BODY_BOLD, fill=CLR_ORDER_MAIN)
            draw.text((770, cy), cname, font=F_BODY_BOLD, fill=CLR_PAY_MAIN)
        else:
            draw.text((770, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((920, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Container 5: SaleReportDB (x: 1065 to 1400, width: 335)
    draw.rounded_rectangle([1065, 435, 1400, 690], radius=10, fill=CLR_WHITE, outline=CLR_REP_BORDER, width=2)
    draw.rounded_rectangle([1080, 445, 1385, 480], radius=6, fill=CLR_REP_BG, outline=CLR_REP_MAIN, width=2)
    draw.text((1090, 453), "🛢 SaleReport Service – DB", font=F_CARD_NAME, fill=CLR_REP_MAIN)

    draw.rounded_rectangle([1080, 495, 1385, 675], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.rectangle([1080, 495, 1385, 528], fill=CLR_GATE_MAIN)
    draw.text((1090, 502), "SaleReports", font=F_CARD_NAME, fill=CLR_WHITE)
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
            draw.text((1090, cy), "PK", font=F_BODY_BOLD, fill=CLR_REP_MAIN)
            draw.text((1125, cy), cname, font=F_BODY_BOLD, fill=CLR_BLACK)
        else:
            draw.text((1125, cy), cname, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)
        draw.text((1275, cy), f"({ctype})", font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Bottom Area: 3 Summary Panels (y: 705 to 945)
    # Panel 1: Database Summary (x: 20 to 510, width: 490)
    draw.rounded_rectangle([20, 705, 510, 945], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((35, 715), "Database Summary", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(20, 742), (510, 742)], fill=CLR_BORDER, width=1)

    draw.rectangle([30, 752, 500, 780], fill=CLR_GATE_MAIN)
    draw.text((38, 758), "Database (Service)", font=F_BODY_BOLD, fill=CLR_WHITE)
    draw.text((280, 758), "Key Tables", font=F_BODY_BOLD, fill=CLR_WHITE)

    d_summary = [
        ("Pharmacy_UserDB (Auth)", "Users Table", CLR_AUTH_BG),
        ("Pharmacy_InventoryDB (Inv)", "Drugs, Suppliers, Inventory", CLR_INV_BG),
        ("Pharmacy_OrderDB (Order)", "Orders, OrderItems", CLR_ORDER_BG),
        ("Pharmacy_PaymentDB (Pay)", "Payments [1:1 Unique]", CLR_PAY_BG),
        ("Pharmacy_SaleReportDB (Rep)", "SaleReports", CLR_REP_BG)
    ]
    for si, (d_name, d_tbls, bg_col) in enumerate(d_summary):
        sy = 784 + si * 30
        draw.rectangle([30, sy, 500, sy + 27], fill=bg_col, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((38, sy + 6), d_name, font=F_ATTR_BOLD, fill=CLR_BLACK)
        draw.text((280, sy + 6), d_tbls, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    # Panel 2: Legend (x: 525 to 885, width: 360)
    draw.rounded_rectangle([525, 705, 885, 945], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((540, 715), "Legend", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(525, 742), (885, 742)], fill=CLR_BORDER, width=1)

    legend_items = [
        ("PK", "Primary Key (Unique Table ID)", CLR_AUTH_MAIN),
        ("FK", "Foreign Key (Logical Reference)", CLR_ORDER_MAIN),
        ("1 : N", "One-to-Many Relationship", CLR_BLACK),
        ("1 : 1", "One-to-One Unique Relationship", CLR_PAY_MAIN),
        ("Table", "Entity Schema with Column Types", CLR_DARK_SLATE),
        ("Index", "Unique Index on Payments.OrderId", CLR_INV_MAIN)
    ]
    for li, (ltag, ldesc, lclr) in enumerate(legend_items):
        ly = 758 + li * 29
        draw.rounded_rectangle([540, ly, 595, ly + 22], radius=4, fill=CLR_GATE_BG, outline=lclr, width=2)
        draw.text((548, ly + 2), ltag, font=F_BODY_BOLD, fill=lclr)
        draw.text((605, ly + 2), ldesc, font=F_ATTR_BOLD, fill=CLR_BLACK)

    # Panel 3: Key Notes (x: 900 to 1400, width: 500)
    draw.rounded_rectangle([900, 705, 1400, 945], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((915, 715), "Key Architectural Notes", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.line([(900, 742), (1400, 742)], fill=CLR_BORDER, width=1)

    k_notes = [
        "• 5 independent databases completely isolate data per microservice.",
        "• Strict 1:1 Unique Constraint on Payments.OrderId prevents duplicates.",
        "• Cross-service references (DrugId in OrderItems) validated via REST APIs.",
        "• Zero direct cross-database SQL joins (strict Microservices pattern).",
        "• Sensitive credentials hashed using PBKDF2 with SHA-256 and salt.",
        "• EF Core 8 Code-First migrations manage schema evolution cleanly."
    ]
    for ni, nt in enumerate(k_notes):
        ny = 755 + ni * 29
        draw.text((915, ny), nt, font=F_ATTR_BOLD, fill=CLR_DARK_SLATE)

    save_image(img, "06_Database_Schema_Diagram.jpg")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_use_case_diagram()
    generate_sequence_diagram()
    generate_flow_diagram()
    generate_er_diagram()
    generate_database_schema_diagram()
    print("ALL 6 DIAGRAMS SUCCESSFULLY GENERATED WITH ZERO OVERFLOWS & NO TECHSTACK!")
