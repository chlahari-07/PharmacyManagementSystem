import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

WORKSPACE_DOCX = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\PharmacyManagement_LLD.docx"
ARTIFACT_DOCX = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\fbadf837-bfa5-49ff-a097-c847f39ee39a\PharmacyManagement_LLD.docx"

DIAGRAMS_DIR = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"

# Corporate Color Palette (Matching TechBuddy Reference)
COLOR_PRIMARY_HEX = "004F7A"    # TechBuddy Deep Teal/Blue
COLOR_SECONDARY_HEX = "1A5276"  # Navy
COLOR_DARK_HEX = "1E293B"       # Slate body
COLOR_HEADER_BG = "F1F5F9"      # Table header background
COLOR_BORDER_HEX = "CBD5E1"     # Table border
COLOR_MUTED_HEX = "64748B"      # Subtext gray

COLOR_PRIMARY = RGBColor(0x00, 0x4F, 0x7A)
COLOR_SECONDARY = RGBColor(0x1A, 0x52, 0x76)
COLOR_DARK = RGBColor(0x1E, 0x29, 0x3B)
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout_box(doc, text, title=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left thick border, no top/bottom/right
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{COLOR_PRIMARY_HEX}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        run_t = p.add_run(f"{title}\n")
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.bold = True
        run_t.font.color.rgb = COLOR_PRIMARY
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_DARK

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(4)

def build_docx(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = docx.Document()

    # Page Margins: 0.8 inch left/right/top/bottom
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.different_first_page_header_footer = True

        # Header for subsequent pages
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Pharmacy Management System - Low Level Design (LLD)")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED

        # Footer for subsequent pages
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        frun = fp.add_run("Confidential - For Internal Use Only                                                       Page Reference: POC-LLD-1.0")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = COLOR_MUTED

    # Helpers for paragraph styling
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = "Calibri"
            run_b.font.size = Pt(10.5)
            run_b.font.bold = True
            run_b.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = "Calibri"
            run_b.font.size = Pt(10)
            run_b.font.bold = True
            run_b.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_DARK
        return p

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(120)

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_t.add_run("PHARMACY MANAGEMENT SYSTEM")
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(28)
    run_t.font.bold = True
    run_t.font.color.rgb = COLOR_PRIMARY

    p_poc = doc.add_paragraph()
    p_poc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_poc.paragraph_format.space_before = Pt(8)
    run_poc = p_poc.add_run("POC")
    run_poc.font.name = "Calibri"
    run_poc.font.size = Pt(20)
    run_poc.font.bold = True
    run_poc.font.color.rgb = COLOR_SECONDARY

    p_lld = doc.add_paragraph()
    p_lld.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lld.paragraph_format.space_before = Pt(14)
    run_lld = p_lld.add_run("Low Level Design (LLD)")
    run_lld.font.name = "Calibri"
    run_lld.font.size = Pt(16)
    run_lld.font.color.rgb = COLOR_PRIMARY

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(240)

    # Bottom Metadata Table
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_l = meta_table.cell(0, 0)
    cell_r = meta_table.cell(0, 1)
    cell_l.width = Inches(4.5)
    cell_r.width = Inches(2.0)

    pl = cell_l.paragraphs[0]
    pl.paragraph_format.line_spacing = 1.2
    run_l1 = pl.add_run("PharmacyManagement Microservices\nPOC – Low Level Design (LLD)\n\n")
    run_l1.font.name = "Calibri"
    run_l1.font.size = Pt(11)
    run_l1.font.bold = True
    run_l1.font.color.rgb = COLOR_DARK
    run_l2 = pl.add_run("Date: 18/11/2026\nCurrent Document Version: [1.0]")
    run_l2.font.name = "Calibri"
    run_l2.font.size = Pt(10.5)
    run_l2.font.color.rgb = COLOR_DARK

    pr = cell_r.paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_r = pr.add_run("Author:\nLahari Chikoti")
    run_r.font.name = "Calibri"
    run_r.font.size = Pt(12)
    run_r.font.bold = True
    run_r.font.color.rgb = COLOR_PRIMARY

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: APPROVAL, CHANGE HISTORY & TABLE OF CONTENTS
    # =========================================================================
    add_h2("DOCUMENT APPROVAL Approvers of this document")
    t_app = doc.add_table(rows=4, cols=5)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_app)
    app_headers = ["Name", "Department", "Role", "Signature", "Date"]
    for i, h in enumerate(app_headers):
        c = t_app.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    app_rows = [
        ("Technical Review Board", "Architecture & Engineering", "Lead Architect", "Approved", "18/11/2026"),
        ("Solution Lead", ".NET Practice", "Solutions Lead", "Approved", "18/11/2026"),
        ("Project Manager", "Healthcare Deliveries", "Delivery Manager", "Approved", "18/11/2026")
    ]
    for r_idx, row in enumerate(app_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t_app.cell(r_idx, c_idx)
            set_cell_margins(c)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Document Change History")
    t_hist = doc.add_table(rows=2, cols=4)
    t_hist.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_hist)
    hist_headers = ["Document Version #", "Author", "Date", "Description"]
    for i, h in enumerate(hist_headers):
        c = t_hist.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    hist_vals = ["1.0", "Lahari Chikoti", "18/11/2026", "Pharmacy Management System Low Level Design (LLD)"]
    for i, val in enumerate(hist_vals):
        c = t_hist.cell(1, i)
        set_cell_margins(c)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Table of Contents")
    t_toc = doc.add_table(rows=21, cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_toc)
    for i, h in enumerate(["Section", "Title", "Page Reference"]):
        c = t_toc.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c, top=60, bottom=60)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    toc_items = [
        ("1.0", "Document Purpose", "3"),
        ("2.0", "Intended Audience", "3"),
        ("3.0", "Project Background and Objectives", "4"),
        ("4.0", "Requirements", "4"),
        ("5.0", "Design Patterns", "6"),
        ("6.0", "Flow Diagram", "7"),
        ("7.0", "Use Case Diagram", "8"),
        ("8.0", "Architecture Diagram", "9"),
        ("9.0", "Entity-Relationship Diagram", "10"),
        ("10.0", "Database Diagram", "11"),
        ("11.0", "Sequence Diagram", "12"),
        ("12.0", "Solution Steps", "13"),
        ("13.0", "Classes Names", "15"),
        ("14.0", "Validations", "17"),
        ("15.0", "API Catalogue", "18"),
        ("16.0", "HTTP Status Codes", "19"),
        ("17.0", "Integrations", "19"),
        ("18.0", "Sample API Requests", "20"),
        ("19.0", "Sample API Responses", "20"),
        ("20.0", "Unit Testing", "21")
    ]
    for r_idx, (sec, tit, pg) in enumerate(toc_items, start=1):
        c0 = t_toc.cell(r_idx, 0)
        c1 = t_toc.cell(r_idx, 1)
        c2 = t_toc.cell(r_idx, 2)
        set_cell_margins(c0, top=50, bottom=50)
        set_cell_margins(c1, top=50, bottom=50)
        set_cell_margins(c2, top=50, bottom=50)
        c0.paragraphs[0].add_run(sec).font.size = Pt(9)
        c1.paragraphs[0].add_run(tit).font.size = Pt(9)
        c2.paragraphs[0].add_run(pg).font.size = Pt(9)

    doc.add_page_break()

    # =========================================================================
    # SECTION 1.0 & 2.0
    # =========================================================================
    add_h1("1.0 Document Purpose")
    add_body(
        "This document describes the Low-Level Design (LLD) of the Pharmacy Management System POC, "
        "developed using C#, ASP.NET Core Web API, .NET 8, Entity Framework Core, LINQ, and Microsoft SQL Server "
        "under a distributed Microservices Architecture. It defines the internal MVC service structures, REST APIs, "
        "database-per-service isolation, authentication and role-based access control (RBAC), transactional integrity rules, "
        "and testing verification approach through interactive Swagger UI."
    )
    add_body(
        "The system consists of five decoupled services: Auth Service, Inventory Service, Order Service, "
        "Payment Service, and SaleReport Service. Each service encapsulates its own bounded context and database, "
        "exposing RESTful endpoints consumed by clinical staff, dispensing doctors, administrators, and external consumers."
    )

    add_h1("2.0 Intended Audience")
    add_body("This document is intended as a technical reference for the following stakeholders:")
    
    t_aud = doc.add_table(rows=6, cols=2)
    t_aud.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_aud)
    for i, h in enumerate(["Role", "Nature of Engagement in Pharmacy Management System Architecture"]):
        c = t_aud.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    aud_rows = [
        ("Product Owners / SMEs", "Ensure that the microservices design aligns strictly with pharmacy dispensing regulations, stock safety, and administrative workflows."),
        ("Business Analysts", "Map clinical and administrative requirements into technical service endpoints and entity specifications."),
        ("Enterprise Architects", "Review architectural consistency, database isolation boundaries, and inter-service HTTP REST communication standards."),
        ("Solution Architects", "Validate security patterns, JWT token issuance, EF Core LINQ query performance, and transactional boundaries."),
        ("Developers", "Use this document as an authoritative technical blueprint for implementing controllers, services, repositories, DTOs, and unit tests.")
    ]
    for r_idx, (role, desc) in enumerate(aud_rows, start=1):
        c0 = t_aud.cell(r_idx, 0)
        c1 = t_aud.cell(r_idx, 1)
        set_cell_margins(c0)
        set_cell_margins(c1)
        r0 = c0.paragraphs[0].add_run(role)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r1 = c1.paragraphs[0].add_run(desc)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)

    doc.add_page_break()

    # =========================================================================
    # SECTION 3.0 & 4.0
    # =========================================================================
    add_h1("3.0 Project Background and Objectives")
    add_h2("3.1 Project Background")
    add_body(
        "The Pharmacy Management System is an enterprise backend application engineered to modernize medication dispensing, "
        "wholesale pharmaceutical procurement, prescription order tracking, and financial analytics. Operating in clinical healthcare "
        "environments, the system enables Doctor users to browse medication catalogs with real-time stock availability, "
        "view unit prices, and place prescription drug orders. Simultaneously, Admin users maintain full control over the "
        "formulary (adding, editing, and deleting drugs), manage certified wholesale pharmaceutical suppliers, track batch purchase prices, "
        "verify doctor orders, mark completed patient counter collections in the 'PickedUp' section, and generate comprehensive sales "
        "and net profit reports."
    )
    add_body(
        "The application is structured into five independent microservices: Auth Service, Inventory Service, "
        "Order Service, Payment Service, and SaleReport Service. In accordance with microservices best practices, "
        "each microservice owns its dedicated database, preventing cross-database query coupling and enabling independent deployment."
    )

    add_h2("3.2 Project Objective")
    add_body("The primary objective is to deliver a robust, scalable, and maintainable backend using .NET 8, C# 12, Entity Framework Core, LINQ, and Microsoft SQL Server 2022. Key goals include:")
    add_bullet("Strict enforcement of the Database-per-Service pattern with zero cross-database joins.", "• Domain Isolation: ")
    add_bullet("Controllers expose clean REST contracts, Services enforce business rules, and Repositories execute LINQ queries.", "• Internal MVC Separation: ")
    add_bullet("Cryptographically signed JWT tokens with Role Claims (Admin vs Doctor) protecting critical endpoints.", "• Stateless Security: ")
    add_bullet("Atomic quantity decrementing during ordering, 1:1 unique payment enforcement, and immutable financial aggregation.", "• Data Consistency: ")
    add_bullet("Complete Swagger / OpenAPI 3.0 integration for interactive API validation without requiring a frontend.", "• Testing & Documentation: ")

    add_h1("4.0 Requirements")
    add_h2("4.1 Functional Requirements (FR)")
    add_body("For Admin Users:", bold_prefix=None)
    add_bullet("Secure registration and authentication with Name, Contact, Email, Password, and Role assignment.", "1. Login / Signup: ")
    add_bullet("Query and inspect complete catalog details including Drug Name, Description, Selling Price, Expiry Date, Quantity, and Availability.", "2. View Drugs: ")
    add_bullet("Full lifecycle formulary management with price validation and duplicate prevention.", "3. Add / Edit / Delete Drugs: ")
    add_bullet("Query registered pharmaceutical suppliers, contact emails, phone numbers, and physical addresses.", "4. View Suppliers: ")
    add_bullet("Vendor management to record verified wholesale distributors.", "5. Add / Edit / Delete Suppliers: ")
    add_bullet("Inspect orders submitted by all doctors, including items, unit prices, doctor identity, and timestamps.", "6. View Doctor Orders: ")
    add_bullet("Inspect order line items and update order status from Pending to Verified upon clinical validation.", "7. Verify Orders: ")
    add_bullet("Confirm counter collection and move verified orders to the fulfilled PickedUp state.", "8. Add Order to PickedUp Section: ")
    add_bullet("Query financial performance aggregated across Daily, Weekly, Monthly, and Yearly intervals.", "9. View Sales Reports: ")
    add_bullet("Export financial data as downloadable CSV spreadsheets or formatted printable receipt views.", "10. Download / Print Sales Report: ")

    add_body("For Doctor Users:", bold_prefix=None)
    add_bullet("Register with Name, Contact, Email, and Password to obtain Doctor privileges.", "1. Login / Signup: ")
    add_bullet("Browse active medication formularies with live stock levels and pricing.", "2. View Drugs: ")
    add_bullet("Place orders containing single or multiple medications, staging items in Cart/Pending status.", "3. Buy Drugs: ")

    add_h2("4.2 Non-Functional Requirements (NFR)")
    add_bullet("Microservices architecture with independent compilation, lifecycle, and dedicated databases.", "• Architecture: ")
    add_bullet("PBKDF2 with SHA-256 password hashing (100,000 iterations); HMAC-SHA256 signed JWT Bearer authentication.", "• Security: ")
    add_bullet("Monetary calculations (Selling Price, Purchase Price, Total Amount, Revenue, Profit) use DECIMAL(18,2).", "• Data Precision: ")
    add_bullet("All audit timestamps are recorded in UTC using DATETIME2(7).", "• Time Precision: ")
    add_bullet("Unified ApiResponse<T> envelope across all services returning Success, Message, Data, and Errors.", "• API Standardization: ")
    add_bullet("Full Swagger / OpenAPI 3.0 UI with Bearer Token Authorize button on every microservice.", "• Interactive Verification: ")

    add_h2("4.3 Technology Stack")
    t_tech = doc.add_table(rows=12, cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tech)
    for i, h in enumerate(["Category", "Technology", "Purpose"]):
        c = t_tech.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    tech_items = [
        ("Programming Language", "C# 12", "Core object-oriented backend programming language with strong typing and async/await."),
        ("Framework", "ASP.NET Core Web API", "High-performance REST API runtime for microservices endpoints."),
        ("Runtime", ".NET 8 (LTS)", "Enterprise Long-Term Support runtime providing modern memory and compute optimizations."),
        ("ORM & Data Access", "Entity Framework Core 8", "Object-Relational Mapping with Code-First modeling, LINQ queries, and migrations."),
        ("Database", "Microsoft SQL Server 2022", "Relational database engine hosting 5 isolated physical/logical database catalogs."),
        ("API Security", "JWT Bearer Authentication", "Stateless asymmetric authentication encoding user claims, email, and roles."),
        ("Authorization", "Role-Based Access Control (RBAC)", "Restricts sensitive APIs to authorized roles (Admin or Doctor)."),
        ("API Gateway", "YARP / Reverse Proxy", "Provides unified request routing, health checks, and cross-cutting security enforcement."),
        ("API Documentation", "Swagger UI / OpenAPI 3.0", "Interactive browser-based API testing sandbox with JWT lock integration."),
        ("Hosting / Runtime", "Kestrel / Native Process", "High-performance cross-platform self-hosted ASP.NET Core runtime."),
        ("Shared Library", "PharmacyManagement.Common", "Shared NuGet/class library standardizing JWT, hashing, constants, and envelopes.")
    ]
    for r_idx, (cat, tech, purp) in enumerate(tech_items, start=1):
        c0 = t_tech.cell(r_idx, 0)
        c1 = t_tech.cell(r_idx, 1)
        c2 = t_tech.cell(r_idx, 2)
        set_cell_margins(c0)
        set_cell_margins(c1)
        set_cell_margins(c2)
        r0 = c0.paragraphs[0].add_run(cat)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r1 = c1.paragraphs[0].add_run(tech)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r2 = c2.paragraphs[0].add_run(purp)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9)

    doc.add_page_break()

    # =========================================================================
    # SECTION 5.0: DESIGN PATTERNS
    # =========================================================================
    add_h1("5.0 Design Patterns")
    t_pat = doc.add_table(rows=9, cols=2)
    t_pat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_pat)
    for i, h in enumerate(["Name", "Description"]):
        c = t_pat.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    pat_rows = [
        ("Microservices Architecture", "Decomposes the system into 5 cohesive, independently deployable services organized around business domains: Auth, Inventory, Order, Payment, and SaleReport."),
        ("Database-Per-Service", "Each microservice exclusively owns its database schema. Direct cross-database SQL queries are forbidden; data is shared strictly via typed HTTP REST APIs."),
        ("Layered Architecture (Internal MVC)", "Internally, each microservice separates concerns into Controllers (API handling), Services (domain logic), and Repositories (EF Core LINQ data access)."),
        ("Repository Pattern", "Abstracts data-access logic from domain services, enabling testability and decoupling business algorithms from database access technologies."),
        ("Dependency Injection (DI)", "ASP.NET Core DI container manages service lifecycles (Scoped DbContexts, Repositories, and Services), promoting loose coupling and testability."),
        ("DTO (Data Transfer Object) Pattern", "Dedicated request and response DTOs prevent over-posting, hide internal database primary keys where appropriate, and enforce request validation."),
        ("API Gateway Pattern", "Centralizes client entry points, handles request forwarding, rate limiting, and decouples internal service ports from client consumers."),
        ("Transactional Outbox / Idempotency", "Payment and stock operations use unique transaction references and idempotent validation to prevent double-charging or duplicate deductions.")
    ]
    for r_idx, (name, desc) in enumerate(pat_rows, start=1):
        c0 = t_pat.cell(r_idx, 0)
        c1 = t_pat.cell(r_idx, 1)
        set_cell_margins(c0)
        set_cell_margins(c1)
        r0 = c0.paragraphs[0].add_run(name)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r1 = c1.paragraphs[0].add_run(desc)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)

    doc.add_page_break()

    # =========================================================================
    # SECTION 6.0: FLOW DIAGRAM
    # =========================================================================
    add_h1("6.0 Flow Diagram")
    flow_img = os.path.join(DIAGRAMS_DIR, "04_Flow_Diagram.jpg")
    if os.path.exists(flow_img):
        doc.add_picture(flow_img, width=Inches(5.4))
    add_h2("Description")
    add_body(
        "The flow diagram models the end-to-end operational execution of the Pharmacy Management System across both Admin "
        "and Doctor / Customer roles. Execution begins at the START pill with user registration and authentication. "
        "Upon successful credential verification, a decision diamond evaluates the user's role: "
        "Admin / Owner branches to inventory procurement, formulary maintenance, order validation, order verification, counter "
        "handover (PickedUp), and financial report generation. "
        "The Doctor User / Customer branches to drug catalog browsing, verifying live quantities and expiry dates, selecting "
        "medications, and placing prescription orders."
    )
    add_body(
        "The central processing pipeline models transactional coordination: verifying stock levels, creating the order record in "
        "OrderDB, executing atomic stock decrements in InventoryDB, computing itemized totals, and executing payment checkout. "
        "A Payment Successful? decision handles branching: if successful, the order transitions to Verified, generates an invoice, "
        "and prepares for counter collection (PickedUp). If payment fails, the system executes the Payment Failed Container "
        "workflow: displaying failure diagnostics, updating the order to PaymentFailed, and either retrying checkout or cancelling the "
        "order and restoring reserved stock before reaching END."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 7.0: USE CASE DIAGRAM
    # =========================================================================
    add_h1("7.0 Use Case Diagram")
    usecase_img = os.path.join(DIAGRAMS_DIR, "02_Use_Case_Diagram.jpg")
    if os.path.exists(usecase_img):
        doc.add_picture(usecase_img, width=Inches(6.5))
    add_h2("Description")
    add_body(
        "The use case diagram illustrates the functional interactions between the two primary actors—Admin and Doctor—and "
        "the Pharmacy Management System boundary. Both actors associate with the foundational Login / Authenticate use case, "
        "which issues role-bearing JWT tokens governing downstream access."
    )
    add_body(
        "Admin Actor (12 Use Cases): Full administrative control encompassing User Management, Drug Formularies (Add/Update/Delete), "
        "Supplier Management, Stock Inwarding, Viewing All Doctor Orders, Validating Order Line Items, Verifying Orders (Pending -> Verified), "
        "Moving Orders to PickedUp Section, Viewing PickedUp Orders, Generating Financial Sales Reports, Downloading CSV Spreadsheets, and "
        "Printing Formatted Receipts."
    )
    add_body(
        "Doctor Actor (7 Use Cases): Clinical user actions including Doctor Signup/Login, Browsing Drug Catalogs, Checking Expiry Dates "
        "& Quantities, Placing Medication Orders, Viewing Personal Order Histories, Tracking Order Status (Cart -> Pending -> Verified -> PickedUp), "
        "and Submitting Online Payments."
    )
    add_body(
        "The diagram explicitly defines core workflow relationships: placing an order <<includes>> Managing Order Lifecycle, "
        "which in turn <<includes>> Deducting Drug Stock Atomically, Processing 1:1 Payment, and Generating Itemized Invoices, "
        "with an <<extend>> association for Order Cancellation upon stock exhaustion."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 8.0: ARCHITECTURE DIAGRAM
    # =========================================================================
    add_h1("8.0 Architecture Diagram")
    arch_img = os.path.join(DIAGRAMS_DIR, "01_Solution_Architecture_Diagram.jpg")
    if os.path.exists(arch_img):
        doc.add_picture(arch_img, width=Inches(6.5))
    add_h2("Description")
    add_body(
        "The architecture diagram represents the distributed microservices topology of the Pharmacy Management System. "
        "Clients—including the interactive Swagger UI, Web clients, and point-of-sale terminals—interact with the backend through an "
        "API Gateway (YARP / Reverse Proxy). The Gateway centralizes request routing, load balancing, SSL termination, and rate limiting."
    )
    add_body(
        "The core domain comprises five independent ASP.NET Core Web API microservices:\n"
        "1. Auth Service (Port 5001): Manages user registrations, PBKDF2 credential verification, and asymmetric JWT issuance.\n"
        "2. Inventory Service (Port 5002): Manages the pharmaceutical formulary, certified suppliers, stock inwarding, and atomic deductions.\n"
        "3. Order Service (Port 5003): Coordinates doctor orders, order item lines, admin verification, and counter collection handovers.\n"
        "4. Payment Service (Port 5004): Processes multi-method checkouts under a strict 1:1 unique order constraint.\n"
        "5. SaleReport Service (Port 5005): Aggregates financial performance, calculating gross revenue, cost of goods sold, and net profit."
    )
    add_body(
        "Each service maintains its dedicated Microsoft SQL Server database. Cross-cutting utilities—including JWT handlers, password hashing, "
        "and standard response envelopes—are centralized within the shared PharmacyManagement.Common class library."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 9.0: ENTITY-RELATIONSHIP (ER) DIAGRAM
    # =========================================================================
    add_h1("9.0 Entity-Relationship Diagram")
    er_img = os.path.join(DIAGRAMS_DIR, "05_ER_Diagram.jpg")
    if os.path.exists(er_img):
        doc.add_picture(er_img, width=Inches(6.5))
    add_h2("Description")
    add_body(
        "The Entity-Relationship (ER) diagram defines the data models and cardinalities across the five microservices. "
        "In strict adherence to microservice isolation, physical foreign keys with database-level cascading rules exist exclusively "
        "within individual service boundaries, while cross-service associations operate as logical foreign keys resolved via REST APIs:"
    )
    add_bullet("A Doctor user in AuthDB can place multiple medication orders. Orders.DoctorID logically references Users.UserId.", "• User to Order (1:M): ")
    add_bullet("A physical database foreign key with ON DELETE CASCADE in OrderDB ensuring complete cleanup of child line items.", "• Order to OrderItem (1:M): ")
    add_bullet("OrderItems.DrugId logically references Drugs.DrugId in InventoryDB, storing an immutable snapshot of DrugName for historical receipt accuracy.", "• Drug to OrderItem (1:M): ")
    add_bullet("Physical foreign keys in InventoryDB tracking wholesale stock receipts with purchase prices.", "• Supplier to Inventory (1:M) & Drug to Inventory (1:M): ")
    add_bullet("A strict one-to-one relationship enforced by a UNIQUE INDEX on Payments.OrderId in PaymentDB.", "• Order to Payment (1:1): ")
    add_bullet("A standalone reporting entity aggregating financial totals across order and inventory data without locking transaction tables.", "• SaleReport (Standalone): ")
    doc.add_page_break()

    # =========================================================================
    # SECTION 10.0: DATABASE DIAGRAM
    # =========================================================================
    add_h1("10.0 Database Diagram")
    db_img = os.path.join(DIAGRAMS_DIR, "06_Database_Schema_Diagram.jpg")
    if os.path.exists(db_img):
        doc.add_picture(db_img, width=Inches(6.5))
    add_h2("Description")
    add_body(
        "The database diagram illustrates the Database-per-Service physical schema design implemented in Microsoft SQL Server 2022. "
        "The system partitions data into five dedicated databases: Pharmacy_UserDB, Pharmacy_InventoryDB, Pharmacy_OrderDB, "
        "Pharmacy_PaymentDB, and Pharmacy_SaleReportDB."
    )
    add_body(
        "Each table definition specifies primary clustered keys, non-clustered indexes on search predicates (such as Users.Role, Drugs.IsAvailable, "
        "Orders.Status), and check constraints. All monetary values (e.g. Drugs.Price, Inventory.PurchasePrice, Orders.TotalAmount, Payments.Amount, "
        "SaleReports.TotalRevenue, SaleReports.Profit) strictly employ DECIMAL(18,2) to prevent floating-point rounding errors. All audit and transaction "
        "timestamps utilize DATETIME2(7) in UTC format."
    )
    add_body(
        "Database scripts are fully scripted in scripts/InitDatabases.sql with idempotent guards (IF NOT EXISTS), enabling automated database creation "
        "and seed data provisioning on any local SQL Server developer environment."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 11.0: SEQUENCE DIAGRAM
    # =========================================================================
    add_h1("11.0 Sequence Diagram")
    seq_img = os.path.join(DIAGRAMS_DIR, "03_Sequence_Diagram.jpg")
    if os.path.exists(seq_img):
        doc.add_picture(seq_img, width=Inches(6.5))
    add_h2("Description")
    add_body(
        "The sequence diagram details the runtime interaction between the Doctor User, Admin User, API Gateway, and all "
        "five microservices across the complete order fulfillment and financial reporting lifecycle across 24 synchronous REST messages:"
    )
    add_bullet("Doctor authenticates with email/password; AuthService validates credentials against AuthDB and returns a signed JWT Bearer Token encoding the Doctor role claim.", "1. Authentication (Steps 1–4): ")
    add_bullet("Doctor passes the token to query active medications; InventoryService queries InventoryDB and returns available drugs with prices.", "2. Catalog Browsing (Steps 5–7): ")
    add_bullet("Doctor submits an order. OrderService stages the order in Pending status and calls InventoryService to decrement stock atomically. InventoryService verifies availability, deducts quantities, and returns success.", "3. Order Placement & Stock Decrement (Steps 8–12): ")
    add_bullet("Doctor triggers payment; PaymentService validates the 1:1 constraint, persists the payment record, and returns a unique transaction reference.", "4. Payment Processing (Steps 13–15): ")
    add_bullet("Admin queries all doctor orders, inspects order line items, validates stock, updates status to Verified, and marks final handover in PickedUp.", "5. Admin Verification & Handover (Steps 16–22): ")
    add_bullet("Admin requests sales reporting; SaleReportService aggregates verified orders, calculates net profit, and returns a financial summary.", "6. Sales Analytics (Steps 23–24): ")
    doc.add_page_break()

    # =========================================================================
    # SECTION 12.0: SOLUTION STEPS
    # =========================================================================
    add_h1("12.0 Solution Steps")
    add_h2("12.1 Customer / Doctor and Admin Registration and Login")
    add_bullet("The user submits registration details (Name, Contact, Email, Password, Role) to AuthService.")
    add_bullet("AuthService verifies email uniqueness in Pharmacy_UserDB and hashes the password using PBKDF2 with HMAC-SHA256 (100,000 iterations).")
    add_bullet("Upon login, AuthService validates credentials and generates a cryptographically signed JWT token containing UserId, Email, and Role claims.")
    add_bullet("The client provides the JWT token via the Authorization: Bearer <token> header for all protected endpoints in Swagger UI.")

    add_h2("12.2 Admin Manages Drugs & Pricing")
    add_bullet("Admin provides the JWT token to access formulary endpoints on InventoryService (Port 5002).")
    add_bullet("Admin creates new drugs by specifying Drug Name, Description, Selling Price, Expiry Date, and Initial Quantity.")
    add_bullet("Admin updates existing medications or deletes discontinued drugs from Pharmacy_InventoryDB.")

    add_h2("12.3 Admin Manages Suppliers & Stock Inventory")
    add_bullet("Admin registers verified pharmaceutical distributors by submitting Supplier Name, Contact Email, Phone, and Address.")
    add_bullet("When new stock arrives, Admin creates an Inventory inward record associating SupplierId, DrugId, PurchasePrice, and QuantityAdded.")
    add_bullet("InventoryService increments Drugs.Quantity and updates Drugs.IsAvailable = true automatically.")

    add_h2("12.4 Doctor Searches & Views Available Drugs")
    add_bullet("Doctor queries GET /api/drugs?availableOnly=true to view only in-stock and non-expired medications.")
    add_bullet("InventoryService runs LINQ queries filtering IsAvailable == true and Quantity > 0, returning catalog items with selling prices.")

    add_h2("12.5 Doctor Buys Drugs (Places Order)")
    add_bullet("Doctor selects one or more medications and submits POST /api/orders with an array of DrugId and Quantity.")
    add_bullet("OrderService extracts DoctorID from the JWT token and verifies requested drugs.")
    add_bullet("OrderService communicates via HTTP with InventoryService to atomically decrement stock.")
    add_bullet("OrderService computes TotalAmount = Sum(Quantity * UnitPrice) and saves the order in Pending status.")

    add_h2("12.6 Payment Processing")
    add_bullet("Doctor submits payment details to PaymentService (POST /api/payments) specifying OrderId, Amount, and PaymentMethod (CreditCard, UPI, NetBanking, Cash).")
    add_bullet("PaymentService verifies that the order has no prior payment, enforcing the 1:1 payment rule.")
    add_bullet("PaymentService generates a unique TransactionReference (e.g., TXN-A83F91B2C4D5), persists the record in Pharmacy_PaymentDB, and marks PaymentStatus = Completed.")

    add_h2("12.7 Admin Order Verification & Pickup Handover")
    add_bullet("Admin accesses GET /api/orders to inspect orders placed by all doctors across the hospital/clinic.")
    add_bullet("Admin reviews the line items, confirms stock validity, and calls PUT /api/orders/{id}/verify, setting Status = Verified.")
    add_bullet("When the doctor or patient arrives at the pharmacy dispensing counter, Admin calls PUT /api/orders/{id}/pickup, transferring the order to the PickedUp section.")

    add_h2("12.8 Admin Sales Report Generation, CSV Download & Print")
    add_bullet("Admin accesses SaleReportService (Port 5005) and calls POST /api/salereports/generate with a range (Daily, Weekly, Monthly, or Yearly).")
    add_bullet("SaleReportService aggregates verified orders, calculates Gross Revenue, aggregates wholesale COGS purchase costs from Inventory, and computes net Profit.")
    add_bullet("Admin downloads the report as an RFC-4180 compliant CSV spreadsheet (GET /api/salereports/{id}/download) or views a formatted ASCII receipt (GET /api/salereports/{id}/print).")

    doc.add_page_break()

    # =========================================================================
    # SECTION 13.0: CLASSES NAMES
    # =========================================================================
    add_h1("13.0 Classes Names")
    add_h2("Entities (Domain Models)")
    t_m = doc.add_table(rows=9, cols=3)
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_m)
    for i, h in enumerate(["S.No", "Class Name", "Description"]):
        c = t_m.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    model_rows = [
        ("1", "User.cs", "Represents user accounts in AuthDB with UserId PK, Name, Email, PhoneNumber, PasswordHash, Role (Admin/Doctor), IsActive, and CreatedDate."),
        ("2", "Drug.cs", "Represents formulary medications in InventoryDB with DrugId PK, Name, Description, Price (selling price), ExpiryDate, Quantity, and IsAvailable."),
        ("3", "Supplier.cs", "Represents wholesale vendors in InventoryDB with SupplierId PK, SupplierName, Email, PhoneNumber, and Address."),
        ("4", "Inventory.cs", "Represents stock inwarding batches in InventoryDB with InventoryId PK, SupplierId FK, DrugId FK, PurchasePrice, QuantityAdded, and StockReceivedDate."),
        ("5", "Order.cs", "Represents orders in OrderDB with OrderId PK, DoctorID logical FK, OrderDate, TotalAmount, and Status (Cart/Pending/Verified/PickedUp)."),
        ("6", "OrderItem.cs", "Represents line items in OrderDB with OrderItemId PK, OrderId FK, DrugId logical FK, DrugName snapshot, Quantity, and UnitPrice."),
        ("7", "Payment.cs", "Represents payment records in PaymentDB with PaymentId PK, OrderId 1:1 unique FK, Amount, PaymentDate, PaymentMethod, PaymentStatus, and TransactionReference."),
        ("8", "SaleReport.cs", "Represents financial reports in SaleReportDB with SaleReportId PK, ReportType (Daily/Weekly/Monthly/Yearly), FromDate, ToDate, TotalOrders, TotalRevenue, GeneratedDate, and Profit.")
    ]
    for r_idx, (sno, cname, desc) in enumerate(model_rows, start=1):
        c0, c1, c2 = t_m.cell(r_idx, 0), t_m.cell(r_idx, 1), t_m.cell(r_idx, 2)
        set_cell_margins(c0); set_cell_margins(c1); set_cell_margins(c2)
        c0.paragraphs[0].add_run(sno).font.size = Pt(9)
        r1 = c1.paragraphs[0].add_run(cname)
        r1.font.bold = True
        r1.font.size = Pt(9)
        c2.paragraphs[0].add_run(desc).font.size = Pt(9)

    add_h2("Controllers (API Layer)")
    t_c = doc.add_table(rows=8, cols=3)
    t_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_c)
    for i, h in enumerate(["S.No", "Class Name", "Description"]):
        c = t_c.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    ctrl_rows = [
        ("1", "AuthController.cs", "Exposes user signup (/register), login (/login), and profile (/me) endpoints under JWT authentication."),
        ("2", "DrugsController.cs", "Exposes catalog retrieval, filtering, and Admin CRUD operations (/api/drugs)."),
        ("3", "SuppliersController.cs", "Exposes Admin CRUD management for certified wholesale pharmaceutical suppliers (/api/suppliers)."),
        ("4", "InventoryController.cs", "Handles stock inwarding batches and inter-service atomic quantity deductions (/api/inventory)."),
        ("5", "OrdersController.cs", "Handles doctor order placement, order verification, counter handover (PickedUp), and order retrieval (/api/orders)."),
        ("6", "PaymentsController.cs", "Handles checkout transactions and enforces the 1:1 order payment rule (/api/payments)."),
        ("7", "SaleReportsController.cs", "Handles report generation, range filtering, CSV spreadsheet download, and printable formatting (/api/salereports).")
    ]
    for r_idx, (sno, cname, desc) in enumerate(ctrl_rows, start=1):
        c0, c1, c2 = t_c.cell(r_idx, 0), t_c.cell(r_idx, 1), t_c.cell(r_idx, 2)
        set_cell_margins(c0); set_cell_margins(c1); set_cell_margins(c2)
        c0.paragraphs[0].add_run(sno).font.size = Pt(9)
        r1 = c1.paragraphs[0].add_run(cname)
        r1.font.bold = True
        r1.font.size = Pt(9)
        c2.paragraphs[0].add_run(desc).font.size = Pt(9)

    doc.add_page_break()

    add_h2("Services (Business Logic Layer)")
    t_s = doc.add_table(rows=9, cols=3)
    t_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_s)
    for i, h in enumerate(["S.No", "Class Name", "Description"]):
        c = t_s.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    svc_rows = [
        ("1", "IAuthService.cs / AuthService.cs", "Implements user registration, duplicate email validation, credential checking, and JWT issuance."),
        ("2", "IDrugService.cs / DrugService.cs", "Implements drug validation, price verification, stock checks, and availability flags."),
        ("3", "ISupplierService.cs / SupplierService.cs", "Implements vendor registration, email/phone format checks, and supplier cataloging."),
        ("4", "IInventoryService.cs / InventoryService.cs", "Coordinates stock inwarding batches, updates drug balances, and executes atomic stock decrements."),
        ("5", "IOrderService.cs / OrderService.cs", "Validates line items, invokes Inventory Service via HTTP client, computes totals, and manages order lifecycle."),
        ("6", "IPaymentService.cs / PaymentService.cs", "Validates order payment eligibility, checks 1:1 uniqueness constraint, and generates transaction codes."),
        ("7", "ISaleReportService.cs / SaleReportService.cs", "Aggregates order data, computes net profit over purchase costs, and formats CSV and print layouts."),
        ("8", "JwtTokenGenerator.cs / PasswordHasher.cs", "Common security primitives implementing HMAC-SHA256 JWT generation and PBKDF2 salt hashing.")
    ]
    for r_idx, (sno, cname, desc) in enumerate(svc_rows, start=1):
        c0, c1, c2 = t_s.cell(r_idx, 0), t_s.cell(r_idx, 1), t_s.cell(r_idx, 2)
        set_cell_margins(c0); set_cell_margins(c1); set_cell_margins(c2)
        c0.paragraphs[0].add_run(sno).font.size = Pt(9)
        r1 = c1.paragraphs[0].add_run(cname)
        r1.font.bold = True
        r1.font.size = Pt(9)
        c2.paragraphs[0].add_run(desc).font.size = Pt(9)

    add_h2("Repositories (Data Access Layer & EF Core DbContexts)")
    t_r = doc.add_table(rows=8, cols=3)
    t_r.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_r)
    for i, h in enumerate(["S.No", "Class Name", "Description"]):
        c = t_r.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    repo_rows = [
        ("1", "UserRepository.cs / AuthDbContext.cs", "Executes LINQ queries against Pharmacy_UserDB for user authentication and profile retrieval."),
        ("2", "DrugRepository.cs / InventoryDbContext.cs", "Executes LINQ queries against Pharmacy_InventoryDB for drug CRUD and atomic decrement updates."),
        ("3", "SupplierRepository.cs", "Executes LINQ queries for pharmaceutical vendor persistence in Pharmacy_InventoryDB."),
        ("4", "InventoryRepository.cs", "Persists stock inward batches and links suppliers with drugs in Pharmacy_InventoryDB."),
        ("5", "OrderRepository.cs / OrderDbContext.cs", "Persists orders and child order items with cascading integrity in Pharmacy_OrderDB."),
        ("6", "PaymentRepository.cs / PaymentDbContext.cs", "Persists payment transactions and enforces unique index on OrderId in Pharmacy_PaymentDB."),
        ("7", "SaleReportRepository.cs / SaleReportDbContext.cs", "Persists aggregated financial reports and date-range queries in Pharmacy_SaleReportDB.")
    ]
    for r_idx, (sno, cname, desc) in enumerate(repo_rows, start=1):
        c0, c1, c2 = t_r.cell(r_idx, 0), t_r.cell(r_idx, 1), t_r.cell(r_idx, 2)
        set_cell_margins(c0); set_cell_margins(c1); set_cell_margins(c2)
        c0.paragraphs[0].add_run(sno).font.size = Pt(9)
        r1 = c1.paragraphs[0].add_run(cname)
        r1.font.bold = True
        r1.font.size = Pt(9)
        c2.paragraphs[0].add_run(desc).font.size = Pt(9)

    doc.add_page_break()

    # =========================================================================
    # SECTION 14.0: VALIDATIONS
    # =========================================================================
    add_h1("14.0 Validations")
    validations = [
        ("User Registration Validations: ", "Strict email format validation, duplicate email checking, minimum 6-character password requirements, and mandatory valid Role (Admin or Doctor)."),
        ("JWT Security Token Verification: ", "Validates cryptographic HMAC-SHA256 signature, issuer (PharmacyManagementAuthService), audience (PharmacyManagementMicroservices), non-expiration, and valid Role claims on protected endpoints."),
        ("Role-Based Access Control: ", "Enforces endpoint policies ensuring only Admin users can modify drugs, suppliers, or verify orders, and only Doctor users can initiate order placement."),
        ("Drug Pricing & Expiry Validation: ", "Requires Price > 0, non-negative Quantity >= 0, and ExpiryDate > DateTime.UtcNow during drug creation and order submission."),
        ("Supplier Profile Validation: ", "Enforces valid email syntax, valid international phone number format, and non-empty physical supplier addresses."),
        ("Stock Inwarding Validation: ", "Verifies that SupplierId and DrugId exist prior to recording stock inward batches, and requires PurchasePrice > 0 and QuantityAdded > 0."),
        ("Atomic Stock Availability Verification: ", "Before staging an order, the system checks Quantity >= RequestedQuantity. If insufficient, the order fails with an explicit out-of-stock validation error."),
        ("Atomic Decrement Concurrency Guard: ", "Automatically updates Drugs.IsAvailable = false when stock drops to 0, preventing race-condition over-selling."),
        ("1:1 Order Payment Enforcement: ", "The system verifies that OrderId has not already been billed (Payments.OrderId unique constraint), preventing double payments."),
        ("Order State Machine Rules: ", "Enforces strict state transitions: Cart -> Pending -> Verified -> PickedUp. Only orders in Verified status can be marked as PickedUp."),
        ("Doctor Order Isolation: ", "Doctors can query only their own orders (DoctorID == Claims.UserId), whereas Admins have global visibility across all hospital orders."),
        ("Report Date Range Validation: ", "Validates that ToDate >= FromDate and ensures valid ReportType enum values (Daily, Weekly, Monthly, Yearly).")
    ]
    for b_prefix, b_text in validations:
        add_bullet(b_text, b_prefix)

    doc.add_page_break()

    # =========================================================================
    # SECTION 15.0: API CATALOGUE
    # =========================================================================
    add_h1("15.0 API Catalogue")
    api_items = [
        ("Authentication", "/api/auth/register", "POST", "Public"),
        ("Authentication", "/api/auth/login", "POST", "Public"),
        ("Authentication", "/api/auth/me", "GET", "Admin / Doctor"),
        ("Authentication", "/api/auth/users", "GET", "Admin"),
        ("Drugs", "/api/drugs", "GET", "Admin / Doctor"),
        ("Drugs", "/api/drugs/{id}", "GET", "Admin / Doctor"),
        ("Drugs", "/api/drugs", "POST", "Admin"),
        ("Drugs", "/api/drugs/{id}", "PUT", "Admin"),
        ("Drugs", "/api/drugs/{id}", "DELETE", "Admin"),
        ("Drugs", "/api/drugs/deduct-stock", "POST", "Internal / Authenticated"),
        ("Suppliers", "/api/suppliers", "GET", "Admin"),
        ("Suppliers", "/api/suppliers/{id}", "GET", "Admin"),
        ("Suppliers", "/api/suppliers", "POST", "Admin"),
        ("Suppliers", "/api/suppliers/{id}", "PUT", "Admin"),
        ("Suppliers", "/api/suppliers/{id}", "DELETE", "Admin"),
        ("Inventory", "/api/inventory", "GET", "Admin"),
        ("Inventory", "/api/inventory", "POST", "Admin"),
        ("Orders", "/api/orders", "POST", "Doctor"),
        ("Orders", "/api/orders", "GET", "Admin / Doctor"),
        ("Orders", "/api/orders/{id}", "GET", "Admin / Doctor"),
        ("Orders", "/api/orders/{id}/verify", "PUT", "Admin"),
        ("Orders", "/api/orders/{id}/pickup", "PUT", "Admin"),
        ("Orders", "/api/orders/pickedup", "GET", "Admin"),
        ("Payments", "/api/payments", "POST", "Doctor / Admin"),
        ("Payments", "/api/payments/order/{orderId}", "GET", "Doctor / Admin"),
        ("Payments", "/api/payments/{id}", "GET", "Admin"),
        ("Sales Reports", "/api/salereports/generate", "POST", "Admin"),
        ("Sales Reports", "/api/salereports", "GET", "Admin"),
        ("Sales Reports", "/api/salereports/{id}/download", "GET", "Admin"),
        ("Sales Reports", "/api/salereports/{id}/print", "GET", "Admin")
    ]
    t_api = doc.add_table(rows=len(api_items) + 1, cols=4)
    t_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_api)
    for i, h in enumerate(["Module", "Endpoint", "Method", "Access"]):
        c = t_api.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    for r_idx, (mod, ep, meth, acc) in enumerate(api_items, start=1):
        c0, c1, c2, c3 = t_api.cell(r_idx, 0), t_api.cell(r_idx, 1), t_api.cell(r_idx, 2), t_api.cell(r_idx, 3)
        set_cell_margins(c0, top=40, bottom=40)
        set_cell_margins(c1, top=40, bottom=40)
        set_cell_margins(c2, top=40, bottom=40)
        set_cell_margins(c3, top=40, bottom=40)
        c0.paragraphs[0].add_run(mod).font.size = Pt(8.5)
        r1 = c1.paragraphs[0].add_run(ep)
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        c2.paragraphs[0].add_run(meth).font.size = Pt(8.5)
        c3.paragraphs[0].add_run(acc).font.size = Pt(8.5)

    doc.add_page_break()

    # =========================================================================
    # SECTION 16.0 & 17.0: HTTP STATUS CODES & INTEGRATIONS
    # =========================================================================
    add_h1("16.0 HTTP Status Codes")
    http_items = [
        ("200", "OK", "The request processed successfully and returned requested entity data."),
        ("201", "Created", "A new resource (User, Drug, Order, Payment, or SaleReport) was created successfully."),
        ("204", "No Content", "The request was completed successfully and no response payload is required."),
        ("400", "Bad Request", "Validation failed (e.g. invalid email format, insufficient stock, negative price, or malformed JSON)."),
        ("401", "Unauthorized", "Missing, expired, or invalid JWT Bearer token, or invalid login credentials."),
        ("403", "Forbidden", "Authenticated user does not possess the required role (e.g., Doctor attempting Admin operations)."),
        ("404", "Not Found", "Requested Drug, Supplier, Order, Payment, or Report was not found in the database."),
        ("409", "Conflict", "State conflict occurred (e.g., duplicate email address, duplicate 1:1 payment for an order)."),
        ("500", "Internal Server Error", "An unhandled exception or database connection error occurred during execution.")
    ]
    t_http = doc.add_table(rows=len(http_items) + 1, cols=3)
    t_http.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_http)
    for i, h in enumerate(["Status Code", "Status", "Description"]):
        c = t_http.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    for r_idx, (sc, st, desc) in enumerate(http_items, start=1):
        c0, c1, c2 = t_http.cell(r_idx, 0), t_http.cell(r_idx, 1), t_http.cell(r_idx, 2)
        set_cell_margins(c0); set_cell_margins(c1); set_cell_margins(c2)
        r0 = c0.paragraphs[0].add_run(sc)
        r0.font.bold = True
        r0.font.size = Pt(9)
        c1.paragraphs[0].add_run(st).font.size = Pt(9)
        c2.paragraphs[0].add_run(desc).font.size = Pt(9)

    add_h1("17.0 Integrations")
    integrations = [
        ("REST APIs (Typed HttpClient): ", "Enables synchronous inter-service HTTP communication between OrderService and InventoryService for atomic stock validation and deduction."),
        ("JWT Bearer Token Security: ", "Stateless cryptographic authentication passing user identity (UserId), email, and roles across microservices."),
        ("Microsoft SQL Server 2022: ", "Hosts 5 isolated databases (Pharmacy_UserDB, Pharmacy_InventoryDB, Pharmacy_OrderDB, Pharmacy_PaymentDB, Pharmacy_SaleReportDB)."),
        ("Entity Framework Core 8: ", "Manages object-relational mapping, code-first migrations, and LINQ execution."),
        ("Swagger / OpenAPI 3.0: ", "Interactive API documentation and testing interface on every microservice."),
        ("CSV & Printable Output: ", "Financial report generation providing RFC-4180 CSV export and ASCII receipts.")
    ]
    for b_prefix, b_text in integrations:
        add_bullet(b_text, b_prefix)

    doc.add_page_break()

    # =========================================================================
    # SECTION 18.0 & 19.0: SAMPLE REQUESTS & RESPONSES
    # =========================================================================
    add_h1("18.0 Sample API Requests")
    add_h2("Doctor Order Creation Request (POST /api/orders)")
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
    add_callout_box(doc, req_json, "JSON Request Payload:")

    add_h2("Order Payment Checkout Request (POST /api/payments)")
    pay_req_json = (
        "{\n"
        '  "orderId": 1,\n'
        '  "amount": 25.50,\n'
        '  "paymentMethod": "CreditCard"\n'
        "}"
    )
    add_callout_box(doc, pay_req_json, "JSON Request Payload:")

    add_h1("19.0 Sample API Responses")
    add_h2("Successful Order Creation Response (Status: 201 Created)")
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
    add_callout_box(doc, res_json, "JSON Response Payload:")

    doc.add_page_break()

    # =========================================================================
    # SECTION 20.0: UNIT TESTING
    # =========================================================================
    add_h1("20.0 Unit Testing")
    add_body("The system is verified using an automated NUnit test matrix covering core service layer scenarios:")

    test_items = [
        ("TC-01", "Auth", "Register new Doctor user with valid email and password.", "User record is saved in UserDB and returns 201 Created."),
        ("TC-02", "Auth", "Register using an email that already exists in UserDB.", "Returns 409 Conflict with duplicate email validation error."),
        ("TC-03", "Auth", "Login with valid credentials for Doctor user.", "Returns 200 OK with valid signed JWT Bearer token and Role claim."),
        ("TC-04", "Auth", "Login with invalid password.", "Returns 401 Unauthorized with credential error message."),
        ("TC-05", "Inventory", "Admin creates new drug with valid price and expiry date.", "Drug is created in InventoryDB with IsAvailable = true."),
        ("TC-06", "Inventory", "Admin attempts to create drug with negative price.", "Validation fails with 400 Bad Request."),
        ("TC-07", "Inventory", "Query available drugs when some medications have Quantity = 0.", "Returns only medications with IsAvailable = true and Quantity > 0."),
        ("TC-08", "Inventory", "Atomic stock decrement when sufficient stock is available.", "Quantity is reduced by requested amount; returns 200 OK."),
        ("TC-09", "Inventory", "Atomic stock decrement when requested quantity exceeds available stock.", "Operation is rejected; stock remains unchanged."),
        ("TC-10", "Order", "Doctor creates order with available medications.", "Order is staged in Pending status with calculated TotalAmount."),
        ("TC-11", "Order", "Doctor attempts to place order for expired or out-of-stock medication.", "Order creation is rejected with stock validation error."),
        ("TC-12", "Order", "Doctor queries own orders.", "Returns only orders associated with the authenticated DoctorID."),
        ("TC-13", "Order", "Admin verifies valid pending order.", "Order status transitions from Pending to Verified."),
        ("TC-14", "Order", "Admin marks verified order as PickedUp.", "Order status transitions to PickedUp; visible in PickedUp query."),
        ("TC-15", "Payment", "Process payment for verified order with valid amount.", "Payment is saved in PaymentDB with Status = Completed."),
        ("TC-16", "Payment", "Attempt duplicate payment for an order with existing payment record.", "1:1 constraint rejects operation with 409 Conflict."),
        ("TC-17", "SaleReport", "Generate Daily sales report for current date range.", "Aggregates orders, computes revenue, costs, and profit."),
        ("TC-18", "SaleReport", "Download sales report as CSV.", "Returns file with text/csv MIME type and RFC-4180 headers."),
        ("TC-19", "SaleReport", "Generate report with invalid date range (FromDate > ToDate).", "Validation fails with 400 Bad Request."),
        ("TC-20", "Security", "Doctor attempts to access Admin drug creation endpoint.", "Request is blocked with 403 Forbidden.")
    ]
    t_test = doc.add_table(rows=len(test_items) + 1, cols=4)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_test)
    for i, h in enumerate(["Test Case ID", "Module", "Test Scenario", "Expected Result"]):
        c = t_test.cell(0, i)
        set_cell_background(c, COLOR_HEADER_BG)
        set_cell_margins(c)
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True

    for r_idx, (tcid, mod, scen, exp) in enumerate(test_items, start=1):
        c0, c1, c2, c3 = t_test.cell(r_idx, 0), t_test.cell(r_idx, 1), t_test.cell(r_idx, 2), t_test.cell(r_idx, 3)
        set_cell_margins(c0, top=50, bottom=50)
        set_cell_margins(c1, top=50, bottom=50)
        set_cell_margins(c2, top=50, bottom=50)
        set_cell_margins(c3, top=50, bottom=50)
        r0 = c0.paragraphs[0].add_run(tcid)
        r0.font.bold = True
        r0.font.size = Pt(9)
        c1.paragraphs[0].add_run(mod).font.size = Pt(9)
        c2.paragraphs[0].add_run(scen).font.size = Pt(8.5)
        c3.paragraphs[0].add_run(exp).font.size = Pt(8.5)

    doc.save(output_path)
    print(f"Generated Word DOCX successfully: {output_path}")

if __name__ == "__main__":
    build_docx(WORKSPACE_DOCX)
    build_docx(ARTIFACT_DOCX)
