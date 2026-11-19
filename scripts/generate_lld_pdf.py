import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

# Output Paths
WORKSPACE_PDF = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\PharmacyManagement_LLD.pdf"
ARTIFACT_PDF = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\PharmacyManagement_LLD.pdf"
DIAGRAMS_DIR = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"

# Corporate Color Palette (Matching Template)
COLOR_PRIMARY = colors.HexColor("#004F7A")      # Deep teal / navy
COLOR_DARK = colors.HexColor("#1E293B")         # Charcoal body text
COLOR_LIGHT_BG = colors.HexColor("#F1F5F9")     # Table header light slate
COLOR_ALT_BG = colors.HexColor("#F8FAFC")       # Alternating row background
COLOR_BORDER = colors.HexColor("#CBD5E1")       # Clean table border
COLOR_MUTED = colors.HexColor("#64748B")        # Subtext muted gray

# Global dictionary to track section page numbers
SECTION_PAGE_MAP = {}

class TrackedParagraph(Paragraph):
    def __init__(self, text, style, section_id):
        super().__init__(text, style)
        self.section_id = section_id

    def draw(self):
        SECTION_PAGE_MAP[self.section_id] = self.canv._pageNumber
        super().draw()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        if page_num == 1:
            return  # Skip cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)

        # Running Header
        self.drawString(54, 750, "Pharmacy Management System — Low Level Design (LLD)")
        self.drawRightString(558, 750, "POC - .NET 10 Microservices")
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "Confidential — For Internal Project Use Only")
        page_text = f"Page {page_num} of {total_pages}"
        self.drawRightString(558, 34, page_text)
        self.restoreState()

