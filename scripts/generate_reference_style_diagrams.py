import os
import math
from PIL import Image, ImageDraw, ImageFont

# Output Directories
OUT_DIR_WORKSPACE = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"
OUT_DIR_ARTIFACT = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\diagrams"

os.makedirs(OUT_DIR_WORKSPACE, exist_ok=True)
os.makedirs(OUT_DIR_ARTIFACT, exist_ok=True)

# Fonts
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG  = "C:/Windows/Fonts/segoeui.ttf"

F_TITLE     = ImageFont.truetype(FONT_BOLD, 24) # Main diagram header
F_SEC_TITLE = ImageFont.truetype(FONT_BOLD, 18) # Subheadings & box titles
F_CARD_NAME = ImageFont.truetype(FONT_BOLD, 16) # Class / Table / Entity name
F_NODE_TXT  = ImageFont.truetype(FONT_BOLD, 14.5) # Node, oval, bullet text
F_BODY_BOLD = ImageFont.truetype(FONT_BOLD, 13.5) # Column names, methods
F_ATTR_BOLD = ImageFont.truetype(FONT_BOLD, 12.5) # Types, subtext
F_BADGE_TXT = ImageFont.truetype(FONT_BOLD, 12) # Labels & connectors

# Palette: Clean, Mostly Black & White / Grayscale with subtle professional slate accents
CLR_WHITE         = (255, 255, 255)
CLR_BLACK         = (20, 20, 20)
CLR_DARK_GRAY     = (50, 50, 50)
CLR_MID_GRAY      = (100, 100, 100)
CLR_LIGHT_GRAY    = (230, 230, 230)
CLR_BG_TINT       = (248, 249, 250)
CLR_BORDER        = (40, 40, 40)
CLR_BORDER_LIGHT  = (180, 180, 180)

# Subtle Tints for Reference 1 (Architecture) and Reference 5 (ER Boxes)
CLR_GATE_BG       = (254, 243, 235)  # Very light warm tint for Gateway
CLR_GATE_BORDER   = (217, 119, 6)
CLR_SVC_BG        = (240, 244, 248)  # Soft cool gray-blue for Services
CLR_SVC_BORDER    = (71, 85, 105)
CLR_TABLE_HDR     = (30, 41, 59)     # Dark slate for Table Headers

def draw_top_title(draw, W, section_text):
    tb = F_TITLE.getbbox(section_text)
    tw = tb[2] - tb[0]
    draw.text((25, 20), section_text, font=F_TITLE, fill=CLR_BLACK)
    draw.line([(25, 55), (W - 25, 55)], fill=CLR_BORDER_LIGHT, width=1)

