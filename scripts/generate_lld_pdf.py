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

# Corporate Color Palette (Matching TechBuddy Reference PDF)
COLOR_PRIMARY = colors.HexColor("#004F7A")      # TechBuddy deep teal / blue
COLOR_SECONDARY = colors.HexColor("#1A5276")    # Medium navy
COLOR_DARK = colors.HexColor("#1E293B")         # Charcoal body text
COLOR_LIGHT_BG = colors.HexColor("#F1F5F9")     # Table header light slate
COLOR_ALT_BG = colors.HexColor("#F8FAFC")       # Alternating row background
COLOR_BORDER = colors.HexColor("#CBD5E1")       # Clean table border
COLOR_ACCENT = colors.HexColor("#059669")       # Success green accent
COLOR_MUTED = colors.HexColor("#64748B")        # Subtext muted gray

# Global dictionary to track section page numbers
SECTION_PAGE_MAP = {}

class TrackedParagraph(Paragraph):
    """Tracks the exact page number where a section heading is rendered."""
    def __init__(self, text, style, section_id):
        super().__init__(text, style)
        self.section_id = section_id

    def draw(self):
        SECTION_PAGE_MAP[self.section_id] = self.canv._pageNumber
        super().draw()

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count in footers,
    skipping the cover page.
    """
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

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_MUTED)
            self.drawString(40, 755, "Pharmacy Management System - Low Level Design (LLD)")
            self.drawRightString(572, 755, "Microservices Architecture (.NET 8 & SQL Server)")
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.5)
            self.line(40, 748, 572, 748)

            # Running Footer
            self.line(40, 45, 572, 45)
            self.setFont("Helvetica", 8)
            self.drawString(40, 32, "Confidential - For Internal Use Only")
            self.drawRightString(572, 32, f"Page {self._pageNumber} of {page_count}")
            
            self.restoreState()

def build_pdf_story(toc_page_map=None):
    styles = getSampleStyleSheet()

    # Custom Typography Styles
    style_cover_title = ParagraphStyle(
        "CoverTitle", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=26, leading=32,
        textColor=COLOR_PRIMARY, alignment=1
    )
    style_cover_sub = ParagraphStyle(
        "CoverSub", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=18, leading=24,
        textColor=COLOR_SECONDARY, alignment=1
    )
    style_cover_desc = ParagraphStyle(
        "CoverDesc", parent=styles["Normal"],
        fontName="Helvetica", fontSize=14, leading=20,
        textColor=COLOR_DARK, alignment=1
    )
    style_cover_meta = ParagraphStyle(
        "CoverMeta", parent=styles["Normal"],
        fontName="Helvetica", fontSize=11, leading=16,
        textColor=COLOR_DARK
    )
    style_cover_author = ParagraphStyle(
        "CoverAuthor", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=12, leading=16,
        textColor=COLOR_DARK, alignment=2
    )

    style_section_h1 = ParagraphStyle(
        "SectionH1", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=15, leading=19,
        textColor=COLOR_PRIMARY, spaceBefore=12, spaceAfter=8,
        keepWithNext=True
    )
    style_section_h2 = ParagraphStyle(
        "SectionH2", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=11.5, leading=15,
        textColor=COLOR_SECONDARY, spaceBefore=8, spaceAfter=4,
        keepWithNext=True
    )
    style_desc_heading = ParagraphStyle(
        "DescHeading", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=11, leading=15,
        textColor=COLOR_PRIMARY, spaceBefore=6, spaceAfter=3,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9, leading=13.5,
        textColor=COLOR_DARK, spaceBefore=3, spaceAfter=4
    )
    style_bullet = ParagraphStyle(
        "Bullet", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9, leading=13.5,
        textColor=COLOR_DARK, leftIndent=14, firstLineIndent=-9,
        spaceBefore=2, spaceAfter=2
    )
    style_th = ParagraphStyle(
        "TableHeader", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=8.5, leading=11.5,
        textColor=COLOR_DARK, alignment=0
    )
    style_td = ParagraphStyle(
        "TableCell", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8, leading=11,
        textColor=COLOR_DARK
    )
    style_td_bold = ParagraphStyle(
        "TableCellBold", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=8, leading=11,
        textColor=COLOR_DARK
    )
    style_code = ParagraphStyle(
        "CodeText", parent=styles["Normal"],
        fontName="Courier", fontSize=7.5, leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("PHARMACY MANAGEMENT SYSTEM", style_cover_title))
    story.append(Spacer(1, 15))
    story.append(Paragraph("POC", style_cover_sub))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Low Level Design (LLD)", style_cover_desc))
    
    story.append(Spacer(1, 260))
    
    meta_text = (
        "<b>Pharmacy Management System Microservices</b><br/>"
        "POC – Low Level Design (LLD)<br/><br/>"
        "<b>Date:</b> 18/11/2026<br/>"
        "<b>Current Document Version:</b> [1.0]"
    )
    author_text = "<b>Author:</b><br/>Lahari Chikoti"
    
    cover_meta_table = Table(
        [
            [Paragraph(meta_text, style_cover_meta), Paragraph(author_text, style_cover_author)]
        ],
        colWidths=[340, 192]
    )
    cover_meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(cover_meta_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: DOCUMENT APPROVAL, CHANGE HISTORY & TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("DOCUMENT APPROVAL Approvers of this document", style_section_h2))
    approval_data = [
        [Paragraph("<b>Name</b>", style_th), Paragraph("<b>Department</b>", style_th), Paragraph("<b>Role</b>", style_th), Paragraph("<b>Signature</b>", style_th), Paragraph("<b>Date</b>", style_th)],
        [Paragraph("Technical Review Board", style_td), Paragraph("Architecture & Engineering", style_td), Paragraph("Lead Architect", style_td), Paragraph("Approved", style_td), Paragraph("18/11/2026", style_td)],
        [Paragraph("Solution Lead", style_td), Paragraph(".NET Practice", style_td), Paragraph("Solutions Lead", style_td), Paragraph("Approved", style_td), Paragraph("18/11/2026", style_td)],
        [Paragraph("Project Manager", style_td), Paragraph("Healthcare Deliveries", style_td), Paragraph("Delivery Manager", style_td), Paragraph("Approved", style_td), Paragraph("18/11/2026", style_td)]
    ]
    t_approval = Table(approval_data, colWidths=[120, 130, 110, 90, 82])
    t_approval.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_approval)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Document Change History", style_section_h2))
    history_data = [
        [Paragraph("<b>Document Version #</b>", style_th), Paragraph("<b>Author</b>", style_th), Paragraph("<b>Date</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("1.0", style_td), Paragraph("Lahari Chikoti", style_td), Paragraph("18/11/2026", style_td), Paragraph("Pharmacy Management System Low Level Design (LLD)", style_td)]
    ]
    t_history = Table(history_data, colWidths=[120, 110, 90, 212])
    t_history.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_history)
    story.append(Spacer(1, 10))

    # Helper function to get page string from toc_page_map
    def pg(sid, fallback):
        if toc_page_map and sid in toc_page_map:
            return str(toc_page_map[sid])
        return str(fallback)

    # Table of Contents Table
    story.append(Paragraph("Table of Contents", style_cover_sub))
    story.append(Spacer(1, 4))
    toc_data = [
        [Paragraph("<b>Section</b>", style_th), Paragraph("<b>Title</b>", style_th), Paragraph("<b>Page No.</b>", style_th)],
        [Paragraph("1.0", style_td), Paragraph("Document Purpose", style_td), Paragraph(pg("sec_1", 3), style_td)],
        [Paragraph("2.0", style_td), Paragraph("Intended Audience", style_td), Paragraph(pg("sec_2", 3), style_td)],
        [Paragraph("3.0", style_td), Paragraph("Project Background and Objectives", style_td), Paragraph(pg("sec_3", 4), style_td)],
        [Paragraph("4.0", style_td), Paragraph("Requirements", style_td), Paragraph(pg("sec_4", 4), style_td)],
        [Paragraph("5.0", style_td), Paragraph("Design Patterns", style_td), Paragraph(pg("sec_5", 6), style_td)],
        [Paragraph("6.0", style_td), Paragraph("Flow Diagram", style_td), Paragraph(pg("sec_6", 7), style_td)],
        [Paragraph("7.0", style_td), Paragraph("Use Case Diagram", style_td), Paragraph(pg("sec_7", 8), style_td)],
        [Paragraph("8.0", style_td), Paragraph("Architecture Diagram", style_td), Paragraph(pg("sec_8", 9), style_td)],
        [Paragraph("9.0", style_td), Paragraph("Entity-Relationship Diagram", style_td), Paragraph(pg("sec_9", 10), style_td)],
        [Paragraph("10.0", style_td), Paragraph("Database Diagram", style_td), Paragraph(pg("sec_10", 11), style_td)],
        [Paragraph("11.0", style_td), Paragraph("Sequence Diagram", style_td), Paragraph(pg("sec_11", 12), style_td)],
        [Paragraph("12.0", style_td), Paragraph("Solution Steps", style_td), Paragraph(pg("sec_12", 13), style_td)],
        [Paragraph("13.0", style_td), Paragraph("Classes Names", style_td), Paragraph(pg("sec_13", 15), style_td)],
        [Paragraph("14.0", style_td), Paragraph("Validations", style_td), Paragraph(pg("sec_14", 17), style_td)],
        [Paragraph("15.0", style_td), Paragraph("API Catalogue", style_td), Paragraph(pg("sec_15", 18), style_td)],
        [Paragraph("16.0", style_td), Paragraph("HTTP Status Codes", style_td), Paragraph(pg("sec_16", 20), style_td)],
        [Paragraph("17.0", style_td), Paragraph("Integrations", style_td), Paragraph(pg("sec_17", 20), style_td)],
        [Paragraph("18.0", style_td), Paragraph("Sample API Requests", style_td), Paragraph(pg("sec_18", 21), style_td)],
        [Paragraph("19.0", style_td), Paragraph("Sample API Responses", style_td), Paragraph(pg("sec_19", 21), style_td)],
        [Paragraph("20.0", style_td), Paragraph("Unit Testing", style_td), Paragraph(pg("sec_20", 22), style_td)]
    ]
    t_toc = Table(toc_data, colWidths=[60, 400, 72])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 1.0 & 2.0
    # =========================================================================
    story.append(TrackedParagraph("1.0 Document Purpose", style_section_h1, "sec_1"))
    story.append(Paragraph(
        "This document describes the <b>Low-Level Design (LLD)</b> of the <b>Pharmacy Management System POC</b>, "
        "developed using <b>C#, ASP.NET Core Web API, .NET 8, Entity Framework Core, LINQ, and Microsoft SQL Server</b> "
        "under a distributed <b>Microservices Architecture</b>. It defines the internal MVC service structures, REST APIs, "
        "database-per-service isolation, authentication and role-based access control (RBAC), transactional integrity rules, "
        "and testing verification approach through interactive Swagger UI.",
        style_body
    ))
    story.append(Paragraph(
        "The system consists of five decoupled services: <b>Auth Service</b>, <b>Inventory Service</b>, <b>Order Service</b>, "
        "<b>Payment Service</b>, and <b>SaleReport Service</b>. Each service encapsulates its own bounded context and database, "
        "exposing RESTful endpoints consumed by clinical staff, dispensing doctors, administrators, and external consumers.",
        style_body
    ))
    story.append(Spacer(1, 8))

    story.append(TrackedParagraph("2.0 Intended Audience", style_section_h1, "sec_2"))
    story.append(Paragraph("This document is intended as a technical reference for the following stakeholders:", style_body))
    
    audience_data = [
        [Paragraph("<b>Role</b>", style_th), Paragraph("<b>Nature of Engagement in Pharmacy Management System Architecture</b>", style_th)],
        [Paragraph("Product Owners / SMEs", style_td_bold), Paragraph("Ensure that the microservices design aligns strictly with pharmacy dispensing regulations, stock safety, and administrative workflows.", style_td)],
        [Paragraph("Business Analysts", style_td_bold), Paragraph("Map clinical and administrative requirements into technical service endpoints and entity specifications.", style_td)],
        [Paragraph("Enterprise Architects", style_td_bold), Paragraph("Review architectural consistency, database isolation boundaries, and inter-service HTTP REST communication standards.", style_td)],
        [Paragraph("Solution Architects", style_td_bold), Paragraph("Validate security patterns, JWT token issuance, EF Core LINQ query performance, and transactional boundaries.", style_td)],
        [Paragraph("Developers", style_td_bold), Paragraph("Use this document as an authoritative technical blueprint for implementing controllers, services, repositories, DTOs, and unit tests.", style_td)]
    ]
    t_aud = Table(audience_data, colWidths=[140, 392])
    t_aud.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_aud)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 3.0 & 4.0
    # =========================================================================
    story.append(TrackedParagraph("3.0 Project Background and Objectives", style_section_h1, "sec_3"))
    story.append(Paragraph("3.1 Project Background", style_section_h2))
    story.append(Paragraph(
        "The <b>Pharmacy Management System</b> is an enterprise backend application engineered to modernize medication dispensing, "
        "wholesale pharmaceutical procurement, prescription order tracking, and financial analytics. Operating in clinical healthcare "
        "environments, the system enables <b>Doctor users</b> to browse medication catalogs with real-time stock availability, "
        "view unit prices, and place prescription drug orders. Simultaneously, <b>Admin users</b> maintain full control over the "
        "formulary (adding, editing, and deleting drugs), manage certified wholesale pharmaceutical suppliers, track batch purchase prices, "
        "verify doctor orders, mark completed patient counter collections in the 'PickedUp' section, and generate comprehensive sales "
        "and net profit reports.",
        style_body
    ))
    story.append(Paragraph(
        "The application is structured into five independent microservices: <b>Auth Service</b>, <b>Inventory Service</b>, "
        "<b>Order Service</b>, <b>Payment Service</b>, and <b>SaleReport Service</b>. In accordance with microservices best practices, "
        "each microservice owns its dedicated database, preventing cross-database query coupling and enabling independent deployment.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3.2 Project Objective", style_section_h2))
    story.append(Paragraph(
        "The primary objective is to deliver a robust, scalable, and maintainable backend using <b>.NET 8, C# 12, Entity Framework Core, "
        "LINQ, and Microsoft SQL Server 2022</b>. Key goals include:",
        style_body
    ))
    story.append(Paragraph("• <b>Domain Isolation:</b> Strict enforcement of the Database-per-Service pattern with zero cross-database joins.", style_bullet))
    story.append(Paragraph("• <b>Internal MVC Separation:</b> Controllers expose clean REST contracts, Services enforce business rules, and Repositories execute LINQ queries.", style_bullet))
    story.append(Paragraph("• <b>Stateless Security:</b> Cryptographically signed JWT tokens with Role Claims (`Admin` vs `Doctor`) protecting critical endpoints.", style_bullet))
    story.append(Paragraph("• <b>Data Consistency:</b> Atomic quantity decrementing during ordering, 1:1 unique payment enforcement, and immutable financial aggregation.", style_bullet))
    story.append(Paragraph("• <b>Testing & Documentation:</b> Complete Swagger / OpenAPI 3.0 integration for interactive API validation without requiring a frontend.", style_bullet))
    story.append(Spacer(1, 6))

    story.append(TrackedParagraph("4.0 Requirements", style_section_h1, "sec_4"))
    story.append(Paragraph("4.1 Functional Requirements (FR)", style_section_h2))
    story.append(Paragraph("<b>For Admin Users:</b>", style_body))
    story.append(Paragraph("1. <b>Login / Signup:</b> Secure registration and authentication with Name, Contact, Email, Password, and Role assignment.", style_bullet))
    story.append(Paragraph("2. <b>View Drugs:</b> Query and inspect complete catalog details including Drug Name, Description, Selling Price, Expiry Date, Quantity, and Availability.", style_bullet))
    story.append(Paragraph("3. <b>Add / Edit / Delete Drugs:</b> Full lifecycle formulary management with price validation and duplicate prevention.", style_bullet))
    story.append(Paragraph("4. <b>View Suppliers:</b> Query registered pharmaceutical suppliers, contact emails, phone numbers, and physical addresses.", style_bullet))
    story.append(Paragraph("5. <b>Add / Edit / Delete Suppliers:</b> Vendor management to record verified wholesale distributors.", style_bullet))
    story.append(Paragraph("6. <b>View Doctor Orders:</b> Inspect orders submitted by all doctors, including items, unit prices, doctor identity, and timestamps.", style_bullet))
    story.append(Paragraph("7. <b>Verify Orders:</b> Inspect order line items and update order status from `Pending` to `Verified` upon clinical validation.", style_bullet))
    story.append(Paragraph("8. <b>Add Order to PickedUp Section:</b> Confirm counter collection and move verified orders to the fulfilled `PickedUp` state.", style_bullet))
    story.append(Paragraph("9. <b>View Sales Reports:</b> Query financial performance aggregated across Daily, Weekly, Monthly, and Yearly intervals.", style_bullet))
    story.append(Paragraph("10. <b>Download / Print Sales Report:</b> Export financial data as downloadable CSV spreadsheets or formatted printable receipt views.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>For Doctor Users:</b>", style_body))
    story.append(Paragraph("1. <b>Login / Signup:</b> Register with Name, Contact, Email, and Password to obtain Doctor privileges.", style_bullet))
    story.append(Paragraph("2. <b>View Drugs:</b> Browse active medication formularies with live stock levels and pricing.", style_bullet))
    story.append(Paragraph("3. <b>Buy Drugs:</b> Place orders containing single or multiple medications, staging items in Cart/Pending status.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2 Non-Functional Requirements (NFR)", style_section_h2))
    story.append(Paragraph("• <b>Architecture:</b> Microservices architecture with independent compilation, lifecycle, and dedicated databases.", style_bullet))
    story.append(Paragraph("• <b>Security:</b> PBKDF2 with SHA-256 password hashing (100,000 iterations); HMAC-SHA256 signed JWT Bearer authentication.", style_bullet))
    story.append(Paragraph("• <b>Data Precision:</b> Monetary calculations (Selling Price, Purchase Price, Total Amount, Revenue, Profit) use `DECIMAL(18,2)`.", style_bullet))
    story.append(Paragraph("• <b>Time Precision:</b> All audit timestamps are recorded in UTC using `DATETIME2(7)`.", style_bullet))
    story.append(Paragraph("• <b>API Standardization:</b> Unified `ApiResponse<T>` envelope across all services returning `Success`, `Message`, `Data`, and `Errors`.", style_bullet))
    story.append(Paragraph("• <b>Interactive Verification:</b> Full Swagger / OpenAPI 3.0 UI with Bearer Token Authorize button on every microservice.", style_bullet))
    story.append(PageBreak())

    # Technology Stack Table
    story.append(Paragraph("4.3 Technology Stack", style_section_h2))
    tech_data = [
        [Paragraph("<b>Category</b>", style_th), Paragraph("<b>Technology</b>", style_th), Paragraph("<b>Purpose</b>", style_th)],
        [Paragraph("Programming Language", style_td_bold), Paragraph("C# 12", style_td), Paragraph("Core object-oriented backend programming language with strong typing and async/await.", style_td)],
        [Paragraph("Framework", style_td_bold), Paragraph("ASP.NET Core Web API", style_td), Paragraph("High-performance REST API runtime for microservices endpoints.", style_td)],
        [Paragraph("Runtime", style_td_bold), Paragraph(".NET 8 (LTS)", style_td), Paragraph("Enterprise Long-Term Support runtime providing modern memory and compute optimizations.", style_td)],
        [Paragraph("ORM & Data Access", style_td_bold), Paragraph("Entity Framework Core 8", style_td), Paragraph("Object-Relational Mapping with Code-First modeling, LINQ queries, and migrations.", style_td)],
        [Paragraph("Database", style_td_bold), Paragraph("Microsoft SQL Server 2022", style_td), Paragraph("Relational database engine hosting 5 isolated physical/logical database catalogs.", style_td)],
        [Paragraph("API Security", style_td_bold), Paragraph("JWT Bearer Authentication", style_td), Paragraph("Stateless asymmetric authentication encoding user claims, email, and roles.", style_td)],
        [Paragraph("Authorization", style_td_bold), Paragraph("Role-Based Access Control (RBAC)", style_td), Paragraph("Restricts sensitive APIs to authorized roles (`Admin` or `Doctor`).", style_td)],
        [Paragraph("API Gateway", style_td_bold), Paragraph("YARP / Reverse Proxy", style_td), Paragraph("Provides unified request routing, health checks, and cross-cutting security enforcement.", style_td)],
        [Paragraph("API Documentation", style_td_bold), Paragraph("Swagger UI / OpenAPI 3.0", style_td), Paragraph("Interactive browser-based API testing sandbox with JWT lock integration.", style_td)],
        [Paragraph("Hosting / Runtime", style_td_bold), Paragraph("Kestrel / Native Process", style_td), Paragraph("High-performance cross-platform self-hosted ASP.NET Core runtime.", style_td)],
        [Paragraph("Shared Library", style_td_bold), Paragraph("PharmacyManagement.Common", style_td), Paragraph("Shared NuGet/class library standardizing JWT, hashing, constants, and envelopes.", style_td)]
    ]
    t_tech = Table(tech_data, colWidths=[120, 140, 272])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5.0: DESIGN PATTERNS
    # =========================================================================
    story.append(TrackedParagraph("5.0 Design Patterns", style_section_h1, "sec_5"))
    patterns_data = [
        [Paragraph("<b>Name</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("Microservices Architecture", style_td_bold), Paragraph("Decomposes the system into 5 cohesive, independently deployable services organized around business domains: Auth, Inventory, Order, Payment, and SaleReport.", style_td)],
        [Paragraph("Database-Per-Service", style_td_bold), Paragraph("Each microservice exclusively owns its database schema. Direct cross-database SQL queries are forbidden; data is shared strictly via typed HTTP REST APIs.", style_td)],
        [Paragraph("Layered Architecture (Internal MVC)", style_td_bold), Paragraph("Internally, each microservice separates concerns into Controllers (API handling), Services (domain logic), and Repositories (EF Core LINQ data access).", style_td)],
        [Paragraph("Repository Pattern", style_td_bold), Paragraph("Abstracts data-access logic from domain services, enabling testability and decoupling business algorithms from database access technologies.", style_td)],
        [Paragraph("Dependency Injection (DI)", style_td_bold), Paragraph("ASP.NET Core DI container manages service lifecycles (Scoped DbContexts, Repositories, and Services), promoting loose coupling and testability.", style_td)],
        [Paragraph("DTO (Data Transfer Object) Pattern", style_td_bold), Paragraph("Dedicated request and response DTOs prevent over-posting, hide internal database primary keys where appropriate, and enforce request validation.", style_td)],
        [Paragraph("API Gateway Pattern", style_td_bold), Paragraph("Centralizes client entry points, handles request forwarding, rate limiting, and decouples internal service ports from client consumers.", style_td)],
        [Paragraph("Transactional Outbox / Idempotency", style_td_bold), Paragraph("Payment and stock operations use unique transaction references and idempotent validation to prevent double-charging or duplicate deductions.", style_td)]
    ]
    t_patterns = Table(patterns_data, colWidths=[150, 382])
    t_patterns.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_patterns)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 6.0: FLOW DIAGRAM
    # =========================================================================
    story.append(TrackedParagraph("6.0 Flow Diagram", style_section_h1, "sec_6"))
    flow_img_path = os.path.join(DIAGRAMS_DIR, "04_Flow_Diagram.jpg")
    if os.path.exists(flow_img_path):
        story.append(Image(flow_img_path, width=450, height=486))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Description", style_desc_heading))
    story.append(Paragraph(
        "The flow diagram models the end-to-end operational execution of the <b>Pharmacy Management System</b> across both <b>Admin</b> "
        "and <b>Doctor / Customer</b> roles. Execution begins at the <b>START</b> pill with user registration and authentication. "
        "Upon successful credential verification, a decision diamond evaluates the user's role: "
        "<b>Admin / Owner</b> branches to inventory procurement, formulary maintenance, order validation, order verification, counter "
        "handover (`PickedUp`), and financial report generation. "
        "The <b>Doctor User / Customer</b> branches to drug catalog browsing, verifying live quantities and expiry dates, selecting "
        "medications, and placing prescription orders.",
        style_body
    ))
    story.append(Paragraph(
        "The central processing pipeline models transactional coordination: verifying stock levels, creating the order record in "
        "`OrderDB`, executing atomic stock decrements in `InventoryDB`, computing itemized totals, and executing payment checkout. "
        "A <b>Payment Successful?</b> decision handles branching: if successful, the order transitions to `Verified`, generates an invoice, "
        "and prepares for counter collection (`PickedUp`). If payment fails, the system executes the <b>Payment Failed Container</b> "
        "workflow: displaying failure diagnostics, updating the order to `PaymentFailed`, and either retrying checkout or cancelling the "
        "order and restoring reserved stock before reaching <b>END</b>.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 7.0: USE CASE DIAGRAM
    # =========================================================================
    story.append(TrackedParagraph("7.0 Use Case Diagram", style_section_h1, "sec_7"))
    usecase_img_path = os.path.join(DIAGRAMS_DIR, "02_Use_Case_Diagram.jpg")
    if os.path.exists(usecase_img_path):
        story.append(Image(usecase_img_path, width=490, height=319))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Description", style_desc_heading))
    story.append(Paragraph(
        "The use case diagram illustrates the functional interactions between the two primary actors—<b>Admin</b> and <b>Doctor</b>—and "
        "the <b>Pharmacy Management System</b> boundary. Both actors associate with the foundational <b>Login / Authenticate</b> use case, "
        "which issues role-bearing JWT tokens governing downstream access.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Admin Actor (12 Use Cases):</b> Full administrative control encompassing User Management, Drug Formularies (Add/Update/Delete), "
        "Supplier Management, Stock Inwarding, Viewing All Doctor Orders, Validating Order Line Items, Verifying Orders (Pending -> Verified), "
        "Moving Orders to PickedUp Section, Viewing PickedUp Orders, Generating Financial Sales Reports, Downloading CSV Spreadsheets, and "
        "Printing Formatted Receipts.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Doctor Actor (7 Use Cases):</b> Clinical user actions including Doctor Signup/Login, Browsing Drug Catalogs, Checking Expiry Dates "
        "& Quantities, Placing Medication Orders, Viewing Personal Order Histories, Tracking Order Status (Cart -> Pending -> Verified -> PickedUp), "
        "and Submitting Online Payments.",
        style_body
    ))
    story.append(Paragraph(
        "The diagram explicitly defines core workflow relationships: placing an order <i>&lt;&lt;includes&gt;&gt;</i> Managing Order Lifecycle, "
        "which in turn <i>&lt;&lt;includes&gt;&gt;</i> Deducting Drug Stock Atomically, Processing 1:1 Payment, and Generating Itemized Invoices, "
        "with an <i>&lt;&lt;extend&gt;&gt;</i> association for Order Cancellation upon stock exhaustion.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 8.0: ARCHITECTURE DIAGRAM
    # =========================================================================
    story.append(TrackedParagraph("8.0 Architecture Diagram", style_section_h1, "sec_8"))
    arch_img_path = os.path.join(DIAGRAMS_DIR, "01_Solution_Architecture_Diagram.jpg")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=490, height=343))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Description", style_desc_heading))
    story.append(Paragraph(
        "The architecture diagram represents the distributed microservices topology of the <b>Pharmacy Management System</b>. "
        "Clients—including the interactive <b>Swagger UI</b>, Web clients, and point-of-sale terminals—interact with the backend through an "
        "<b>API Gateway (YARP / Reverse Proxy)</b>. The Gateway centralizes request routing, load balancing, SSL termination, and rate limiting.",
        style_body
    ))
    story.append(Paragraph(
        "The core domain comprises five independent ASP.NET Core Web API microservices: "
        "<b>1. Auth Service (Port 5001):</b> Manages user registrations, PBKDF2 credential verification, and asymmetric JWT issuance. "
        "<b>2. Inventory Service (Port 5002):</b> Manages the pharmaceutical formulary, certified suppliers, stock inwarding, and atomic deductions. "
        "<b>3. Order Service (Port 5003):</b> Coordinates doctor orders, order item lines, admin verification, and counter collection handovers. "
        "<b>4. Payment Service (Port 5004):</b> Processes multi-method checkouts under a strict 1:1 unique order constraint. "
        "<b>5. SaleReport Service (Port 5005):</b> Aggregates financial performance, calculating gross revenue, cost of goods sold, and net profit.",
        style_body
    ))
    story.append(Paragraph(
        "Each service maintains its dedicated Microsoft SQL Server database. Cross-cutting utilities—including JWT handlers, password hashing, "
        "and standard response envelopes—are centralized within the shared <b>PharmacyManagement.Common</b> class library.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 9.0: ENTITY-RELATIONSHIP (ER) DIAGRAM
    # =========================================================================
    story.append(TrackedParagraph("9.0 Entity-Relationship Diagram", style_section_h1, "sec_9"))
    er_img_path = os.path.join(DIAGRAMS_DIR, "05_ER_Diagram.jpg")
    if os.path.exists(er_img_path):
        story.append(Image(er_img_path, width=490, height=343))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Description", style_desc_heading))
    story.append(Paragraph(
        "The Entity-Relationship (ER) diagram defines the data models and cardinalities across the five microservices. "
        "In strict adherence to microservice isolation, physical foreign keys with database-level cascading rules exist exclusively "
        "within individual service boundaries, while cross-service associations operate as logical foreign keys resolved via REST APIs:",
        style_body
    ))
    story.append(Paragraph("• <b>User to Order (1:M):</b> A Doctor user in `AuthDB` can place multiple medication orders. `Orders.DoctorID` logically references `Users.UserId`.", style_bullet))
    story.append(Paragraph("• <b>Order to OrderItem (1:M):</b> A physical database foreign key with `ON DELETE CASCADE` in `OrderDB` ensuring complete cleanup of child line items.", style_bullet))
    story.append(Paragraph("• <b>Drug to OrderItem (1:M):</b> `OrderItems.DrugId` logically references `Drugs.DrugId` in `InventoryDB`, storing an immutable snapshot of `DrugName` for historical receipt accuracy.", style_bullet))
    story.append(Paragraph("• <b>Supplier to Inventory (1:M) & Drug to Inventory (1:M):</b> Physical foreign keys in `InventoryDB` tracking wholesale stock receipts with purchase prices.", style_bullet))
    story.append(Paragraph("• <b>Order to Payment (1:1):</b> A strict one-to-one relationship enforced by a `UNIQUE INDEX` on `Payments.OrderId` in `PaymentDB`.", style_bullet))
    story.append(Paragraph("• <b>SaleReport (Standalone):</b> A standalone reporting entity aggregating financial totals across order and inventory data without locking transaction tables.", style_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 10.0: DATABASE DIAGRAM
    # =========================================================================
    story.append(TrackedParagraph("10.0 Database Diagram", style_section_h1, "sec_10"))
    db_img_path = os.path.join(DIAGRAMS_DIR, "06_Database_Schema_Diagram.jpg")
    if os.path.exists(db_img_path):
        story.append(Image(db_img_path, width=490, height=338))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Description", style_desc_heading))
    story.append(Paragraph(
        "The database diagram illustrates the <b>Database-per-Service</b> physical schema design implemented in <b>Microsoft SQL Server 2022</b>. "
        "The system partitions data into five dedicated databases: <b>Pharmacy_UserDB</b>, <b>Pharmacy_InventoryDB</b>, <b>Pharmacy_OrderDB</b>, "
        "<b>Pharmacy_PaymentDB</b>, and <b>Pharmacy_SaleReportDB</b>.",
        style_body
    ))
    story.append(Paragraph(
        "Each table definition specifies primary clustered keys, non-clustered indexes on search predicates (such as `Users.Role`, `Drugs.IsAvailable`, "
        "`Orders.Status`), and check constraints. All monetary values (e.g. `Drugs.Price`, `Inventory.PurchasePrice`, `Orders.TotalAmount`, `Payments.Amount`, "
        "`SaleReports.TotalRevenue`, `SaleReports.Profit`) strictly employ `DECIMAL(18,2)` to prevent floating-point rounding errors. All audit and transaction "
        "timestamps utilize `DATETIME2(7)` in UTC format.",
        style_body
    ))
    story.append(Paragraph(
        "Database scripts are fully scripted in `scripts/InitDatabases.sql` with idempotent guards (`IF NOT EXISTS`), enabling automated database creation "
        "and seed data provisioning on any local SQL Server developer environment.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 11.0: SEQUENCE DIAGRAM
    # =========================================================================
    story.append(TrackedParagraph("11.0 Sequence Diagram", style_section_h1, "sec_11"))
    seq_img_path = os.path.join(DIAGRAMS_DIR, "03_Sequence_Diagram.jpg")
    if os.path.exists(seq_img_path):
        story.append(Image(seq_img_path, width=490, height=357))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Description", style_desc_heading))
    story.append(Paragraph(
        "The sequence diagram details the runtime interaction between the <b>Doctor User</b>, <b>Admin User</b>, <b>API Gateway</b>, and all "
        "five microservices across the complete order fulfillment and financial reporting lifecycle across 24 synchronous REST messages:",
        style_body
    ))
    story.append(Paragraph("1. <b>Authentication (Steps 1–4):</b> Doctor authenticates with email/password; AuthService validates credentials against `AuthDB` and returns a signed JWT Bearer Token encoding the `Doctor` role claim.", style_bullet))
    story.append(Paragraph("2. <b>Catalog Browsing (Steps 5–7):</b> Doctor passes the token to query active medications; InventoryService queries `InventoryDB` and returns available drugs with prices.", style_bullet))
    story.append(Paragraph("3. <b>Order Placement & Stock Decrement (Steps 8–12):</b> Doctor submits an order. OrderService stages the order in `Pending` status and calls InventoryService to decrement stock atomically. InventoryService verifies availability, deducts quantities, and returns success.", style_bullet))
    story.append(Paragraph("4. <b>Payment Processing (Steps 13–15):</b> Doctor triggers payment; PaymentService validates the 1:1 constraint, persists the payment record, and returns a unique transaction reference.", style_bullet))
    story.append(Paragraph("5. <b>Admin Verification & Handover (Steps 16–22):</b> Admin queries all doctor orders, inspects order line items, validates stock, updates status to `Verified`, and marks final handover in `PickedUp`.", style_bullet))
    story.append(Paragraph("6. <b>Sales Analytics (Steps 23–24):</b> Admin requests sales reporting; SaleReportService aggregates verified orders, calculates net profit, and returns a financial summary.", style_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 12.0: SOLUTION STEPS
    # =========================================================================
    story.append(TrackedParagraph("12.0 Solution Steps", style_section_h1, "sec_12"))
    
    story.append(Paragraph("12.1 Customer / Doctor and Admin Registration and Login", style_section_h2))
    story.append(Paragraph("• The user submits registration details (Name, Contact, Email, Password, Role) to `AuthService`.", style_bullet))
    story.append(Paragraph("• `AuthService` verifies email uniqueness in `Pharmacy_UserDB` and hashes the password using PBKDF2 with HMAC-SHA256 (100,000 iterations).", style_bullet))
    story.append(Paragraph("• Upon login, `AuthService` validates credentials and generates a cryptographically signed JWT token containing `UserId`, `Email`, and `Role` claims.", style_bullet))
    story.append(Paragraph("• The client provides the JWT token via the `Authorization: Bearer <token>` header for all protected endpoints in Swagger UI.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.2 Admin Manages Drugs & Pricing", style_section_h2))
    story.append(Paragraph("• Admin provides the JWT token to access formulary endpoints on `InventoryService` (Port 5002).", style_bullet))
    story.append(Paragraph("• Admin creates new drugs by specifying Drug Name, Description, Selling Price, Expiry Date, and Initial Quantity.", style_bullet))
    story.append(Paragraph("• Admin updates existing medications or deletes discontinued drugs from `Pharmacy_InventoryDB`.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.3 Admin Manages Suppliers & Stock Inventory", style_section_h2))
    story.append(Paragraph("• Admin registers verified pharmaceutical distributors by submitting Supplier Name, Contact Email, Phone, and Address.", style_bullet))
    story.append(Paragraph("• When new stock arrives, Admin creates an `Inventory` inward record associating `SupplierId`, `DrugId`, `PurchasePrice`, and `QuantityAdded`.", style_bullet))
    story.append(Paragraph("• `InventoryService` increments `Drugs.Quantity` and updates `Drugs.IsAvailable = true` automatically.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.4 Doctor Searches & Views Available Drugs", style_section_h2))
    story.append(Paragraph("• Doctor queries `GET /api/drugs?availableOnly=true` to view only in-stock and non-expired medications.", style_bullet))
    story.append(Paragraph("• `InventoryService` runs LINQ queries filtering `IsAvailable == true` and `Quantity > 0`, returning catalog items with selling prices.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.5 Doctor Buys Drugs (Places Order)", style_section_h2))
    story.append(Paragraph("• Doctor selects one or more medications and submits `POST /api/orders` with an array of `DrugId` and `Quantity`.", style_bullet))
    story.append(Paragraph("• `OrderService` extracts `DoctorID` from the JWT token and verifies requested drugs.", style_bullet))
    story.append(Paragraph("• `OrderService` communicates via HTTP with `InventoryService` to atomically decrement stock.", style_bullet))
    story.append(Paragraph("• `OrderService` computes `TotalAmount = Sum(Quantity * UnitPrice)` and saves the order in `Pending` status.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.6 Payment Processing", style_section_h2))
    story.append(Paragraph("• Doctor submits payment details to `PaymentService` (`POST /api/payments`) specifying `OrderId`, `Amount`, and `PaymentMethod` (CreditCard, UPI, NetBanking, Cash).", style_bullet))
    story.append(Paragraph("• `PaymentService` verifies that the order has no prior payment, enforcing the 1:1 payment rule.", style_bullet))
    story.append(Paragraph("• `PaymentService` generates a unique `TransactionReference` (e.g., `TXN-A83F91B2C4D5`), persists the record in `Pharmacy_PaymentDB`, and marks `PaymentStatus = Completed`.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.7 Admin Order Verification & Pickup Handover", style_section_h2))
    story.append(Paragraph("• Admin accesses `GET /api/orders` to inspect orders placed by all doctors across the hospital/clinic.", style_bullet))
    story.append(Paragraph("• Admin reviews the line items, confirms stock validity, and calls `PUT /api/orders/{id}/verify`, setting `Status = Verified`.", style_bullet))
    story.append(Paragraph("• When the doctor or patient arrives at the pharmacy dispensing counter, Admin calls `PUT /api/orders/{id}/pickup`, transferring the order to the `PickedUp` section.", style_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12.8 Admin Sales Report Generation, CSV Download & Print", style_section_h2))
    story.append(Paragraph("• Admin accesses `SaleReportService` (Port 5005) and calls `POST /api/salereports/generate` with a range (`Daily`, `Weekly`, `Monthly`, or `Yearly`).", style_bullet))
    story.append(Paragraph("• `SaleReportService` aggregates verified orders, calculates Gross Revenue, aggregates wholesale COGS purchase costs from Inventory, and computes net `Profit`.", style_bullet))
    story.append(Paragraph("• Admin downloads the report as an RFC-4180 compliant CSV spreadsheet (`GET /api/salereports/{id}/download`) or views a formatted ASCII receipt (`GET /api/salereports/{id}/print`).", style_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 13.0: CLASSES NAMES
    # =========================================================================
    story.append(TrackedParagraph("13.0 Classes Names", style_section_h1, "sec_13"))
    
    story.append(Paragraph("Entities (Domain Models)", style_section_h2))
    models_data = [
        [Paragraph("<b>S.No</b>", style_th), Paragraph("<b>Class Name</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("1", style_td), Paragraph("User.cs", style_td_bold), Paragraph("Represents user accounts in AuthDB with UserId PK, Name, Email, PhoneNumber, PasswordHash, Role (Admin/Doctor), IsActive, and CreatedDate.", style_td)],
        [Paragraph("2", style_td), Paragraph("Drug.cs", style_td_bold), Paragraph("Represents formulary medications in InventoryDB with DrugId PK, Name, Description, Price (selling price), ExpiryDate, Quantity, and IsAvailable.", style_td)],
        [Paragraph("3", style_td), Paragraph("Supplier.cs", style_td_bold), Paragraph("Represents wholesale vendors in InventoryDB with SupplierId PK, SupplierName, Email, PhoneNumber, and Address.", style_td)],
        [Paragraph("4", style_td), Paragraph("Inventory.cs", style_td_bold), Paragraph("Represents stock inwarding batches in InventoryDB with InventoryId PK, SupplierId FK, DrugId FK, PurchasePrice, QuantityAdded, and StockReceivedDate.", style_td)],
        [Paragraph("5", style_td), Paragraph("Order.cs", style_td_bold), Paragraph("Represents orders in OrderDB with OrderId PK, DoctorID logical FK, OrderDate, TotalAmount, and Status (Cart/Pending/Verified/PickedUp).", style_td)],
        [Paragraph("6", style_td), Paragraph("OrderItem.cs", style_td_bold), Paragraph("Represents line items in OrderDB with OrderItemId PK, OrderId FK, DrugId logical FK, DrugName snapshot, Quantity, and UnitPrice.", style_td)],
        [Paragraph("7", style_td), Paragraph("Payment.cs", style_td_bold), Paragraph("Represents payment records in PaymentDB with PaymentId PK, OrderId 1:1 unique FK, Amount, PaymentDate, PaymentMethod, PaymentStatus, and TransactionReference.", style_td)],
        [Paragraph("8", style_td), Paragraph("SaleReport.cs", style_td_bold), Paragraph("Represents financial reports in SaleReportDB with SaleReportId PK, ReportType (Daily/Weekly/Monthly/Yearly), FromDate, ToDate, TotalOrders, TotalRevenue, GeneratedDate, and Profit.", style_td)]
    ]
    t_models = Table(models_data, colWidths=[35, 135, 362])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Controllers (API Layer)", style_section_h2))
    ctrl_data = [
        [Paragraph("<b>S.No</b>", style_th), Paragraph("<b>Class Name</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("1", style_td), Paragraph("AuthController.cs", style_td_bold), Paragraph("Exposes user signup (`/register`), login (`/login`), and profile (`/me`) endpoints under JWT authentication.", style_td)],
        [Paragraph("2", style_td), Paragraph("DrugsController.cs", style_td_bold), Paragraph("Exposes catalog retrieval, filtering, and Admin CRUD operations (`/api/drugs`).", style_td)],
        [Paragraph("3", style_td), Paragraph("SuppliersController.cs", style_td_bold), Paragraph("Exposes Admin CRUD management for certified wholesale pharmaceutical suppliers (`/api/suppliers`).", style_td)],
        [Paragraph("4", style_td), Paragraph("InventoryController.cs", style_td_bold), Paragraph("Handles stock inwarding batches and inter-service atomic quantity deductions (`/api/inventory`).", style_td)],
        [Paragraph("5", style_td), Paragraph("OrdersController.cs", style_td_bold), Paragraph("Handles doctor order placement, order verification, counter handover (`PickedUp`), and order retrieval (`/api/orders`).", style_td)],
        [Paragraph("6", style_td), Paragraph("PaymentsController.cs", style_td_bold), Paragraph("Handles checkout transactions and enforces the 1:1 order payment rule (`/api/payments`).", style_td)],
        [Paragraph("7", style_td), Paragraph("SaleReportsController.cs", style_td_bold), Paragraph("Handles report generation, range filtering, CSV spreadsheet download, and printable formatting (`/api/salereports`).", style_td)]
    ]
    t_ctrl = Table(ctrl_data, colWidths=[35, 145, 352])
    t_ctrl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_ctrl)
    story.append(PageBreak())

    story.append(Paragraph("Services (Business Logic Layer)", style_section_h2))
    svc_data = [
        [Paragraph("<b>S.No</b>", style_th), Paragraph("<b>Class Name</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("1", style_td), Paragraph("IAuthService.cs / AuthService.cs", style_td_bold), Paragraph("Implements user registration, duplicate email validation, credential checking, and JWT issuance.", style_td)],
        [Paragraph("2", style_td), Paragraph("IDrugService.cs / DrugService.cs", style_td_bold), Paragraph("Implements drug validation, price verification, stock checks, and availability flags.", style_td)],
        [Paragraph("3", style_td), Paragraph("ISupplierService.cs / SupplierService.cs", style_td_bold), Paragraph("Implements vendor registration, email/phone format checks, and supplier cataloging.", style_td)],
        [Paragraph("4", style_td), Paragraph("IInventoryService.cs / InventoryService.cs", style_td_bold), Paragraph("Coordinates stock inwarding batches, updates drug balances, and executes atomic stock decrements.", style_td)],
        [Paragraph("5", style_td), Paragraph("IOrderService.cs / OrderService.cs", style_td_bold), Paragraph("Validates line items, invokes Inventory Service via HTTP client, computes totals, and manages order lifecycle.", style_td)],
        [Paragraph("6", style_td), Paragraph("IPaymentService.cs / PaymentService.cs", style_td_bold), Paragraph("Validates order payment eligibility, checks 1:1 uniqueness constraint, and generates transaction codes.", style_td)],
        [Paragraph("7", style_td), Paragraph("ISaleReportService.cs / SaleReportService.cs", style_td_bold), Paragraph("Aggregates order data, computes net profit over purchase costs, and formats CSV and print layouts.", style_td)],
        [Paragraph("8", style_td), Paragraph("JwtTokenGenerator.cs / PasswordHasher.cs", style_td_bold), Paragraph("Common security primitives implementing HMAC-SHA256 JWT generation and PBKDF2 salt hashing.", style_td)]
    ]
    t_svc = Table(svc_data, colWidths=[35, 185, 312])
    t_svc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_svc)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Repositories (Data Access Layer & EF Core DbContexts)", style_section_h2))
    repo_data = [
        [Paragraph("<b>S.No</b>", style_th), Paragraph("<b>Class Name</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("1", style_td), Paragraph("UserRepository.cs / AuthDbContext.cs", style_td_bold), Paragraph("Executes LINQ queries against `Pharmacy_UserDB` for user authentication and profile retrieval.", style_td)],
        [Paragraph("2", style_td), Paragraph("DrugRepository.cs / InventoryDbContext.cs", style_td_bold), Paragraph("Executes LINQ queries against `Pharmacy_InventoryDB` for drug CRUD and atomic decrement updates.", style_td)],
        [Paragraph("3", style_td), Paragraph("SupplierRepository.cs", style_td_bold), Paragraph("Executes LINQ queries for pharmaceutical vendor persistence in `Pharmacy_InventoryDB`.", style_td)],
        [Paragraph("4", style_td), Paragraph("InventoryRepository.cs", style_td_bold), Paragraph("Persists stock inward batches and links suppliers with drugs in `Pharmacy_InventoryDB`.", style_td)],
        [Paragraph("5", style_td), Paragraph("OrderRepository.cs / OrderDbContext.cs", style_td_bold), Paragraph("Persists orders and child order items with cascading integrity in `Pharmacy_OrderDB`.", style_td)],
        [Paragraph("6", style_td), Paragraph("PaymentRepository.cs / PaymentDbContext.cs", style_td_bold), Paragraph("Persists payment transactions and enforces unique index on `OrderId` in `Pharmacy_PaymentDB`.", style_td)],
        [Paragraph("7", style_td), Paragraph("SaleReportRepository.cs / SaleReportDbContext.cs", style_td_bold), Paragraph("Persists aggregated financial reports and date-range queries in `Pharmacy_SaleReportDB`.", style_td)]
    ]
    t_repo = Table(repo_data, colWidths=[35, 195, 302])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_repo)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 14.0: VALIDATIONS
    # =========================================================================
    story.append(TrackedParagraph("14.0 Validations", style_section_h1, "sec_14"))
    validations = [
        "<b>User Registration Validations:</b> Strict email format validation, duplicate email checking, minimum 6-character password requirements, and mandatory valid Role (`Admin` or `Doctor`).",
        "<b>JWT Security Token Verification:</b> Validates cryptographic HMAC-SHA256 signature, issuer (`PharmacyManagementAuthService`), audience (`PharmacyManagementMicroservices`), non-expiration, and valid Role claims on protected endpoints.",
        "<b>Role-Based Access Control:</b> Enforces endpoint policies ensuring only `Admin` users can modify drugs, suppliers, or verify orders, and only `Doctor` users can initiate order placement.",
        "<b>Drug Pricing & Expiry Validation:</b> Requires `Price > 0`, non-negative `Quantity >= 0`, and `ExpiryDate > DateTime.UtcNow` during drug creation and order submission.",
        "<b>Supplier Profile Validation:</b> Enforces valid email syntax, valid international phone number format, and non-empty physical supplier addresses.",
        "<b>Stock Inwarding Validation:</b> Verifies that `SupplierId` and `DrugId` exist prior to recording stock inward batches, and requires `PurchasePrice > 0` and `QuantityAdded > 0`.",
        "<b>Atomic Stock Availability Verification:</b> Before staging an order, the system checks `Quantity >= RequestedQuantity`. If insufficient, the order fails with an explicit out-of-stock validation error.",
        "<b>Atomic Decrement Concurrency Guard:</b> Automatically updates `Drugs.IsAvailable = false` when stock drops to 0, preventing race-condition over-selling.",
        "<b>1:1 Order Payment Enforcement:</b> The system verifies that `OrderId` has not already been billed (`Payments.OrderId` unique constraint), preventing double payments.",
        "<b>Order State Machine Rules:</b> Enforces strict state transitions: `Cart` -> `Pending` -> `Verified` -> `PickedUp`. Only orders in `Verified` status can be marked as `PickedUp`.",
        "<b>Doctor Order Isolation:</b> Doctors can query only their own orders (`DoctorID == Claims.UserId`), whereas Admins have global visibility across all hospital orders.",
        "<b>Report Date Range Validation:</b> Validates that `ToDate >= FromDate` and ensures valid `ReportType` enum values (`Daily`, `Weekly`, `Monthly`, `Yearly`)."
    ]
    for v in validations:
        story.append(Paragraph(f"• {v}", style_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 15.0: API CATALOGUE
    # =========================================================================
    story.append(TrackedParagraph("15.0 API Catalogue", style_section_h1, "sec_15"))
    api_data = [
        [Paragraph("<b>Module</b>", style_th), Paragraph("<b>Endpoint</b>", style_th), Paragraph("<b>Method</b>", style_th), Paragraph("<b>Access</b>", style_th)],
        [Paragraph("Authentication", style_td), Paragraph("/api/auth/register", style_td_bold), Paragraph("POST", style_td), Paragraph("Public", style_td)],
        [Paragraph("Authentication", style_td), Paragraph("/api/auth/login", style_td_bold), Paragraph("POST", style_td), Paragraph("Public", style_td)],
        [Paragraph("Authentication", style_td), Paragraph("/api/auth/me", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Authentication", style_td), Paragraph("/api/auth/users", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        
        [Paragraph("Drugs", style_td), Paragraph("/api/drugs", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Drugs", style_td), Paragraph("/api/drugs/{id}", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Drugs", style_td), Paragraph("/api/drugs", style_td_bold), Paragraph("POST", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Drugs", style_td), Paragraph("/api/drugs/{id}", style_td_bold), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Drugs", style_td), Paragraph("/api/drugs/{id}", style_td_bold), Paragraph("DELETE", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Drugs", style_td), Paragraph("/api/drugs/deduct-stock", style_td_bold), Paragraph("POST", style_td), Paragraph("Internal / Authenticated", style_td)],

        [Paragraph("Suppliers", style_td), Paragraph("/api/suppliers", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Suppliers", style_td), Paragraph("/api/suppliers/{id}", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Suppliers", style_td), Paragraph("/api/suppliers", style_td_bold), Paragraph("POST", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Suppliers", style_td), Paragraph("/api/suppliers/{id}", style_td_bold), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Suppliers", style_td), Paragraph("/api/suppliers/{id}", style_td_bold), Paragraph("DELETE", style_td), Paragraph("Admin", style_td)],

        [Paragraph("Inventory", style_td), Paragraph("/api/inventory", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Inventory", style_td), Paragraph("/api/inventory", style_td_bold), Paragraph("POST", style_td), Paragraph("Admin", style_td)],

        [Paragraph("Orders", style_td), Paragraph("/api/orders", style_td_bold), Paragraph("POST", style_td), Paragraph("Doctor", style_td)],
        [Paragraph("Orders", style_td), Paragraph("/api/orders", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Orders", style_td), Paragraph("/api/orders/{id}", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin / Doctor", style_td)],
        [Paragraph("Orders", style_td), Paragraph("/api/orders/{id}/verify", style_td_bold), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Orders", style_td), Paragraph("/api/orders/{id}/pickup", style_td_bold), Paragraph("PUT", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Orders", style_td), Paragraph("/api/orders/pickedup", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],

        [Paragraph("Payments", style_td), Paragraph("/api/payments", style_td_bold), Paragraph("POST", style_td), Paragraph("Doctor / Admin", style_td)],
        [Paragraph("Payments", style_td), Paragraph("/api/payments/order/{orderId}", style_td_bold), Paragraph("GET", style_td), Paragraph("Doctor / Admin", style_td)],
        [Paragraph("Payments", style_td), Paragraph("/api/payments/{id}", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],

        [Paragraph("Sales Reports", style_td), Paragraph("/api/salereports/generate", style_td_bold), Paragraph("POST", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Sales Reports", style_td), Paragraph("/api/salereports", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Sales Reports", style_td), Paragraph("/api/salereports/{id}/download", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)],
        [Paragraph("Sales Reports", style_td), Paragraph("/api/salereports/{id}/print", style_td_bold), Paragraph("GET", style_td), Paragraph("Admin", style_td)]
    ]
    t_api = Table(api_data, colWidths=[90, 240, 60, 142])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_api)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 16.0 & 17.0: HTTP STATUS CODES & INTEGRATIONS
    # =========================================================================
    story.append(TrackedParagraph("16.0 HTTP Status Codes", style_section_h1, "sec_16"))
    http_data = [
        [Paragraph("<b>Status Code</b>", style_th), Paragraph("<b>Status</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("200", style_td_bold), Paragraph("OK", style_td), Paragraph("The request processed successfully and returned requested entity data.", style_td)],
        [Paragraph("201", style_td_bold), Paragraph("Created", style_td), Paragraph("A new resource (User, Drug, Order, Payment, or SaleReport) was created successfully.", style_td)],
        [Paragraph("204", style_td_bold), Paragraph("No Content", style_td), Paragraph("The request was completed successfully and no response payload is required.", style_td)],
        [Paragraph("400", style_td_bold), Paragraph("Bad Request", style_td), Paragraph("Validation failed (e.g. invalid email format, insufficient stock, negative price, or malformed JSON).", style_td)],
        [Paragraph("401", style_td_bold), Paragraph("Unauthorized", style_td), Paragraph("Missing, expired, or invalid JWT Bearer token, or invalid login credentials.", style_td)],
        [Paragraph("403", style_td_bold), Paragraph("Forbidden", style_td), Paragraph("Authenticated user does not possess the required role (e.g., Doctor attempting Admin operations).", style_td)],
        [Paragraph("404", style_td_bold), Paragraph("Not Found", style_td), Paragraph("Requested Drug, Supplier, Order, Payment, or Report was not found in the database.", style_td)],
        [Paragraph("409", style_td_bold), Paragraph("Conflict", style_td), Paragraph("State conflict occurred (e.g., duplicate email address, duplicate 1:1 payment for an order).", style_td)],
        [Paragraph("500", style_td_bold), Paragraph("Internal Server Error", style_td), Paragraph("An unhandled exception or database connection error occurred during execution.", style_td)]
    ]
    t_http = Table(http_data, colWidths=[80, 110, 342])
    t_http.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_http)
    story.append(Spacer(1, 8))

    story.append(TrackedParagraph("17.0 Integrations", style_section_h1, "sec_17"))
    integrations = [
        "<b>REST APIs (Typed HttpClient):</b> Enables synchronous inter-service HTTP communication between `OrderService` and `InventoryService` for atomic stock validation and deduction.",
        "<b>JWT Bearer Token Security:</b> Stateless cryptographic authentication passing user identity (`UserId`), email, and roles across microservices.",
        "<b>Microsoft SQL Server 2022:</b> Hosts 5 isolated databases (`Pharmacy_UserDB`, `Pharmacy_InventoryDB`, `Pharmacy_OrderDB`, `Pharmacy_PaymentDB`, `Pharmacy_SaleReportDB`).",
        "<b>Entity Framework Core 8:</b> Manages object-relational mapping, code-first migrations, and LINQ execution.",
        "<b>Swagger / OpenAPI 3.0:</b> Interactive API documentation and testing interface on every microservice.",
        "<b>CSV & Printable Output:</b> Financial report generation providing RFC-4180 CSV export and ASCII receipts."
    ]
    for item in integrations:
        story.append(Paragraph(f"• {item}", style_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 18.0 & 19.0: SAMPLE REQUESTS & RESPONSES
    # =========================================================================
    story.append(TrackedParagraph("18.0 Sample API Requests", style_section_h1, "sec_18"))
    
    story.append(Paragraph("Doctor Order Creation Request (`POST /api/orders`)", style_section_h2))
    req_json = (
        "{\n"
        '  "items": [\n'
        '    {\n'
        '      "drugId": 1,\n'
        '      "quantity": 2\n'
        '    },\n'
        '    {\n'
        '      "drugId": 2,\n'
        '      "quantity": 1\n'
        '    }\n'
        '  ]\n'
        "}"
    )
    story.append(Paragraph(req_json.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Order Payment Checkout Request (`POST /api/payments`)", style_section_h2))
    pay_req_json = (
        "{\n"
        '  "orderId": 1,\n'
        '  "amount": 25.50,\n'
        '  "paymentMethod": "CreditCard"\n'
        "}"
    )
    story.append(Paragraph(pay_req_json.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code))
    story.append(Spacer(1, 8))

    story.append(TrackedParagraph("19.0 Sample API Responses", style_section_h1, "sec_19"))
    
    story.append(Paragraph("Successful Order Creation Response (Status: 201 Created)", style_section_h2))
    res_json = (
        "{\n"
        '  "success": true,\n'
        '  "message": "Order created successfully",\n'
        '  "data": {\n'
        '    "orderId": 1,\n'
        '    "doctorId": 2,\n'
        '    "doctorName": "Dr. Robert Smith",\n'
        '    "orderDate": "2026-11-18T10:15:30Z",\n'
        '    "totalAmount": 25.50,\n'
        '    "status": "Pending",\n'
        '    "orderItems": [\n'
        '      {\n'
        '        "orderItemId": 1,\n'
        '        "drugId": 1,\n'
        '        "drugName": "Paracetamol 500mg",\n'
        '        "quantity": 2,\n'
        '        "unitPrice": 5.50,\n'
        '        "totalPrice": 11.00\n'
        '      },\n'
        '      {\n'
        '        "orderItemId": 2,\n'
        '        "drugId": 2,\n'
        '        "drugName": "Amoxicillin 250mg",\n'
        '        "quantity": 1,\n'
        '        "unitPrice": 14.50,\n'
        '        "totalPrice": 14.50\n'
        '      }\n'
        '    ]\n'
        '  },\n'
        '  "errors": []\n'
        "}"
    )
    story.append(Paragraph(res_json.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 20.0: UNIT TESTING
    # =========================================================================
    story.append(TrackedParagraph("20.0 Unit Testing", style_section_h1, "sec_20"))
    story.append(Paragraph("The system is verified using an automated NUnit test matrix covering core service layer scenarios:", style_body))
    
    tests_data = [
        [Paragraph("<b>Test Case ID</b>", style_th), Paragraph("<b>Module</b>", style_th), Paragraph("<b>Test Scenario</b>", style_th), Paragraph("<b>Expected Result</b>", style_th)],
        [Paragraph("TC-01", style_td_bold), Paragraph("Auth", style_td), Paragraph("Register new Doctor user with valid email and password.", style_td), Paragraph("User record is saved in UserDB and returns 201 Created.", style_td)],
        [Paragraph("TC-02", style_td_bold), Paragraph("Auth", style_td), Paragraph("Register using an email that already exists in UserDB.", style_td), Paragraph("Returns 409 Conflict with duplicate email validation error.", style_td)],
        [Paragraph("TC-03", style_td_bold), Paragraph("Auth", style_td), Paragraph("Login with valid credentials for Doctor user.", style_td), Paragraph("Returns 200 OK with valid signed JWT Bearer token and Role claim.", style_td)],
        [Paragraph("TC-04", style_td_bold), Paragraph("Auth", style_td), Paragraph("Login with invalid password.", style_td), Paragraph("Returns 401 Unauthorized with credential error message.", style_td)],
        
        [Paragraph("TC-05", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Admin creates new drug with valid price and expiry date.", style_td), Paragraph("Drug is created in InventoryDB with IsAvailable = true.", style_td)],
        [Paragraph("TC-06", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Admin attempts to create drug with negative price.", style_td), Paragraph("Validation fails with 400 Bad Request.", style_td)],
        [Paragraph("TC-07", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Query available drugs when some medications have Quantity = 0.", style_td), Paragraph("Returns only medications with IsAvailable = true and Quantity > 0.", style_td)],
        [Paragraph("TC-08", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Atomic stock decrement when sufficient stock is available.", style_td), Paragraph("Quantity is reduced by requested amount; returns 200 OK.", style_td)],
        [Paragraph("TC-09", style_td_bold), Paragraph("Inventory", style_td), Paragraph("Atomic stock decrement when requested quantity exceeds available stock.", style_td), Paragraph("Operation is rejected; stock remains unchanged.", style_td)],

        [Paragraph("TC-10", style_td_bold), Paragraph("Order", style_td), Paragraph("Doctor creates order with available medications.", style_td), Paragraph("Order is staged in Pending status with calculated TotalAmount.", style_td)],
        [Paragraph("TC-11", style_td_bold), Paragraph("Order", style_td), Paragraph("Doctor attempts to place order for expired or out-of-stock medication.", style_td), Paragraph("Order creation is rejected with stock validation error.", style_td)],
        [Paragraph("TC-12", style_td_bold), Paragraph("Order", style_td), Paragraph("Doctor queries own orders.", style_td), Paragraph("Returns only orders associated with the authenticated DoctorID.", style_td)],
        [Paragraph("TC-13", style_td_bold), Paragraph("Order", style_td), Paragraph("Admin verifies valid pending order.", style_td), Paragraph("Order status transitions from Pending to Verified.", style_td)],
        [Paragraph("TC-14", style_td_bold), Paragraph("Order", style_td), Paragraph("Admin marks verified order as PickedUp.", style_td), Paragraph("Order status transitions to PickedUp; visible in PickedUp query.", style_td)],

        [Paragraph("TC-15", style_td_bold), Paragraph("Payment", style_td), Paragraph("Process payment for verified order with valid amount.", style_td), Paragraph("Payment is saved in PaymentDB with Status = Completed.", style_td)],
        [Paragraph("TC-16", style_td_bold), Paragraph("Payment", style_td), Paragraph("Attempt duplicate payment for an order with existing payment record.", style_td), Paragraph("1:1 constraint rejects operation with 409 Conflict.", style_td)],

        [Paragraph("TC-17", style_td_bold), Paragraph("SaleReport", style_td), Paragraph("Generate Daily sales report for current date range.", style_td), Paragraph("Aggregates orders, computes revenue, costs, and profit.", style_td)],
        [Paragraph("TC-18", style_td_bold), Paragraph("SaleReport", style_td), Paragraph("Download sales report as CSV.", style_td), Paragraph("Returns file with `text/csv` MIME type and RFC-4180 headers.", style_td)],
        [Paragraph("TC-19", style_td_bold), Paragraph("SaleReport", style_td), Paragraph("Generate report with invalid date range (FromDate > ToDate).", style_td), Paragraph("Validation fails with 400 Bad Request.", style_td)],
        [Paragraph("TC-20", style_td_bold), Paragraph("Security", style_td), Paragraph("Doctor attempts to access Admin drug creation endpoint.", style_td), Paragraph("Request is blocked with 403 Forbidden.", style_td)]
    ]
    t_tests = Table(tests_data, colWidths=[55, 65, 200, 212])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_tests)

    return story

def generate_two_pass_pdf(output_filename):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    # PASS 1: Build dummy to gather exact page numbers
    dummy_doc = SimpleDocTemplate(
        "dummy_pass1.pdf",
        pagesize=letter,
        leftMargin=40, rightMargin=40,
        topMargin=50, bottomMargin=50
    )
    story1 = build_pdf_story(toc_page_map=None)
    dummy_doc.build(story1, canvasmaker=NumberedCanvas)
    
    # Copy gathered page numbers
    final_page_map = dict(SECTION_PAGE_MAP)
    print("Dynamic Section Page Map:", final_page_map)
    if os.path.exists("dummy_pass1.pdf"):
        os.remove("dummy_pass1.pdf")
    
    # PASS 2: Build final PDF with dynamically accurate Table of Contents
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=40, rightMargin=40,
        topMargin=50, bottomMargin=50
    )
    story2 = build_pdf_story(toc_page_map=final_page_map)
    doc.build(story2, canvasmaker=NumberedCanvas)
    print(f"Generated LLD PDF successfully: {output_filename}")

if __name__ == "__main__":
    generate_two_pass_pdf(WORKSPACE_PDF)
    generate_two_pass_pdf(ARTIFACT_PDF)