def build_pdf_story(section_page_dict):
    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=COLOR_PRIMARY,
        alignment=1, # Center
        spaceAfter=10
    )

    style_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=20,
        textColor=COLOR_PRIMARY,
        alignment=1,
        spaceAfter=30
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=COLOR_PRIMARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyClean',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_DARK,
        spaceAfter=5
    )

    style_bullet = ParagraphStyle(
        'BulletClean',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=COLOR_DARK,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    style_caption = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_MUTED,
        alignment=1,
        spaceBefore=4,
        spaceAfter=8
    )

    style_th = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_DARK
    )

    style_td = ParagraphStyle(
        'TableData',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_DARK
    )

    style_td_bold = ParagraphStyle(
        'TableDataBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_DARK
    )

    story = []

    # --------------------------------------------------------------------------
    # COVER PAGE
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 120))
    story.append(Paragraph("PHARMACY MANAGEMENT SYSTEM", style_title))
    story.append(Paragraph("POC<br/>Low Level Design (LLD)", style_subtitle))
    story.append(Spacer(1, 240))

    meta_text = (
        "PharmacyManagement Microservices<br/>"
        "POC – Low Level Design (LLD)<br/><br/>"
        "Date: 19/11/2026<br/>"
        "Current Document Version: [1.0]<br/><br/>"
        "Author: <b>Lahari Chikoti</b>"
    )
    story.append(Paragraph(meta_text, style_body))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # DOCUMENT APPROVAL & CHANGE HISTORY
    # --------------------------------------------------------------------------
    story.append(Paragraph("DOCUMENT APPROVAL Approvers of this document", style_h1))
    
    app_data = [
        [Paragraph("Name", style_th), Paragraph("Department", style_th), Paragraph("Role", style_th), Paragraph("Signature", style_th), Paragraph("Date", style_th)],
        [Paragraph("Lahari Chikoti", style_td_bold), Paragraph("Engineering", style_td), Paragraph("Lead Developer", style_td), Paragraph("L. Chikoti", style_td), Paragraph("19/11/2026", style_td)],
        [Paragraph("Technical Reviewer", style_td_bold), Paragraph("Architecture", style_td), Paragraph("Solution Architect", style_td), Paragraph("Approved", style_td), Paragraph("19/11/2026", style_td)]
    ]
    t_app = Table(app_data, colWidths=[110, 95, 115, 95, 85])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_app)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Document Change History", style_h1))
    hist_data = [
        [Paragraph("Document Version #", style_th), Paragraph("Author", style_th), Paragraph("Date", style_th), Paragraph("Description", style_th)],
        [Paragraph("1.0", style_td_bold), Paragraph("Lahari Chikoti", style_td), Paragraph("19/11/2026", style_td), Paragraph("Pharmacy Management System LLD Initial Baseline", style_td)]
    ]
    t_hist = Table(hist_data, colWidths=[110, 100, 85, 205])
    t_hist.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_hist)
    story.append(Spacer(1, 15))

    # --------------------------------------------------------------------------
    # TABLE OF CONTENTS
    # --------------------------------------------------------------------------
    story.append(Paragraph("Table of Contents", ParagraphStyle('TOCH', parent=style_h1, alignment=2)))

    toc_defs = [
        ("1.0", "Document Purpose", "sec_1"),
        ("2.0", "Intended Audience", "sec_2"),
        ("3.0", "Project Background and Objectives", "sec_3"),
        ("4.0", "Requirements", "sec_4"),
        ("5.0", "Design Patterns", "sec_5"),
        ("6.0", "Flow Diagram", "sec_6"),
        ("7.0", "Use Case Diagram", "sec_7"),
        ("8.0", "Architecture Diagram", "sec_8"),
        ("9.0", "Entity-Relationship Diagram", "sec_9"),
        ("10.0", "Database Diagram", "sec_10"),
        ("11.0", "Class Diagram", "sec_11"),
        ("12.0", "Solution Steps", "sec_12"),
        ("13.0", "Classes Names", "sec_13"),
        ("14.0", "Validations", "sec_14"),
        ("15.0", "API Catalogue", "sec_15"),
        ("16.0", "HTTP Status Codes", "sec_16"),
        ("17.0", "Integrations", "sec_17"),
        ("18.0", "Sample API Requests", "sec_18"),
        ("19.0", "Sample API Responses", "sec_19"),
        ("20.0", "NUnit Unit Testing", "sec_20")
    ]

    toc_rows = [[Paragraph("Section", style_th), Paragraph("Title", style_th), Paragraph("Page No.", style_th)]]
    for s_num, s_title, s_key in toc_defs:
        p_str = str(section_page_dict.get(s_key, ""))
        toc_rows.append([
            Paragraph(s_num, style_td_bold),
            Paragraph(s_title, style_td),
            Paragraph(p_str, ParagraphStyle('TRight', parent=style_td, alignment=2))
        ])

    t_toc = Table(toc_rows, colWidths=[65, 365, 70])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 1.0 & 2.0
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("1.0 Document Purpose", style_h1, "sec_1"))
    story.append(Paragraph(
        "This document describes the Low-Level Design (LLD) of the Pharmacy Management System. "
        "The system is built using C#, ASP.NET Core Web API, .NET 10, and a microservices architecture. "
        "It defines the service layout, database tables, business rules, validations, APIs, and unit testing approach.",
        style_body
    ))
    story.append(Paragraph(
        "The application has five independent services: Auth Service, Inventory Service, Order Service, "
        "Payment Service, and SaleReport Service. Each service owns its private database. "
        "Services talk to each other through REST APIs, while the YARP API Gateway routes client requests. "
        "Swagger UI is used to test and document all endpoints.",
        style_body
    ))
    story.append(Spacer(1, 10))

    story.append(TrackedParagraph("2.0 Intended Audience", style_h1, "sec_2"))
    story.append(Paragraph("This document serves as a guide for project stakeholders:", style_body))

    aud_rows = [
        [Paragraph("Role", style_th), Paragraph("Engagement in Pharmacy Management Architecture", style_th)],
        [Paragraph("Product Owners / SMEs", style_td_bold), Paragraph("Confirm that the design covers all pharmacy requirements.", style_td)],
        [Paragraph("Business Analysts", style_td_bold), Paragraph("Map doctor and admin business workflows to technical APIs.", style_td)],
        [Paragraph("Enterprise Architects", style_td_bold), Paragraph("Review microservice boundaries, security rules, and database isolation.", style_td)],
        [Paragraph("Solution Architects", style_td_bold), Paragraph("Check the API contracts, service communications, and data flow.", style_td)],
        [Paragraph("Developers & QA Engineers", style_td_bold), Paragraph("Use this document to implement features and write unit tests.", style_td)]
    ]
    t_aud = Table(aud_rows, colWidths=[160, 340])
    t_aud.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_aud)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 3.0 & 4.0
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("3.0 Project Background and Objectives", style_h1, "sec_3"))
    story.append(Paragraph("3.1 Project Background", style_h2))
    story.append(Paragraph(
        "Pharmacies need reliable software to manage medicine stocks, drug suppliers, doctor prescription orders, "
        "and sales accounting. Handling these records manually leads to misplaced orders, billing errors, or stock shortages.<br/><br/>"
        "The Pharmacy Management System provides a clean backend solution. Doctors can check available medicines, "
        "add items to cart, and place orders. Admins can manage medicines, track supplier deliveries, verify orders, "
        "and view profit and sales reports.",
        style_body
    ))

    story.append(Paragraph("3.2 Project Objective", style_h2))
    story.append(Paragraph(
        "The objective is to develop a reliable and modular backend using C#, ASP.NET Core Web API, .NET 10, "
        "and microservices architecture. Key goals include:<br/>"
        "• Dividing operations into five services with separate SQL databases.<br/>"
        "• Securing endpoints using JWT Bearer authentication and role checks (Admin and Doctor).<br/>"
        "• Enabling doctors to browse medicines, place orders, and simulate payments.<br/>"
        "• Enabling admins to manage inventory, verify orders, and review sales analytics.<br/>"
        "• Documenting all endpoints in Swagger UI and validating logic with NUnit tests.",
        style_body
    ))
    story.append(Spacer(1, 10))

    story.append(TrackedParagraph("4.0 Requirements", style_h1, "sec_4"))
    story.append(Paragraph("4.1 Functional Requirements (FR)", style_h2))
    story.append(Paragraph("<b>For Admin:</b>", style_body))
    story.append(Paragraph("• Login / Signup: Sign up and log in using name, email, contact number, and password.", style_bullet))
    story.append(Paragraph("• View Drugs: Browse and view full details of all medicines in the pharmacy.", style_bullet))
    story.append(Paragraph("• Manage Drugs: Add new drugs, edit drug details and prices, and delete drugs.", style_bullet))
    story.append(Paragraph("• Manage Suppliers: View suppliers, add new suppliers, and update supplier information.", style_bullet))
    story.append(Paragraph("• View Doctor Orders: Review orders placed by doctors and check their validity.", style_bullet))
    story.append(Paragraph("• Verify Orders: Mark valid doctor orders as 'Verified'.", style_bullet))
    story.append(Paragraph("• Order Handover: Move verified orders to the 'PickedUp' section once collected.", style_bullet))
    story.append(Paragraph("• Sales Reports: View daily, weekly, monthly, and yearly sales summaries.", style_bullet))
    story.append(Paragraph("• Download / Print: Export sales reports in CSV format for printing and bookkeeping.", style_bullet))
    story.append(Paragraph("• Dashboard Analytics: Monitor low stock medicines, check expired drugs, analyze profit margins, and track top-selling medicines.", style_bullet))

    story.append(Paragraph("<b>For Doctor User:</b>", style_body))
    story.append(Paragraph("• Login / Signup: Sign up and log in with name, email, contact number, and password.", style_bullet))
    story.append(Paragraph("• View Drugs: Browse all available medicines with prices and current stock counts.", style_bullet))
    story.append(Paragraph("• Buy Drugs & Cart: Add selected drugs to cart and create prescription orders.", style_bullet))
    story.append(Paragraph("• Payment Simulation: Complete order payment checkout using simulated payment.", style_bullet))
    story.append(Paragraph("• Track Order Status: Check order progress (Cart, Pending, Verified, PickedUp, or Cancelled).", style_bullet))
    story.append(Paragraph("• Order History: View all previously placed orders and receipts.", style_bullet))

    story.append(Paragraph("4.2 Non-Functional Requirements", style_h2))
    story.append(Paragraph("• Microservices Architecture: 5 separate services with isolated databases.", style_bullet))
    story.append(Paragraph("• Security: Protected APIs require valid JWT Bearer tokens with role claims.", style_bullet))
    story.append(Paragraph("• REST APIs: Synchronous communication between services using typed HTTP clients.", style_bullet))
    story.append(Paragraph("• Routing: YARP API Gateway acts as a single entry point for all client requests.", style_bullet))
    story.append(Paragraph("• Validation & Error Handling: Clear validation messages and standard HTTP status codes.", style_bullet))
    story.append(Paragraph("• Testing: Comprehensive NUnit unit tests and interactive testing via Swagger UI.", style_bullet))

    story.append(Paragraph("4.3 Technology Stack", style_h2))
    tech_rows = [
        [Paragraph("Category", style_th), Paragraph("Technology", style_th), Paragraph("Purpose", style_th)],
        [Paragraph("Language", style_td_bold), Paragraph("C# 12", style_td), Paragraph("Primary programming language for all services.", style_td)],
        [Paragraph("Framework", style_td_bold), Paragraph("ASP.NET Core Web API", style_td), Paragraph("Framework used to build RESTful microservice APIs.", style_td)],
        [Paragraph("Runtime", style_td_bold), Paragraph(".NET 10", style_td), Paragraph("Cross-platform runtime to build and run the services.", style_td)],
        [Paragraph("ORM", style_td_bold), Paragraph("Entity Framework Core 8", style_td), Paragraph("Maps C# models to SQL tables using Code-First approach.", style_td)],
        [Paragraph("Database", style_td_bold), Paragraph("Microsoft SQL Server 2022", style_td), Paragraph("Hosts 5 separate databases for microservice data isolation.", style_td)],
        [Paragraph("Security", style_td_bold), Paragraph("JWT Bearer & PBKDF2", style_td), Paragraph("Authenticates users and hashes passwords securely.", style_td)],
        [Paragraph("Authorization", style_td_bold), Paragraph("Role-Based Access (RBAC)", style_td), Paragraph("Restricts API access based on Admin and Doctor roles.", style_td)],
        [Paragraph("API Gateway", style_td_bold), Paragraph("YARP", style_td), Paragraph("Routes incoming requests to the appropriate microservices.", style_td)],
        [Paragraph("API Documentation", style_td_bold), Paragraph("Swagger / OpenAPI 3.0", style_td), Paragraph("Documents and interactively tests backend APIs.", style_td)],
        [Paragraph("Testing", style_td_bold), Paragraph("NUnit & Moq", style_td), Paragraph("Automated unit test suite verifying service layer logic.", style_td)]
    ]
    t_tech = Table(tech_rows, colWidths=[120, 150, 230])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_tech)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 5.0 DESIGN PATTERNS
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("5.0 Design Patterns", style_h1, "sec_5"))
    story.append(Paragraph("The architecture uses standard enterprise design patterns to maintain clean separation of concerns:", style_body))

    pat_rows = [
        [Paragraph("Name", style_th), Paragraph("Description", style_th)],
        [Paragraph("REST API", style_td_bold), Paragraph("HTTP-based REST APIs are used for client calls and service-to-service communication.", style_td)],
        [Paragraph("Microservices Architecture", style_td_bold), Paragraph("The system is divided into five independent services: Auth, Inventory, Order, Payment, and SaleReport.", style_td)],
        [Paragraph("Layered Architecture", style_td_bold), Paragraph("Each microservice follows a Controller, Service, and Repository structure to separate concerns.", style_td)],
        [Paragraph("Repository Pattern", style_td_bold), Paragraph("Repositories handle database access, keeping data logic separate from business rules.", style_td)],
        [Paragraph("Dependency Injection", style_td_bold), Paragraph("Services and repositories are injected via built-in DI containers for testability.", style_td)],
        [Paragraph("Database per Service", style_td_bold), Paragraph("Each microservice owns its private database. No direct cross-service SQL joins are allowed.", style_td)],
        [Paragraph("API Gateway Pattern", style_td_bold), Paragraph("YARP provides a centralized entry point and routes client requests to microservices.", style_td)],
        [Paragraph("DTO Pattern", style_td_bold), Paragraph("Request and response DTOs define clean API contracts and prevent over-posting.", style_td)]
    ]
    t_pat = Table(pat_rows, colWidths=[160, 340])
    t_pat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_pat)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 6.0 FLOW DIAGRAM
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("6.0 Flow Diagram", style_h1, "sec_6"))
    flow_img_path = os.path.join(DIAGRAMS_DIR, "04_Flow_Diagram.jpg")
    if os.path.exists(flow_img_path):
        story.append(Image(flow_img_path, width=440, height=475))
        story.append(Paragraph("Figure 6.0 – Operational Flow Diagram", style_caption))

    story.append(Paragraph("<b>Description</b>", style_body))
    story.append(Paragraph(
        "The flow diagram shows the operational steps for Admin and Doctor users. A user signs up or logs in and receives a JWT token. "
        "Based on their role:<br/>"
        "• Admins manage drugs, update supplier inventory, review doctor orders, verify orders, mark orders as picked up, and review sales reports.<br/>"
        "• Doctors browse available medicines, add items to cart, place orders, and proceed to payment simulation.<br/>"
        "If payment succeeds, the order is placed in Pending status for admin verification. "
        "If payment fails, the system shows an error and releases any reserved medicine stock.",
        style_body
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 7.0 USE CASE DIAGRAM
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("7.0 Use Case Diagram", style_h1, "sec_7"))
    usecase_img_path = os.path.join(DIAGRAMS_DIR, "02_Use_Case_Diagram.jpg")
    if os.path.exists(usecase_img_path):
        story.append(Image(usecase_img_path, width=490, height=319))
        story.append(Paragraph("Figure 7.0 – Use Case Diagram", style_caption))

    story.append(Paragraph("<b>Description</b>", style_body))
    story.append(Paragraph(
        "The use case diagram highlights the interactions between the two primary actors (Doctor and Admin) and the Pharmacy Management System.<br/>"
        "• The Doctor registers, logs in, browses medicines, places prescription orders, simulates payments, and tracks order status.<br/>"
        "• The Admin manages the drug catalog, handles supplier stock inwarding, verifies incoming doctor orders, marks completed orders as picked up, and views financial reports. "
        "User registration and login are shared by both roles.",
        style_body
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 8.0 ARCHITECTURE DIAGRAM
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("8.0 Architecture Diagram", style_h1, "sec_8"))
    arch_img_path = os.path.join(DIAGRAMS_DIR, "01_Solution_Architecture_Diagram.jpg")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=490, height=319))
        story.append(Paragraph("Figure 8.0 – Solution Architecture Diagram", style_caption))

    story.append(Paragraph("<b>Description</b>", style_body))
    story.append(Paragraph(
        "The architecture diagram represents the layered structure of the system:<br/>"
        "1. Presentation Layer: Client applications and Swagger UI submit HTTP requests.<br/>"
        "2. Application Layer: The YARP API Gateway routes incoming requests to five microservices: Auth Service, Inventory Service, Order Service, Payment Service, and SaleReport Service.<br/>"
        "3. Data Layer: Each microservice manages its own private SQL database (User DB, Inventory DB, Order DB, Payment DB, SaleReport DB). Services communicate using REST APIs.",
        style_body
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 9.0 ENTITY-RELATIONSHIP DIAGRAM
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("9.0 Entity-Relationship Diagram", style_h1, "sec_9"))
    er_img_path = os.path.join(DIAGRAMS_DIR, "05_ER_Diagram.jpg")
    if os.path.exists(er_img_path):
        story.append(Image(er_img_path, width=490, height=344))
        story.append(Paragraph("Figure 9.0 – Entity-Relationship Diagram (Database-Per-Service Boxes)", style_caption))

    story.append(Paragraph("<b>Description</b>", style_body))
    story.append(Paragraph(
        "The ER diagram represents the data entities and attributes organized into separate boxes for each database:<br/>"
        "• User DB: Contains the User entity with login, role, and contact attributes.<br/>"
        "• Inventory DB: Contains Drugs, Suppliers, and Inventory entities with supply and stock relationships.<br/>"
        "• Order DB: Contains Orders and OrderItems entities tracking prescription orders.<br/>"
        "• Payment DB: Contains Payments tracking simulated checkout transactions.<br/>"
        "• SaleReport DB: Standalone service containing SaleReports for revenue and profit summaries.<br/>"
        "Physical foreign keys exist only within the same database. Relationships across databases are logical references verified through REST APIs.",
        style_body
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 10.0 DATABASE DIAGRAM
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("10.0 Database Diagram", style_h1, "sec_10"))
    db_img_path = os.path.join(DIAGRAMS_DIR, "06_Database_Schema_Diagram.jpg")
    if os.path.exists(db_img_path):
        story.append(Image(db_img_path, width=490, height=317))
        story.append(Paragraph("Figure 10.0 – Database Schema Diagram", style_caption))

    story.append(Paragraph("<b>Description</b>", style_body))
    story.append(Paragraph(
        "The database diagram illustrates the physical tables, column data types, and primary/foreign keys across all five databases.<br/>"
        "Key tables include Users (credentials and roles), Drugs (pricing, quantities, and minimum stock alerts), Suppliers (vendor contacts), "
        "Inventory (purchase price and supply dates), Orders and OrderItems (prescription line items), Payments (1:1 unique payment records), "
        "and SaleReports (financial totals).<br/>"
        "A unique index on Payment.OrderId prevents duplicate payments for the same order.",
        style_body
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 11.0 CLASS DIAGRAM
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("11.0 Class Diagram", style_h1, "sec_11"))
    cls_img_path = os.path.join(DIAGRAMS_DIR, "03_Class_Diagram.jpg")
    if os.path.exists(cls_img_path):
        story.append(Image(cls_img_path, width=490, height=343))
        story.append(Paragraph("Figure 11.0 – Domain Class Diagram", style_caption))

    story.append(Paragraph("<b>Description</b>", style_body))
    story.append(Paragraph(
        "The class diagram illustrates the object-oriented domain models and their responsibilities:<br/>"
        "• User: Handles authentication, signup, and role identification.<br/>"
        "• Drug: Represents medicine catalog data, selling price, stock levels, and expiry date.<br/>"
        "• Supplier: Manages supplier profiles and vendor associations.<br/>"
        "• Order & OrderItem: Tracks prescription lines, quantities, unit prices, and status updates.<br/>"
        "• Payment: Simulates checkout transactions with 1:1 order enforcement.<br/>"
        "• SaleReport: Aggregates revenue, purchase costs, and profit calculations.<br/>"
        "Dashed lines indicate relationships such as 'places', 'manages', 'supplies', 'contains', and 'paid by'.",
        style_body
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 12.0 SOLUTION STEPS
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("12.0 Solution Steps", style_h1, "sec_12"))

    steps = [
        ("User Registration and Login", [
            "The user submits registration information (name, email, phone number, password, and role).",
            "Auth Service hashes the password securely using PBKDF2 and saves the user record in User DB.",
            "The user logs in with valid email and password credentials.",
            "Auth Service verifies the password hash and returns a signed JWT token containing user ID, email, and role."
        ]),
        ("Admin Manages Drugs and Suppliers", [
            "The Admin logs in and sends the JWT token in the Authorization header.",
            "The Admin creates, updates, or deletes medicines in the Inventory Service, setting selling price and minimum stock quantity.",
            "The Admin adds suppliers and enters incoming medicine stock along with purchase price in the Inventory table.",
            "Medicine catalog and stock data are saved in Inventory DB."
        ]),
        ("Doctor Searches Drugs and Adds to Cart", [
            "The Doctor logs in and queries available medicines through the search endpoints.",
            "Inventory Service returns active medicines that have sufficient stock.",
            "The Doctor selects medicine items, specifies quantities, and adds them to the order cart."
        ]),
        ("Doctor Places Order and Simulates Payment", [
            "The Doctor submits the order payload containing selected medicine items and quantities.",
            "Order Service calls Inventory Service to verify availability and deduct medicine quantities.",
            "Order Service creates the order record in Order DB with status 'Pending' and triggers payment.",
            "Payment Service records the simulated transaction, assigns a unique transaction reference, and sets status to 'Completed'."
        ]),
        ("Admin Verifies Order and Marks PickedUp", [
            "The Admin reviews pending orders submitted by doctors.",
            "The Admin verifies prescription items and updates order status to 'Verified'.",
            "When the medicines are collected, the Admin updates the status to 'PickedUp' in the pickup section."
        ]),
        ("Admin Generates and Downloads Sales Reports", [
            "The Admin selects a reporting range (Daily, Weekly, Monthly, or Yearly).",
            "SaleReport Service aggregates completed orders, calculates revenue, subtracts purchase costs to compute profit, and saves the report.",
            "The Admin can view summary statistics or download the report as a CSV file."
        ])
    ]
    for s_title, s_bullets in steps:
        story.append(Paragraph(s_title, style_h2))
        for b in s_bullets:
            story.append(Paragraph(f"• {b}", style_bullet))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 13.0 CLASSES NAMES
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("13.0 Classes Names", style_h1, "sec_13"))

    story.append(Paragraph("Entities (Models)", style_h2))
    e_rows = [
        [Paragraph("S.No", style_th), Paragraph("Class Name", style_th), Paragraph("Description", style_th)],
        [Paragraph("1", style_td_bold), Paragraph("User.cs", style_td_bold), Paragraph("Represents user account information, password hash, and assigned role (Admin or Doctor).", style_td)],
        [Paragraph("2", style_td_bold), Paragraph("Drug.cs", style_td_bold), Paragraph("Represents medicine details, description, selling price, expiry date, quantity, and minimum stock limit.", style_td)],
        [Paragraph("3", style_td_bold), Paragraph("Supplier.cs", style_td_bold), Paragraph("Represents supplier contact information, email, phone number, and address.", style_td)],
        [Paragraph("4", style_td_bold), Paragraph("Inventory.cs", style_td_bold), Paragraph("Represents incoming stock shipments, purchase prices, supply dates, and supplier links.", style_td)],
        [Paragraph("5", style_td_bold), Paragraph("Order.cs", style_td_bold), Paragraph("Represents prescription orders placed by doctors, order date, total amount, and status.", style_td)],
        [Paragraph("6", style_td_bold), Paragraph("OrderItem.cs", style_td_bold), Paragraph("Represents individual medicine line items belonging to an order with unit price.", style_td)],
        [Paragraph("7", style_td_bold), Paragraph("Payment.cs", style_td_bold), Paragraph("Represents simulated payment records with 1:1 order linking and transaction references.", style_td)],
        [Paragraph("8", style_td_bold), Paragraph("SaleReport.cs", style_td_bold), Paragraph("Represents financial sales reports, total order counts, revenue, and profit calculations.", style_td)]
    ]
    t_e = Table(e_rows, colWidths=[35, 145, 320])
    t_e.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_e)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Controllers (API Layer)", style_h2))
    c_rows = [
        [Paragraph("S.No", style_th), Paragraph("Class Name", style_th), Paragraph("Description", style_th)],
        [Paragraph("1", style_td_bold), Paragraph("AuthController.cs", style_td_bold), Paragraph("Handles user registration, login, and profile retrieval APIs.", style_td)],
        [Paragraph("2", style_td_bold), Paragraph("DrugsController.cs", style_td_bold), Paragraph("Handles drug catalog search, drug creation, updates, and low-stock alerts.", style_td)],
        [Paragraph("3", style_td_bold), Paragraph("SuppliersController.cs", style_td_bold), Paragraph("Handles supplier registration, retrieval, and profile updates.", style_td)],
        [Paragraph("4", style_td_bold), Paragraph("InventoryController.cs", style_td_bold), Paragraph("Handles stock inward shipments, batch updates, and stock deduction.", style_td)],
        [Paragraph("5", style_td_bold), Paragraph("OrdersController.cs", style_td_bold), Paragraph("Handles order creation, status tracking, admin verification, and pickup handover.", style_td)],
        [Paragraph("6", style_td_bold), Paragraph("PaymentsController.cs", style_td_bold), Paragraph("Handles checkout payment simulation and transaction verification.", style_td)],
        [Paragraph("7", style_td_bold), Paragraph("SaleReportsController.cs", style_td_bold), Paragraph("Handles sales report generation, profit analytics, and CSV download APIs.", style_td)]
    ]
    t_c = Table(c_rows, colWidths=[35, 145, 320])
    t_c.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_c)
    story.append(PageBreak())

    story.append(Paragraph("Services (Business Logic)", style_h2))
    s_rows = [
        [Paragraph("S.No", style_th), Paragraph("Class Name", style_th), Paragraph("Description", style_th)],
        [Paragraph("1", style_td_bold), Paragraph("AuthService.cs", style_td_bold), Paragraph("Implements user registration, password verification, and login logic.", style_td)],
        [Paragraph("2", style_td_bold), Paragraph("TokenService.cs", style_td_bold), Paragraph("Generates signed JWT tokens with user claims and expiration.", style_td)],
        [Paragraph("3", style_td_bold), Paragraph("DrugService.cs", style_td_bold), Paragraph("Handles medicine availability checks, stock updates, and low-stock alerts.", style_td)],
        [Paragraph("4", style_td_bold), Paragraph("SupplierService.cs", style_td_bold), Paragraph("Manages supplier records, contact updates, and vendor associations.", style_td)],
        [Paragraph("5", style_td_bold), Paragraph("OrderService.cs", style_td_bold), Paragraph("Coordinates order creation, stock reservation, verification, and handover.", style_td)],
        [Paragraph("6", style_td_bold), Paragraph("PaymentService.cs", style_td_bold), Paragraph("Simulates payment processing and enforces 1:1 transaction rules.", style_td)],
        [Paragraph("7", style_td_bold), Paragraph("SaleReportService.cs", style_td_bold), Paragraph("Computes revenue, purchase costs, profit, and builds CSV report files.", style_td)]
    ]
    t_s = Table(s_rows, colWidths=[35, 145, 320])
    t_s.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_s)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Repositories (Data Access Layer)", style_h2))
    r_rows = [
        [Paragraph("S.No", style_th), Paragraph("Class Name", style_th), Paragraph("Description", style_th)],
        [Paragraph("1", style_td_bold), Paragraph("UserRepository.cs", style_td_bold), Paragraph("Manages database operations for user accounts in User DB.", style_td)],
        [Paragraph("2", style_td_bold), Paragraph("DrugRepository.cs", style_td_bold), Paragraph("Handles CRUD database queries for medicines in Inventory DB.", style_td)],
        [Paragraph("3", style_td_bold), Paragraph("SupplierRepository.cs", style_td_bold), Paragraph("Manages database queries for supplier records in Inventory DB.", style_td)],
        [Paragraph("4", style_td_bold), Paragraph("InventoryRepository.cs", style_td_bold), Paragraph("Manages stock inward entries and batch history in Inventory DB.", style_td)],
        [Paragraph("5", style_td_bold), Paragraph("OrderRepository.cs", style_td_bold), Paragraph("Handles order and order item queries with EF Core in Order DB.", style_td)],
        [Paragraph("6", style_td_bold), Paragraph("PaymentRepository.cs", style_td_bold), Paragraph("Saves and queries payment records with unique order IDs in Payment DB.", style_td)],
        [Paragraph("7", style_td_bold), Paragraph("SaleReportRepository.cs", style_td_bold), Paragraph("Stores and queries sales summary records in SaleReport DB.", style_td)]
    ]
    t_r = Table(r_rows, colWidths=[35, 145, 320])
    t_r.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_r)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 14.0 & 15.0
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("14.0 Validations", style_h1, "sec_14"))
    story.append(Paragraph("• User Input Validations: Ensure required fields (name, valid email format, contact phone number, password length) are provided.", style_bullet))
    story.append(Paragraph("• Role Authorization: Ensure only Admin can add/edit drugs, manage suppliers, verify orders, and view sales reports.", style_bullet))
    story.append(Paragraph("• Doctor Isolation: Ensure Doctors can only view and manage their own orders.", style_bullet))
    story.append(Paragraph("• Stock Availability: Verify that requested medicine quantities do not exceed available stock before creating an order.", style_bullet))
    story.append(Paragraph("• Low Stock Trigger: Automatically identify medicines whose stock is at or below MinimumStockQuantity.", style_bullet))
    story.append(Paragraph("• Expiry Validation: Prevent selling medicines that have passed their expiration date.", style_bullet))
    story.append(Paragraph("• Order Status Flow: Orders progress through Cart -> Pending -> Verified -> PickedUp (or Cancelled).", style_bullet))
    story.append(Paragraph("• 1:1 Payment Rule: Exactly one payment is allowed per order. Duplicate payments for the same order are rejected.", style_bullet))
    story.append(Paragraph("• Token Security: Every protected API validates JWT signature, issuer, expiration, and role claims.", style_bullet))
    story.append(Spacer(1, 10))

    story.append(TrackedParagraph("15.0 API Catalogue", style_h1, "sec_15"))
    story.append(Paragraph("The table below lists all endpoints exposed by the microservices (routed through YARP API Gateway):", style_body))

    api_rows = [
        [Paragraph("Module", style_th), Paragraph("Endpoint", style_th), Paragraph("Method", style_th), Paragraph("Access", style_th)],
        [Paragraph("Auth", style_td_bold), Paragraph("/api/auth/register", style_td), Paragraph("POST", style_td), Paragraph("Public", style_td)],
        [Paragraph("Auth", style_td_bold), Paragraph("/api/auth/login", style_td), Paragraph("POST", style_td), Paragraph("Public", style_td)],
        [Paragraph("Auth", style_td_bold), Paragraph("/api/auth/me", style_td), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/drugs", style_td), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/drugs/{id}", style_td), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/drugs", style_td), Paragraph("POST", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/drugs/{id}", style_td), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/drugs/{id}", style_td), Paragraph("DELETE", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/drugs/low-stock", style_td), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/suppliers", style_td), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/suppliers", style_td), Paragraph("POST", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td_bold), Paragraph("/api/inventory/inward", style_td), Paragraph("POST", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders", style_td), Paragraph("POST", style_td), Paragraph("Doctor", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders", style_td), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders/my-orders", style_td), Paragraph("GET", style_td), Paragraph("Doctor", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders/{id}", style_td), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders/{id}/verify", style_td), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders/{id}/pickup", style_td), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Order", style_td_bold), Paragraph("/api/orders/{id}/cancel", style_td), Paragraph("PUT", style_td), Paragraph("Doctor / Admin", style_td)],
        [Paragraph("Payment", style_td_bold), Paragraph("/api/payments/simulate", style_td), Paragraph("POST", style_td), Paragraph("Doctor / Internal", style_td)],
        [Paragraph("SaleReport", style_td_bold), Paragraph("/api/salereports/generate", style_td), Paragraph("POST", style_td), Paragraph("Admin", style_td)]
    ]
    t_api = Table(api_rows, colWidths=[80, 240, 60, 120])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_api)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 16.0 & 17.0
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("16.0 HTTP Status Codes", style_h1, "sec_16"))
    stat_rows = [
        [Paragraph("Status Code", style_th), Paragraph("Status", style_th), Paragraph("Description", style_th)],
        [Paragraph("200", style_td_bold), Paragraph("OK", style_td_bold), Paragraph("The request succeeded and returned the requested data.", style_td)],
        [Paragraph("201", style_td_bold), Paragraph("Created", style_td_bold), Paragraph("A new user, drug, order, payment, or report was created successfully.", style_td)],
        [Paragraph("204", style_td_bold), Paragraph("No Content", style_td_bold), Paragraph("The request succeeded and no response body is needed (e.g. deletion).", style_td)],
        [Paragraph("400", style_td_bold), Paragraph("Bad Request", style_td_bold), Paragraph("The request is invalid, missing data, or failed validation checks.", style_td)],
        [Paragraph("401", style_td_bold), Paragraph("Unauthorized", style_td_bold), Paragraph("The JWT token is missing, expired, or invalid.", style_td)],
        [Paragraph("403", style_td_bold), Paragraph("Forbidden", style_td_bold), Paragraph("The user does not have permission for this action (e.g. Doctor calling Admin API).", style_td)],
        [Paragraph("404", style_td_bold), Paragraph("Not Found", style_td_bold), Paragraph("The requested drug, order, supplier, or user record was not found.", style_td)],
        [Paragraph("409", style_td_bold), Paragraph("Conflict", style_td_bold), Paragraph("A conflict occurred, such as duplicate email or duplicate payment for an order.", style_td)],
        [Paragraph("500", style_td_bold), Paragraph("Internal Server Error", style_td_bold), Paragraph("An unexpected error occurred while processing the request.", style_td)]
    ]
    t_stat = Table(stat_rows, colWidths=[75, 105, 320])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_stat)
    story.append(Spacer(1, 10))

    story.append(TrackedParagraph("17.0 Integrations", style_h1, "sec_17"))
    story.append(Paragraph("• YARP API Gateway: Provides a central entry point and routes client requests to the appropriate microservice.", style_bullet))
    story.append(Paragraph("• REST APIs: Enable synchronous communication between Order, Inventory, and Payment services using typed HTTP clients.", style_bullet))
    story.append(Paragraph("• JWT Bearer Authentication: Secures APIs with signed tokens and supports role-based access for Admin and Doctor.", style_bullet))
    story.append(Paragraph("• SQL Server 2022: Maintains five separate databases ensuring data isolation per service.", style_bullet))
    story.append(Paragraph("• Entity Framework Core 8: Manages database access, Code-First mappings, and schema updates.", style_bullet))
    story.append(Paragraph("• Swagger UI & OpenAPI: Provide interactive API documentation and testing for all microservices.", style_bullet))
    story.append(Paragraph("• NUnit & Moq: Automated unit test suite verifying service layer logic using mocked dependencies.", style_bullet))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 18.0 & 19.0
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("18.0 Sample API Requests", style_h1, "sec_18"))
    story.append(Paragraph("Sample POST request to create an order (/api/orders):", style_body))

    req_code = (
        "{\n"
        '  "doctorId": 2,\n'
        '  "items": [\n'
        "    {\n"
        '      "drugId": 1,\n'
        '      "drugName": "Paracetamol 500mg",\n'
        '      "quantity": 2,\n'
        '      "unitPrice": 9.99\n'
        "    },\n"
        "    {\n"
        '      "drugId": 3,\n'
        '      "drugName": "Ibuprofen 400mg",\n'
        '      "quantity": 1,\n'
        '      "unitPrice": 12.00\n'
        "    }\n"
        "  ]\n"
        "}"
    )
    t_box_req = Table([[Paragraph(f"<pre>{req_code}</pre>", ParagraphStyle('CodeBox', parent=styles['Normal'], fontName='Courier', fontSize=8, leading=10.5))]], colWidths=[500])
    t_box_req.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_box_req)
    story.append(Spacer(1, 15))

    story.append(TrackedParagraph("19.0 Sample API Responses", style_h1, "sec_19"))
    story.append(Paragraph("Successful response returned after order creation:", style_body))

    res_code = (
        "{\n"
        '  "statusCode": 201,\n'
        '  "message": "Order created successfully",\n'
        '  "data": {\n'
        '    "orderId": 101,\n'
        '    "doctorId": 2,\n'
        '    "orderDate": "2026-11-19T10:30:00Z",\n'
        '    "totalAmount": 31.98,\n'
        '    "status": "Pending",\n'
        '    "orderItems": [\n'
        "      {\n"
        '        "orderItemId": 201,\n'
        '        "drugId": 1,\n'
        '        "drugName": "Paracetamol 500mg",\n'
        '        "quantity": 2,\n'
        '        "unitPrice": 9.99\n'
        "      },\n"
        "      {\n"
        '        "orderItemId": 202,\n'
        '        "drugId": 3,\n'
        '        "drugName": "Ibuprofen 400mg",\n'
        '        "quantity": 1,\n'
        '        "unitPrice": 12.00\n'
        "      }\n"
        "    ]\n"
        "  }\n"
        "}"
    )
    t_box_res = Table([[Paragraph(f"<pre>{res_code}</pre>", ParagraphStyle('CodeBoxRes', parent=styles['Normal'], fontName='Courier', fontSize=8, leading=10.5))]], colWidths=[500])
    t_box_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_box_res)
    story.append(Paragraph("<b>Status Code: 201 Created</b>", style_body))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 20.0 NUNIT UNIT TESTING
    # --------------------------------------------------------------------------
    story.append(TrackedParagraph("20.0 NUnit Unit Testing", style_h1, "sec_20"))
    story.append(Paragraph("The unit testing suite validates key business logic and error scenarios using NUnit and Moq:", style_body))

    test_rows = [
        [Paragraph("Test Case ID", style_th), Paragraph("Module", style_th), Paragraph("Test Scenario", style_th), Paragraph("Expected Result", style_th)],
        [Paragraph("TC-01", style_td_bold), Paragraph("Auth", style_td), Paragraph("Register user with valid details.", style_td), Paragraph("User is created with hashed password and role.", style_td)],
        [Paragraph("TC-02", style_td_bold), Paragraph("Auth", style_td), Paragraph("Register with duplicate email.", style_td), Paragraph("Registration fails with a duplicate email error.", style_td)],
        [Paragraph("TC-03", style_td_bold), Paragraph("Auth", style_td), Paragraph("Login with valid credentials.", style_td), Paragraph("Login succeeds and returns a signed JWT token.", style_td)],
        [Paragraph("TC-04", style_td_bold), Paragraph("Auth", style_td), Paragraph("Login with incorrect password.", style_td), Paragraph("Login fails with 401 Unauthorized.", style_td)],
        [Paragraph("TC-05", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Add medicine with valid details.", style_td), Paragraph("Medicine is saved with price and stock count.", style_td)],
        [Paragraph("TC-06", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Add medicine with negative price.", style_td), Paragraph("Validation fails with 400 Bad Request.", style_td)],
        [Paragraph("TC-07", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Update medicine price and stock.", style_td), Paragraph("Medicine record is updated successfully in SQL.", style_td)],
        [Paragraph("TC-08", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Query medicines below min stock.", style_td), Paragraph("Returns medicines where quantity <= min stock level.", style_td)],
        [Paragraph("TC-09", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Deduct stock when sufficient.", style_td), Paragraph("Medicine stock is reduced by requested quantity.", style_td)],
        [Paragraph("TC-10", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Deduct stock when insufficient.", style_td), Paragraph("Throws exception and stock remains unchanged.", style_td)],
        [Paragraph("TC-11", style_td_bold), Paragraph("Order", style_td), Paragraph("Create order with valid items.", style_td), Paragraph("Order is created in Pending status with total.", style_td)],
        [Paragraph("TC-12", style_td_bold), Paragraph("Order", style_td), Paragraph("Create order with empty cart.", style_td), Paragraph("Validation fails with 400 Bad Request.", style_td)],
        [Paragraph("TC-13", style_td_bold), Paragraph("Order", style_td), Paragraph("Doctor views own order history.", style_td), Paragraph("Returns only orders matching logged-in doctor ID.", style_td)],
        [Paragraph("TC-14", style_td_bold), Paragraph("Order", style_td), Paragraph("Admin verifies pending order.", style_td), Paragraph("Order status changes from 'Pending' to 'Verified'.", style_td)],
        [Paragraph("TC-15", style_td_bold), Paragraph("Order", style_td), Paragraph("Admin marks order as picked up.", style_td), Paragraph("Order status updates to 'PickedUp' in pickup section.", style_td)],
        [Paragraph("TC-16", style_td_bold), Paragraph("Order", style_td), Paragraph("Doctor cancels order before pickup.", style_td), Paragraph("Order status updates to 'Cancelled' and stock is released.", style_td)],
        [Paragraph("TC-17", style_td_bold), Paragraph("Payment", style_td), Paragraph("Simulate payment for pending order.", style_td), Paragraph("Payment record created with status 'Completed'.", style_td)],
        [Paragraph("TC-18", style_td_bold), Paragraph("Payment", style_td), Paragraph("Simulate duplicate payment.", style_td), Paragraph("Rejected due to 1:1 unique constraint on OrderId.", style_td)],
        [Paragraph("TC-19", style_td_bold), Paragraph("SaleReport", style_td), Paragraph("Generate report for date range.", style_td), Paragraph("Calculates total orders, total revenue, and profit.", style_td)],
        [Paragraph("TC-20", style_td_bold), Paragraph("SaleReport", style_td), Paragraph("Export sales report to CSV.", style_td), Paragraph("Generates CSV file byte array for download.", style_td)]
    ]
    t_test = Table(test_rows, colWidths=[60, 80, 180, 180])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_test)

    return story

def build_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_path = output_path + ".tmp.pdf"

    # Pass 1: Compute section page numbers
    doc_pass1 = SimpleDocTemplate(
        temp_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    story1 = build_pdf_story({})
    doc_pass1.build(story1, canvasmaker=NumberedCanvas)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Pass 2: Compile final PDF with accurate dynamic TOC page numbers
    doc_pass2 = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    story2 = build_pdf_story(SECTION_PAGE_MAP)
    doc_pass2.build(story2, canvasmaker=NumberedCanvas)
    print(f"Generated LLD PDF successfully: {output_path}")

if __name__ == "__main__":
    build_pdf(WORKSPACE_PDF)
    build_pdf(ARTIFACT_PDF)