def draw_arrow(draw, start, end, color=CLR_BLACK, width=2, label=None, label_above=True, is_dashed=False):
    x1, y1 = start
    x2, y2 = end
    if is_dashed:
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist > 0:
            steps = int(dist // 10)
            dx = (x2 - x1) / dist * 6
            dy = (y2 - y1) / dist * 6
            for i in range(0, steps, 2):
                sx = x1 + (x2 - x1) * (i / steps)
                sy = y1 + (y2 - y1) * (i / steps)
                draw.line([(sx, sy), (sx + dx, sy + dy)], fill=color, width=width)
    else:
        draw.line([start, end], fill=color, width=width)
    
    # Arrow head
    angle = math.atan2(y2 - y1, x2 - x1)
    hlen = 9
    p1 = (x2 - hlen * math.cos(angle - math.pi / 6), y2 - hlen * math.sin(angle - math.pi / 6))
    p2 = (x2 - hlen * math.cos(angle + math.pi / 6), y2 - hlen * math.sin(angle + math.pi / 6))
    draw.polygon([(x2, y2), p1, p2], fill=color)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ly = my - 16 if label_above else my + 6
        bbox = F_BADGE_TXT.getbbox(label)
        lw = bbox[2] - bbox[0] + 12
        draw.rounded_rectangle([mx - lw//2, ly - 2, mx + lw//2, ly + 16], radius=3, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=1)
        draw.text((mx - lw//2 + 6, ly), label, font=F_BADGE_TXT, fill=color)

def draw_cylinder(draw, x, y, w, h, db_name, theme=CLR_BORDER, bg=CLR_WHITE):
    cap = 14
    draw.rectangle([x, y + cap//2, x + w, y + h - cap//2], fill=bg, outline=theme, width=2)
    draw.ellipse([x, y + h - cap, x + w, y + h], fill=bg, outline=theme, width=2)
    draw.arc([x, y + h//2 - cap//2, x + w, y + h//2 + cap//2], 0, 180, fill=theme, width=1)
    draw.ellipse([x, y, x + w, y + cap], fill=bg, outline=theme, width=2)
    
    nb = F_CARD_NAME.getbbox(db_name)
    nw = nb[2] - nb[0]
    draw.text((x + (w - nw)//2, y + (h - 18)//2), db_name, font=F_CARD_NAME, fill=CLR_BLACK)

def save_image(img, name):
    p1 = os.path.join(OUT_DIR_WORKSPACE, name)
    p2 = os.path.join(OUT_DIR_ARTIFACT, name)
    img.save(p1, "JPEG", quality=96)
    img.save(p2, "JPEG", quality=96)
    print(f"Generated Reference-Style Diagram: {name} ({img.size[0]}x{img.size[1]})")

# ==============================================================================
# 1. ARCHITECTURE DIAGRAM (Matching Reference 1: Presentation, App, Data Layers)
# ==============================================================================
def generate_architecture_diagram():
    W, H = 1350, 880
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_top_title(draw, W, "8.0 Architecture Diagram")

    # Layer Vertical Dividing Dotted Lines
    # Presentation Layer: x: 30 to 240
    # Application Layer:  x: 270 to 920
    # Data Layer:         x: 950 to 1320
    for y in range(70, H - 70, 12):
        draw.line([(255, y), (255, y + 6)], fill=CLR_BORDER_LIGHT, width=2)
        draw.line([(935, y), (935, y + 6)], fill=CLR_BORDER_LIGHT, width=2)

    # Layer Footers
    draw.text((80, H - 45), "Presentation Layer", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((540, H - 45), "Application Layer", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((1080, H - 45), "Data Layer", font=F_SEC_TITLE, fill=CLR_BLACK)

    # Presentation Layer: Client Box (x: 40 to 210, y: 360 to 450)
    draw.rounded_rectangle([40, 360, 210, 460], radius=8, fill=CLR_SVC_BG, outline=CLR_SVC_BORDER, width=2)
    # User Icon
    draw.ellipse([70, 385, 105, 420], fill=CLR_WHITE, outline=CLR_SVC_BORDER, width=2) # head
    draw.arc([60, 415, 115, 455], 180, 360, fill=CLR_SVC_BORDER, width=2)               # shoulders
    draw.text((120, 395), "Client", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((120, 422), "(Swagger UI)", font=F_ATTR_BOLD, fill=CLR_MID_GRAY)

    # Arrow: Client -> API Gateway
    draw_arrow(draw, (210, 410), (300, 410), CLR_BLACK, 2)

    # Application Layer: API Gateway Box (x: 300 to 450, y: 350 to 470)
    draw.rounded_rectangle([300, 350, 450, 470], radius=10, fill=CLR_GATE_BG, outline=CLR_GATE_BORDER, width=2)
    # Gateway icon
    draw.rectangle([325, 375, 355, 405], fill=CLR_WHITE, outline=CLR_GATE_BORDER, width=2)
    draw.line([(340, 375), (340, 405)], fill=CLR_GATE_BORDER, width=2)
    draw.text((365, 378), "API Gateway", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((365, 402), "(YARP Routing)", font=F_ATTR_BOLD, fill=CLR_MID_GRAY)
    draw.text((320, 435), "Reverse Proxy & Security", font=F_ATTR_BOLD, fill=CLR_DARK_GRAY)

    # 5 Microservices Dashed Containers & Data Layer Cylinders
    # Y positions for the 5 services:
    # 1. User Microservice      y: 80 to 210
    # 2. Inventory Microservice y: 230 to 360
    # 3. Order Microservice     y: 380 to 510
    # 4. Payment Microservice   y: 530 to 660
    # 5. SaleReport Microservice y: 680 to 810
    svcs = [
        ("User Microservice", "Auth Service", "User DB", 80),
        ("Inventory Microservice", "Inventory Service", "Inventory DB", 230),
        ("Order Microservice", "Order Service", "Order DB", 380),
        ("Payment Microservice", "Payment Service", "Payment DB", 530),
        ("SaleReport Microservice", "SaleReport Service", "SaleReport DB", 680)
    ]

    for ms_tag, svc_name, db_name, sy in svcs:
        cy = sy + 65 # center y

        # Dashed Microservice Container (x: 520 to 890, y: sy to sy + 130)
        draw.rounded_rectangle([520, sy, 890, sy + 130], radius=8, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=2)
        # Dashed effect on border
        draw.text((535, sy + 8), f"• {ms_tag}", font=F_BADGE_TXT, fill=CLR_MID_GRAY)

        # Service Box inside container (x: 545 to 740, y: sy + 35 to sy + 110)
        draw.rounded_rectangle([545, sy + 35, 740, sy + 110], radius=6, fill=CLR_SVC_BG, outline=CLR_SVC_BORDER, width=2)
        snb = F_CARD_NAME.getbbox(svc_name)
        draw.text((545 + (195 - (snb[2]-snb[0]))//2, sy + 48), svc_name, font=F_CARD_NAME, fill=CLR_BLACK)
        draw.text((545 + (195 - F_ATTR_BOLD.getbbox("(Web API)")[2])//2, sy + 75), "(Web API)", font=F_ATTR_BOLD, fill=CLR_MID_GRAY)

        # Arrow from Gateway to Service
        # Gateway center is at (450, 410). Service entry is at (545, cy).
        draw.line([(450, 410), (485, 410)], fill=CLR_BLACK, width=2)
        draw.line([(485, 410), (485, cy)], fill=CLR_BLACK, width=2)
        draw_arrow(draw, (485, cy), (545, cy), CLR_BLACK, 2)

        # Arrow from Service to DB
        draw_arrow(draw, (740, cy), (1010, cy), CLR_BLACK, 2)

        # Data Layer Cylinder (x: 1010 to 1260, y: sy + 30 to sy + 110)
        draw_cylinder(draw, 1010, sy + 25, 250, 85, db_name, CLR_BORDER, CLR_WHITE)

    save_image(img, "01_Solution_Architecture_Diagram.jpg")

# ==============================================================================
# 2. USE CASE DIAGRAM (Matching Reference 4: System Box, 2 Actors, Clean Ovals)
# ==============================================================================
def generate_use_case_diagram():
    W, H = 1350, 880
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_top_title(draw, W, "7.0 Use Case Diagram")

    # Big System Boundary Box (x: 210 to 1140, y: 70 to 850)
    draw.rounded_rectangle([210, 70, 1140, 850], radius=10, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((500, 85), "Pharmacy Management System", font=F_SEC_TITLE, fill=CLR_BLACK)

    # Actor 1: Doctor (Customer) - Left (x = 100, y = 430)
    ax, ay = 100, 430
    draw.ellipse([ax - 22, ay - 60, ax + 22, ay - 16], outline=CLR_BLACK, width=2) # Head
    draw.line([(ax, ay - 16), (ax, ay + 45)], fill=CLR_BLACK, width=2)            # Spine
    draw.line([(ax - 35, ay + 10), (ax + 35, ay + 10)], fill=CLR_BLACK, width=2)  # Arms
    draw.line([(ax, ay + 45), (ax - 25, ay + 105)], fill=CLR_BLACK, width=2)      # Left leg
    draw.line([(ax, ay + 45), (ax + 25, ay + 105)], fill=CLR_BLACK, width=2)      # Right leg
    draw.text((ax - 25, ay + 115), "Doctor", font=F_CARD_NAME, fill=CLR_BLACK)

    # Actor 2: Admin (Pharmacist) - Right (x = 1250, y = 430)
    bx, by = 1250, 430
    draw.ellipse([bx - 22, by - 60, bx + 22, by - 16], outline=CLR_BLACK, width=2)
    draw.line([(bx, by - 16), (bx, by + 45)], fill=CLR_BLACK, width=2)
    draw.line([(bx - 35, by + 10), (bx + 35, by + 10)], fill=CLR_BLACK, width=2)
    draw.line([(bx, by + 45), (bx - 25, by + 105)], fill=CLR_BLACK, width=2)
    draw.line([(bx, by + 45), (bx + 25, by + 105)], fill=CLR_BLACK, width=2)
    draw.text((bx - 25, by + 115), "Admin", font=F_CARD_NAME, fill=CLR_BLACK)

    # Doctor Use Cases (Left Side Ovals: x: 240 to 520, width: 280)
    doctor_ucs = [
        ("Register / Login", 130),
        ("Search Available Drugs", 215),
        ("View Drug Details", 300),
        ("Add Drugs to Cart", 385),
        ("Place Medicine Order", 470),
        ("Track Order Status", 555),
        ("Select Payment Method", 640),
        ("Simulate Payment & Checkout", 725)
    ]
    for u_txt, uy in doctor_ucs:
        draw.ellipse([240, uy, 530, uy + 55], fill=CLR_WHITE, outline=CLR_BORDER, width=2)
        tb = F_NODE_TXT.getbbox(u_txt)
        draw.text((240 + (290 - (tb[2]-tb[0]))//2, uy + 18), u_txt, font=F_NODE_TXT, fill=CLR_BLACK)
        # Connector line to Doctor
        draw.line([(ax + 25, ay + 10), (240, uy + 27)], fill=CLR_MID_GRAY, width=1)

    # Admin Use Cases (Right Side Ovals: x: 820 to 1110, width: 290)
    admin_ucs = [
        ("Register / Login", 130),
        ("Add / Edit / Delete Drugs", 215),
        ("View & Manage Suppliers", 300),
        ("View Doctor Orders", 385),
        ("Verify Valid Orders", 470),
        ("Add Order to PickedUp Section", 555),
        ("View Sales Analytics", 640),
        ("Download / Print Sales Report", 725)
    ]
    for u_txt, uy in admin_ucs:
        draw.ellipse([820, uy, 1110, uy + 55], fill=CLR_WHITE, outline=CLR_BORDER, width=2)
        tb = F_NODE_TXT.getbbox(u_txt)
        draw.text((820 + (290 - (tb[2]-tb[0]))//2, uy + 18), u_txt, font=F_NODE_TXT, fill=CLR_BLACK)
        # Connector line to Admin
        draw.line([(bx - 25, by + 10), (1110, uy + 27)], fill=CLR_MID_GRAY, width=1)

    # Center Linking Use Cases (Core System Operations)
    center_ucs = [
        ("Low Stock Monitoring", 260),
        ("Check Drug Expiry Dates", 390),
        ("1:1 Payment Verification", 520),
        ("Profit & Sales Aggregation", 650)
    ]
    for c_txt, cy in center_ucs:
        draw.ellipse([545, cy, 805, cy + 55], fill=CLR_BG_TINT, outline=CLR_BORDER_LIGHT, width=2)
        tb = F_NODE_TXT.getbbox(c_txt)
        draw.text((545 + (260 - (tb[2]-tb[0]))//2, cy + 18), c_txt, font=F_NODE_TXT, fill=CLR_DARK_GRAY)

    save_image(img, "02_Use_Case_Diagram.jpg")

# ==============================================================================
# 3. ENTITY RELATION DIAGRAM (Matching Reference 5 & User Prompt: Separate DB Boxes)
# "Use different boxes for different databases and keep all that boxes in the single image.
#  In each box should ER diagram of that specific DB tables."
# ==============================================================================
def generate_er_diagram():
    W, H = 1450, 1020
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_top_title(draw, W, "9.0 Entity-Relationship Diagram")

    # Helper function to draw an entity with its attribute ovals
    def draw_er_entity(cx, cy, ent_name, attrs, primary_key):
        ew, eh = 140, 50
        # Entity Rectangle
        draw.rectangle([cx - ew//2, cy - eh//2, cx + ew//2, cy + eh//2], fill=CLR_WHITE, outline=CLR_BORDER, width=2)
        nb = F_CARD_NAME.getbbox(ent_name)
        draw.text((cx - (nb[2]-nb[0])//2, cy - 10), ent_name, font=F_CARD_NAME, fill=CLR_BLACK)

        # Attribute Ovals positioned radially around entity
        n = len(attrs)
        radius_x = 135
        radius_y = 65
        for i, a in enumerate(attrs):
            ang = math.pi * 2 * (i / n) - math.pi / 2
            ax = cx + int(radius_x * math.cos(ang))
            ay = cy + int(radius_y * math.sin(ang))
            ow, oh = 50, 16
            draw.ellipse([ax - ow, ay - oh, ax + ow, ay + oh], fill=CLR_WHITE, outline=CLR_BORDER, width=1)
            draw.line([(cx, cy), (ax, ay)], fill=CLR_BORDER_LIGHT, width=1)
            # Re-draw ellipse on top of line
            draw.ellipse([ax - ow, ay - oh, ax + ow, ay + oh], fill=CLR_WHITE, outline=CLR_BORDER, width=1)
            ab = F_ATTR_BOLD.getbbox(a)
            draw.text((ax - (ab[2]-ab[0])//2, ay - 8), a, font=F_ATTR_BOLD, fill=CLR_BLACK)
            if a == primary_key:
                # Underline PK
                draw.line([(ax - (ab[2]-ab[0])//2, ay + 7), (ax + (ab[2]-ab[0])//2, ay + 7)], fill=CLR_BLACK, width=1)

    # Box 1: User DB (Auth Service) - Top Left (x: 30 to 450, y: 70 to 360)
    draw.rounded_rectangle([30, 70, 450, 360], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
    draw.rectangle([30, 70, 450, 102], fill=CLR_TABLE_HDR)
    draw.text((45, 78), "User DB (Auth Service)", font=F_SEC_TITLE, fill=CLR_WHITE)
    draw_er_entity(240, 230, "User", ["UserId (PK)", "name", "email", "phone", "passwordHash", "Role", "createdDate", "IsActive"], "UserId (PK)")

    # Box 2: Inventory DB (Inventory Service) - Top Right (x: 480 to 1420, y: 70 to 520)
    draw.rounded_rectangle([480, 70, 1420, 520], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
    draw.rectangle([480, 70, 1420, 102], fill=CLR_TABLE_HDR)
    draw.text((495, 78), "Inventory DB (Inventory Service)", font=F_SEC_TITLE, fill=CLR_WHITE)

    # Inside Inventory DB: Supplier, Drugs, Inventory entities + relationships
    draw_er_entity(630, 260, "Supplier", ["SupplierId (PK)", "supplierName", "email", "phone", "address"], "SupplierId (PK)")
    draw_er_entity(1270, 260, "Drugs", ["drugId (PK)", "name", "Price", "Expirydate", "quantity", "MinStockQty"], "drugId (PK)")
    draw_er_entity(950, 420, "Inventory", ["InventoryId (PK)", "supplierId", "DrugId", "purchasePrice", "SupplyDate", "QtySupplied"], "InventoryId (PK)")

    # Relationship Diamonds inside Inventory DB
    # Supplier --<supplies>-- Inventory
    def draw_er_rel(x1, y1, x2, y2, label):
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        rw, rh = 40, 20
        draw.line([(x1, y1), (x2, y2)], fill=CLR_BLACK, width=2)
        draw.polygon([(mx, my - rh), (mx + rw, my), (mx, my + rh), (mx - rw, my)], fill=CLR_WHITE, outline=CLR_BORDER)
        draw.line([(mx, my - rh), (mx + rw, my), (mx, my + rh), (mx - rw, my), (mx, my - rh)], fill=CLR_BORDER, width=2)
        lb = F_BADGE_TXT.getbbox(label)
        draw.text((mx - (lb[2]-lb[0])//2, my - 7), label, font=F_BADGE_TXT, fill=CLR_BLACK)

    draw_er_rel(630, 310, 880, 420, "supplies")
    draw.text((645, 320), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((860, 400), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    draw_er_rel(1270, 310, 1020, 420, "stocked")
    draw.text((1250, 320), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1035, 400), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # Box 3: Order DB (Order Service) - Bottom Left (x: 30 to 720, y: 390 to 800)
    draw.rounded_rectangle([30, 390, 720, 800], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
    draw.rectangle([30, 390, 720, 422], fill=CLR_TABLE_HDR)
    draw.text((45, 398), "Order DB (Order Service)", font=F_SEC_TITLE, fill=CLR_WHITE)

    draw_er_entity(220, 590, "Order", ["OrderId (PK)", "DoctorID", "OrderDate", "TotalAmount", "status"], "OrderId (PK)")
    draw_er_entity(550, 590, "OrderItem", ["OrderItemId (PK)", "OrderId", "DrugId", "quantity", "UnitPrice"], "OrderItemId (PK)")

    draw_er_rel(290, 590, 480, 590, "contains")
    draw.text((300, 565), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((460, 565), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # Box 4: Payment DB (Payment Service) - Bottom Center (x: 750 to 1100, y: 550 to 800)
    draw.rounded_rectangle([750, 550, 1100, 800], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
    draw.rectangle([750, 550, 1100, 582], fill=CLR_TABLE_HDR)
    draw.text((765, 558), "Payment DB", font=F_SEC_TITLE, fill=CLR_WHITE)

    draw_er_entity(925, 680, "Payment", ["PaymentId (PK)", "OrderId", "Amount", "paymentDate", "PaymentMethod", "PaymentStatus"], "PaymentId (PK)")

    # Box 5: SaleReport DB (SaleReport Service) - Bottom Right (x: 1120 to 1420, y: 550 to 800)
    draw.rounded_rectangle([1120, 550, 1420, 800], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
    draw.rectangle([1120, 550, 1420, 582], fill=CLR_TABLE_HDR)
    draw.text((1135, 558), "SaleReport DB", font=F_SEC_TITLE, fill=CLR_WHITE)

    draw_er_entity(1270, 680, "SaleReport", ["SaleReportId (PK)", "ReportType", "FromDate", "ToDate", "TotalOrders", "TotalRevenue", "Profit"], "SaleReportId (PK)")

    # Cross-Database Relationships (Dashed clean logical connector lines)
    # 1. User DB (User) -> Order DB (Order) [1:M]
    draw.line([(240, 280), (240, 540)], fill=CLR_DARK_GRAY, width=2)
    draw_er_rel(240, 360, 240, 480, "places")
    draw.text((250, 340), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((250, 510), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2. Order DB (Order) -> Payment DB (Payment) [1:1]
    draw.line([(290, 620), (750, 620)], fill=CLR_DARK_GRAY, width=2)
    draw.line([(750, 620), (855, 680)], fill=CLR_DARK_GRAY, width=2)
    draw.text((300, 625), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((825, 660), "1 (1:1)", font=F_CARD_NAME, fill=CLR_BLACK)

    # 3. Inventory DB (Drugs) -> Order DB (OrderItem) [1:M]
    draw.line([(1270, 310), (1270, 500)], fill=CLR_DARK_GRAY, width=2)
    draw.line([(1270, 500), (620, 500)], fill=CLR_DARK_GRAY, width=2)
    draw.line([(620, 500), (620, 540)], fill=CLR_DARK_GRAY, width=2)
    draw.text((1275, 330), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((630, 520), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # Bottom Architectural Legend Box (x: 30 to 1420, y: 830 to 1000)
    draw.rounded_rectangle([30, 830, 1420, 1000], radius=8, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((45, 842), "Architecture & Relationship Rules:", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((45, 875), "• Database-Per-Service: Each microservice owns its private database. No direct cross-database SQL foreign keys exist.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)
    draw.text((45, 905), "• Intra-Database Relationships: Supplier-to-Inventory (1:M), Drug-to-Inventory (1:M), and Order-to-OrderItem (1:M) use physical SQL foreign keys.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)
    draw.text((45, 935), "• Cross-Database Relationships: User-to-Order (1:M), Drug-to-OrderItem (1:M), and Order-to-Payment (1:1) are logical references verified via REST APIs.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)
    draw.text((45, 965), "• Standalone Service: SaleReportService operates independently to compute analytics and financial summaries across dates.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)

    save_image(img, "05_ER_Diagram.jpg")

# ==============================================================================
# 4. DATABASE DIAGRAM (Matching Reference 2: Dark Blue Header, Clear Columns)
# ==============================================================================
def generate_database_diagram():
    W, H = 1420, 920
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_top_title(draw, W, "10.0 Database Diagram")

    # Helper function to draw table box matching Reference 2
    def draw_db_table(x, y, w, tbl_name, cols):
        hdr_h = 36
        row_h = 24
        tbl_h = hdr_h + len(cols) * row_h + 10
        # Table container
        draw.rounded_rectangle([x, y, x + w, y + tbl_h], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
        # Dark Header Bar
        draw.rounded_rectangle([x, y, x + w, y + hdr_h], radius=6, fill=CLR_TABLE_HDR, outline=CLR_TABLE_HDR, width=1)
        draw.rectangle([x, y + 20, x + w, y + hdr_h], fill=CLR_TABLE_HDR) # square off bottom corners of header
        draw.text((x + 14, y + 8), tbl_name, font=F_CARD_NAME, fill=CLR_WHITE)
        # Gear icon placeholder on right
        draw.text((x + w - 28, y + 8), "⚙", font=F_BODY_BOLD, fill=CLR_BORDER_LIGHT)

        # Rows
        for i, (col_name, col_type, is_pk, is_fk) in enumerate(cols):
            ry = y + hdr_h + 8 + i * row_h
            if is_pk:
                draw.text((x + 12, ry), "🔑", font=F_BADGE_TXT, fill=CLR_BLACK)
                draw.text((x + 32, ry), col_name, font=F_BODY_BOLD, fill=CLR_BLACK)
            elif is_fk:
                draw.text((x + 12, ry), "🔗", font=F_BADGE_TXT, fill=CLR_DARK_GRAY)
                draw.text((x + 32, ry), col_name, font=F_BODY_BOLD, fill=CLR_BLACK)
            else:
                draw.text((x + 32, ry), col_name, font=F_ATTR_BOLD, fill=CLR_DARK_GRAY)

            tb = F_ATTR_BOLD.getbbox(col_type)
            draw.text((x + w - (tb[2]-tb[0]) - 14, ry), col_type, font=F_ATTR_BOLD, fill=CLR_MID_GRAY)

        return x, y, w, tbl_h

    # Table 1: users (x: 40, y: 80, width: 280)
    draw_db_table(40, 80, 280, "users", [
        ("user_id", "int", True, False),
        ("name", "varchar(100)", False, False),
        ("email", "varchar(150)", False, False),
        ("phone", "varchar(20)", False, False),
        ("role", "varchar(20)", False, False),
        ("password_hash", "varchar(255)", False, False),
        ("is_active", "bit", False, False),
        ("created_date", "datetime2", False, False)
    ])

    # Table 2: suppliers (x: 40, y: 360, width: 280)
    draw_db_table(40, 360, 280, "suppliers", [
        ("supplier_id", "int", True, False),
        ("supplier_name", "varchar(150)", False, False),
        ("email", "varchar(150)", False, False),
        ("phone", "varchar(20)", False, False),
        ("address", "varchar(300)", False, False)
    ])

    # Table 3: inventory (x: 40, y: 570, width: 280)
    draw_db_table(40, 570, 280, "inventory", [
        ("inventory_id", "int", True, False),
        ("supplier_id", "int", False, True),
        ("drug_id", "int", False, True),
        ("purchase_price", "decimal(18,2)", False, False),
        ("supply_date", "datetime2", False, False),
        ("quantity_supplied", "int", False, False)
    ])

    # Table 4: drugs (medicines) (x: 380, y: 80, width: 300)
    draw_db_table(380, 80, 300, "drugs (medicines)", [
        ("drug_id", "int", True, False),
        ("name", "varchar(150)", False, False),
        ("description", "varchar(500)", False, False),
        ("price", "decimal(18,2)", False, False),
        ("expiry_date", "date", False, False),
        ("quantity", "int", False, False),
        ("min_stock_qty", "int", False, False),
        ("is_available", "bit", False, False)
    ])

    # Table 5: orders (x: 740, y: 80, width: 300)
    draw_db_table(740, 80, 300, "orders", [
        ("order_id", "int", True, False),
        ("doctor_id", "int", False, True),
        ("order_date", "datetime2", False, False),
        ("total_amount", "decimal(18,2)", False, False),
        ("status", "varchar(20)", False, False)
    ])

    # Table 6: order_items (x: 1090, y: 80, width: 290)
    draw_db_table(1090, 80, 290, "order_items", [
        ("order_item_id", "int", True, False),
        ("order_id", "int", False, True),
        ("drug_id", "int", False, True),
        ("quantity", "int", False, False),
        ("unit_price", "decimal(18,2)", False, False)
    ])

    # Table 7: payments (x: 740, y: 350, width: 300)
    draw_db_table(740, 350, 300, "payments", [
        ("payment_id", "int", True, False),
        ("order_id", "int (1:1 Unique)", False, True),
        ("amount", "decimal(18,2)", False, False),
        ("payment_date", "datetime2", False, False),
        ("payment_method", "varchar(50)", False, False),
        ("payment_status", "varchar(20)", False, False)
    ])

    # Table 8: salereports (x: 1090, y: 350, width: 290)
    draw_db_table(1090, 350, 290, "salereports", [
        ("sale_report_id", "int", True, False),
        ("report_type", "varchar(20)", False, False),
        ("from_date", "datetime2", False, False),
        ("to_date", "datetime2", False, False),
        ("total_orders", "int", False, False),
        ("total_revenue", "decimal(18,2)", False, False),
        ("generated_date", "datetime2", False, False),
        ("profit", "decimal(18,2)", False, False)
    ])

    # Foreign Key Relationship Lines (with fork / crow's foot indicators)
    # 1. users -> orders (1:M)
    draw.line([(320, 115), (740, 115)], fill=CLR_BORDER, width=2)
    draw.text((325, 95), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((715, 95), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2. orders -> order_items (1:M)
    draw.line([(1040, 125), (1090, 125)], fill=CLR_BORDER, width=2)
    draw.text((1045, 105), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1075, 105), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # 3. drugs -> order_items (1:M)
    draw.line([(680, 180), (1060, 180)], fill=CLR_BORDER, width=2)
    draw.line([(1060, 180), (1090, 150)], fill=CLR_BORDER, width=2)
    draw.text((685, 160), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((1075, 130), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # 4. orders -> payments (1:1 Unique)
    draw.line([(890, 235), (890, 350)], fill=CLR_BORDER, width=2)
    draw.text((900, 240), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((900, 325), "1 (1:1)", font=F_CARD_NAME, fill=CLR_BLACK)

    # 5. suppliers -> inventory (1:M)
    draw.line([(180, 495), (180, 570)], fill=CLR_BORDER, width=2)
    draw.text((190, 500), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((190, 545), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # 6. drugs -> inventory (1:M)
    draw.line([(530, 330), (530, 630)], fill=CLR_BORDER, width=2)
    draw.line([(530, 630), (320, 630)], fill=CLR_BORDER, width=2)
    draw.text((540, 335), "1", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.text((325, 610), "M", font=F_CARD_NAME, fill=CLR_BLACK)

    # Bottom Notes Panel (x: 40 to 1380, y: 780 to 900)
    draw.rounded_rectangle([40, 780, 1380, 900], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER_LIGHT, width=2)
    draw.text((55, 792), "Database Architecture Notes:", font=F_SEC_TITLE, fill=CLR_BLACK)
    draw.text((55, 822), "• 5 Isolated Databases: Pharmacy_UserDB, Pharmacy_InventoryDB, Pharmacy_OrderDB, Pharmacy_PaymentDB, Pharmacy_SaleReportDB.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)
    draw.text((55, 848), "• Unique 1:1 Payment Constraint: Payment.order_id has a UNIQUE index ensuring an order cannot be paid twice.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)
    draw.text((55, 874), "• Low Stock Trigger: Drugs.quantity <= Drugs.min_stock_qty triggers alerts on the Admin dashboard.", font=F_BODY_BOLD, fill=CLR_DARK_GRAY)

    save_image(img, "06_Database_Schema_Diagram.jpg")

# ==============================================================================
# 5. CLASS DIAGRAM (Matching Reference 3: 3-Compartment UML, (C) icon, Dashed Lines)
# ==============================================================================
def generate_class_diagram():
    W, H = 1400, 980
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_top_title(draw, W, "11.0 Class Diagram")

    # Helper function to draw UML class box with 3 compartments
    def draw_uml_class(x, y, w, cls_name, fields, methods):
        hdr_h = 34
        fld_h = len(fields) * 22 + 8
        mth_h = len(methods) * 22 + 8
        total_h = hdr_h + fld_h + mth_h

        # Outer border
        draw.rounded_rectangle([x, y, x + w, y + total_h], radius=4, fill=CLR_WHITE, outline=CLR_BORDER, width=2)

        # Header compartment
        draw.rectangle([x, y, x + w, y + hdr_h], fill=CLR_BG_TINT, outline=CLR_BORDER, width=1)
        # Circle (C) icon
        draw.ellipse([x + 12, y + 8, x + 30, y + 26], fill=CLR_WHITE, outline=CLR_BORDER, width=2)
        draw.text((x + 16, y + 7), "C", font=F_BADGE_TXT, fill=CLR_BLACK)
        draw.text((x + 38, y + 7), cls_name, font=F_CARD_NAME, fill=CLR_BLACK)

        # Divider line
        draw.line([(x, y + hdr_h), (x + w, y + hdr_h)], fill=CLR_BORDER, width=1)

        # Fields compartment
        fy = y + hdr_h + 6
        for f in fields:
            draw.text((x + 10, fy), f, font=F_ATTR_BOLD, fill=CLR_DARK_GRAY)
            fy += 22

        # Divider line
        draw.line([(x, y + hdr_h + fld_h), (x + w, y + hdr_h + fld_h)], fill=CLR_BORDER, width=1)

        # Methods compartment
        my = y + hdr_h + fld_h + 6
        for m in methods:
            draw.text((x + 10, my), m, font=F_ATTR_BOLD, fill=CLR_BLACK)
            my += 22

        return x, y, w, total_h

    # Class 1: User (Top Center: x: 530, y: 70, width: 340)
    draw_uml_class(530, 70, 340, "User", [
        "-userId : int",
        "-name : string",
        "-phone : string",
        "-email : string",
        "-role : string",
        "-passwordHash : string"
    ], [
        "+login(email, password) : Token",
        "+signup(userDto) : User",
        "+viewDrugs() : List<Drug>",
        "+placeOrder(orderDto) : Order",
        "+viewOrders() : List<Order>"
    ])

    # Class 2: Supplier (Middle Left: x: 60, y: 390, width: 330)
    draw_uml_class(60, 390, 330, "Supplier", [
        "-supplierId : int",
        "-supplierName : string",
        "-email : string",
        "-phoneNumber : string",
        "-address : string"
    ], [
        "+addSupplier(dto) : Supplier",
        "+updateSupplier(id, dto) : void",
        "+deleteSupplier(id) : void",
        "+getSupplierDetails(id) : Supplier"
    ])

    # Class 3: Drug (Middle Center: x: 440, y: 390, width: 340)
    draw_uml_class(440, 390, 340, "Drug", [
        "-drugId : int",
        "-name : string",
        "-description : string",
        "-price : decimal",
        "-expiryDate : DateTime",
        "-quantity : int",
        "-minStockQty : int"
    ], [
        "+addDrug(dto) : Drug",
        "+updateDrug(id, dto) : void",
        "+deleteDrug(id) : void",
        "+checkAvailability() : bool",
        "+updateStock(qty) : void"
    ])

    # Class 4: Order (Middle Right: x: 820, y: 390, width: 340)
    draw_uml_class(820, 390, 340, "Order", [
        "-orderId : int",
        "-doctorId : int",
        "-orderDate : DateTime",
        "-totalAmount : decimal",
        "-status : string"
    ], [
        "+createOrder(dto) : Order",
        "+calculateTotal() : decimal",
        "+updateStatus(status) : void",
        "+verifyOrder(id) : void",
        "+markPickedUp(id) : void"
    ])

    # Class 5: OrderItem (Bottom Right: x: 820, y: 690, width: 340)
    draw_uml_class(820, 690, 340, "OrderItem", [
        "-orderItemId : int",
        "-orderId : int",
        "-drugId : int",
        "-quantity : int",
        "-unitPrice : decimal"
    ], [
        "+calculateSubTotal() : decimal",
        "+updateQuantity(qty) : void"
    ])

    # Class 6: Payment (Bottom Center: x: 440, y: 690, width: 340)
    draw_uml_class(440, 690, 340, "Payment", [
        "-paymentId : int",
        "-orderId : int",
        "-amount : decimal",
        "-paymentDate : DateTime",
        "-paymentMethod : string",
        "-paymentStatus : string"
    ], [
        "+simulatePayment(orderId, amt) : Payment",
        "+verifyTransaction(id) : bool"
    ])

    # Class 7: SaleReport (Bottom Left: x: 60, y: 690, width: 330)
    draw_uml_class(60, 690, 330, "SaleReport", [
        "-saleReportId : int",
        "-reportType : string",
        "-fromDate : DateTime",
        "-toDate : DateTime",
        "-totalOrders : int",
        "-totalRevenue : decimal",
        "-profit : decimal"
    ], [
        "+generateReport(type, from, to) : Report",
        "+exportCsv() : byte[]"
    ])

    # Dashed Relationship Connectors with Labels
    # User -> Supplier (manages)
    draw_arrow(draw, (530, 240), (330, 390), CLR_BORDER, 2, "manages", True, True)

    # User -> Drug (views)
    draw_arrow(draw, (650, 310), (600, 390), CLR_BORDER, 2, "views", True, True)

    # User -> Order (places)
    draw_arrow(draw, (870, 240), (940, 390), CLR_BORDER, 2, "places", True, True)

    # Supplier -> Drug (supplies)
    draw_arrow(draw, (390, 450), (440, 450), CLR_BORDER, 2, "supplies", True, True)

    # Order -> OrderItem (contains)
    draw_arrow(draw, (990, 620), (990, 690), CLR_BORDER, 2, "contains", True, True)

    # Drug -> OrderItem (included in)
    draw_arrow(draw, (780, 520), (820, 720), CLR_BORDER, 2, "included in", True, True)

    # Order -> Payment (paid by)
    draw_arrow(draw, (820, 580), (780, 720), CLR_BORDER, 2, "paid by", True, True)

    # User -> SaleReport (analyzes)
    draw_arrow(draw, (530, 290), (220, 690), CLR_BORDER, 2, "views reports", True, True)

    save_image(img, "03_Class_Diagram.jpg")

# ==============================================================================
# 6. FLOW DIAGRAM (Matching Reference Template Page 8)
# ==============================================================================
def generate_flow_diagram():
    W, H = 1250, 1350
    img = Image.new("RGB", (W, H), CLR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_top_title(draw, W, "6.0 Flow Diagram")

    # START Pill
    draw.rounded_rectangle([535, 80, 715, 125], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((595, 90), "START", font=F_CARD_NAME, fill=CLR_BLACK)
    draw_arrow(draw, (625, 125), (625, 155), CLR_BLACK, 2)

    # Login Box (width: 520px)
    draw.rounded_rectangle([365, 155, 885, 205], radius=8, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((410, 168), "User Registration / Admin or Doctor Login", font=F_CARD_NAME, fill=CLR_BLACK)
    draw_arrow(draw, (625, 205), (625, 240), CLR_BLACK, 2)

    # Role Diamond
    dw, dh = 85, 40
    pts = [(625, 240), (625 + dw, 275), (625, 310), (625 - dw, 275)]
    draw.polygon(pts, fill=CLR_WHITE, outline=CLR_BORDER)
    draw.line(pts + [pts[0]], fill=CLR_BORDER, width=2)
    draw.text((602, 263), "Role?", font=F_CARD_NAME, fill=CLR_BLACK)

    # 2 Branches: Admin (Left) & Doctor (Right)
    draw.line([(625 - dw, 275), (240, 275)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (240, 275), (240, 320), CLR_BLACK, 2)
    draw.text((310, 250), "Admin / Pharmacist", font=F_BODY_BOLD, fill=CLR_BLACK)

    draw.line([(625 + dw, 275), (1010, 275)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (1010, 275), (1010, 320), CLR_BLACK, 2)
    draw.text((800, 250), "Doctor / Customer", font=F_BODY_BOLD, fill=CLR_BLACK)

    # Admin Lane (Left Column: x: 50 to 430, width = 380px)
    admin_boxes = [
        ("Manage Users & Roles", "(Admin & Doctor Accounts)", 320),
        ("Manage Drugs Catalog", "(Add, Edit, Delete Drugs)", 405),
        ("Manage Suppliers & Stock", "(Stock Inwarding & Batches)", 490),
        ("Verify Doctor Orders", "(Check Prescription Details)", 575),
        ("Handover Medicine", "(Mark Order as 'PickedUp')", 660),
        ("View Sales Analytics", "(Revenue, Orders & Profit)", 745)
    ]
    for b_t1, b_t2, by in admin_boxes:
        draw.rounded_rectangle([50, by, 430, by + 58], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
        tb1 = F_NODE_TXT.getbbox(b_t1)
        draw.text((50 + (380 - (tb1[2]-tb1[0]))//2, by + 10), b_t1, font=F_NODE_TXT, fill=CLR_BLACK)
        tb2 = F_ATTR_BOLD.getbbox(b_t2)
        draw.text((50 + (380 - (tb2[2]-tb2[0]))//2, by + 32), b_t2, font=F_ATTR_BOLD, fill=CLR_DARK_GRAY)
        if by < 745:
            draw_arrow(draw, (240, by + 58), (240, by + 88), CLR_BLACK, 2)

    # Doctor Lane (Right Column: x: 820 to 1200, width = 380px)
    doc_boxes = [
        ("Search Available Drugs", "(Browse Catalog & Check Stock)", 320),
        ("View Drug Details", "(Unit Prices & Dosage Info)", 405),
        ("Select Quantities", "(Add Medicine Items to Cart)", 490),
        ("Create Prescription Order", "(Enter Doctor ID & Details)", 575),
        ("Calculate Total Amount", "(Sum of Quantity * UnitPrice)", 660),
        ("Proceed to Payment", "(Select Simulation Payment Method)", 745)
    ]
    for b_t1, b_t2, by in doc_boxes:
        draw.rounded_rectangle([820, by, 1200, by + 58], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
        tb1 = F_NODE_TXT.getbbox(b_t1)
        draw.text((820 + (380 - (tb1[2]-tb1[0]))//2, by + 10), b_t1, font=F_NODE_TXT, fill=CLR_BLACK)
        tb2 = F_ATTR_BOLD.getbbox(b_t2)
        draw.text((820 + (380 - (tb2[2]-tb2[0]))//2, by + 32), b_t2, font=F_ATTR_BOLD, fill=CLR_DARK_GRAY)
        draw_arrow(draw, (1010, by + 58), (1010, by + 88), CLR_BLACK, 2)

    # Center Flow: Payment Decision Diamond
    draw.line([(1010, 803), (1010, 830)], fill=CLR_BLACK, width=2)
    draw.line([(1010, 830), (625, 830)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (625, 830), (625, 855), CLR_BLACK, 2)

    # Payment Successful? Diamond
    p_dw, p_dh = 100, 45
    p_pts = [(625, 855), (625 + p_dw, 900), (625, 945), (625 - p_dw, 900)]
    draw.polygon(p_pts, fill=CLR_WHITE, outline=CLR_BORDER)
    draw.line(p_pts + [p_pts[0]], fill=CLR_BORDER, width=2)
    draw.text((555, 888), "Payment Successful?", font=F_CARD_NAME, fill=CLR_BLACK)

    # Branch NO (Left to Dashed Box)
    draw.line([(625 - p_dw, 900), (420, 900)], fill=CLR_BLACK, width=2)
    draw_arrow(draw, (420, 900), (390, 900), CLR_BLACK, 2)
    draw.text((450, 875), "No", font=F_CARD_NAME, fill=CLR_BLACK)

    # Payment Failed Box (Dashed: x: 80 to 390, width: 310px, y: 860 to 1150)
    draw.rounded_rectangle([80, 860, 390, 1150], radius=10, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
    draw.text((120, 875), "Payment Failed Subflow", font=F_CARD_NAME, fill=CLR_BLACK)
    draw.line([(80, 905), (390, 905)], fill=CLR_BORDER_LIGHT, width=1)

    fail_steps = [
        ("Show Failure Message", 920),
        ("Update Status = 'Failed'", 980),
        ("Release Reserved Drug Stock", 1040)
    ]
    for ft, fy in fail_steps:
        draw.rounded_rectangle([95, fy, 375, fy + 44], radius=6, fill=CLR_WHITE, outline=CLR_BORDER_LIGHT, width=2)
        tb = F_NODE_TXT.getbbox(ft)
        draw.text((95 + (280 - (tb[2]-tb[0]))//2, fy + 12), ft, font=F_NODE_TXT, fill=CLR_BLACK)
        if fy < 1040:
            draw_arrow(draw, (235, fy + 44), (235, fy + 60), CLR_BLACK, 2)

    draw.rounded_rectangle([95, 1100, 375, 1140], radius=6, fill=CLR_WHITE, outline=CLR_BORDER, width=2)
    draw.text((150, 1110), "Cancel Order Record", font=F_BODY_BOLD, fill=CLR_BLACK)

    # Branch YES (Down to Success Flow)
    draw_arrow(draw, (625, 945), (625, 985), CLR_BLACK, 2)
    draw.text((635, 955), "Yes", font=F_CARD_NAME, fill=CLR_BLACK)

    success_boxes = [
        ("Confirm Order (Status = 'Pending')", 985),
        ("Generate Invoice & Payment ID", 1055),
        ("Pharmacist Order Verification & Handover", 1125)
    ]
    for st, sy in success_boxes:
        draw.rounded_rectangle([440, sy, 890, sy + 50], radius=8, fill=CLR_BG_TINT, outline=CLR_BORDER, width=2)
        tb = F_CARD_NAME.getbbox(st)
        draw.text((440 + (450 - (tb[2]-tb[0]))//2, sy + 15), st, font=F_CARD_NAME, fill=CLR_BLACK)
        if sy < 1125:
            draw_arrow(draw, (665, sy + 50), (665, sy + 70), CLR_BLACK, 2)

    # Connect to END Pill
    draw_arrow(draw, (665, 1175), (665, 1225), CLR_BLACK, 2)
    draw.line([(235, 1140), (235, 1205)], fill=CLR_BLACK, width=2)
    draw.line([(235, 1205), (575, 1205)], fill=CLR_BLACK, width=2)
    draw.line([(240, 803), (240, 830)], fill=CLR_BLACK, width=2)

    # END Pill
    draw.rounded_rectangle([575, 1225, 755, 1270], radius=22, fill=CLR_WHITE, outline=CLR_BORDER, width=3)
    draw.text((640, 1235), "END", font=F_CARD_NAME, fill=CLR_BLACK)

    save_image(img, "04_Flow_Diagram.jpg")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_use_case_diagram()
    generate_er_diagram()
    generate_database_diagram()
    generate_class_diagram()
    generate_flow_diagram()
    print("ALL 6 DIAGRAMS SUCCESSFULLY GENERATED IN BLACK-AND-WHITE / REFERENCE STYLE!")
