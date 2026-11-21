import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

WORKSPACE_DOCX = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\PharmacyManagement_LLD.docx"
ARTIFACT_DOCX = r"C:\Users\chikoti lahari\.gemini\antigravity\brain\1b3064b5-dfd3-4cc3-896f-67b0eb16619c\PharmacyManagement_LLD.docx"
DIAGRAMS_DIR = r"c:\Users\chikoti lahari\OneDrive\Desktop\pharmacyManagement\docs\diagrams"

# Corporate Color Palette (Matching Template: Deep Navy & Clean Slate)
COLOR_PRIMARY_HEX = "004F7A"    # Deep Teal/Navy
COLOR_DARK_HEX = "1E293B"       # Slate body
COLOR_HEADER_BG = "F1F5F9"      # Table header background
COLOR_BORDER_HEX = "CBD5E1"     # Table border
COLOR_MUTED_HEX = "64748B"      # Subtext gray

COLOR_PRIMARY = RGBColor(0x00, 0x4F, 0x7A)
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
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="20" w:space="0" w:color="{COLOR_PRIMARY_HEX}"/>'
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
    run.font.size = Pt(9.5)
    run.font.color.rgb = COLOR_DARK

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(4)

def build_docx(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = docx.Document()

    # Page Margins: 0.8 inch
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # --------------------------------------------------------------------------
    # COVER PAGE
    # --------------------------------------------------------------------------
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(90)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("PHARMACY MANAGEMENT SYSTEM\n")
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(26)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_PRIMARY

    r_t2 = p_title.add_run("POC\nLow Level Design (LLD)")
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(18)
    r_t2.font.color.rgb = COLOR_PRIMARY

    p_mid = doc.add_paragraph()
    p_mid.paragraph_format.space_before = Pt(180)

    p_meta = doc.add_paragraph()
    r_m = p_meta.add_run("PharmacyManagement Microservices\nPOC – Low Level Design (LLD)\n\nDate: 19/11/2026\nCurrent Document Version: [1.0]\n\nAuthor: Lahari Chikoti")
    r_m.font.name = "Calibri"
    r_m.font.size = Pt(10.5)
    r_m.font.color.rgb = COLOR_DARK

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # DOCUMENT APPROVAL & CHANGE HISTORY
    # --------------------------------------------------------------------------
    p_app = doc.add_paragraph()
    r_app = p_app.add_run("DOCUMENT APPROVAL Approvers of this document")
    r_app.font.name = "Calibri"
    r_app.font.size = Pt(13)
    r_app.font.bold = True
    r_app.font.color.rgb = COLOR_PRIMARY

    tbl_app = doc.add_table(rows=3, cols=5)
    tbl_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_app)
    app_headers = ["Name", "Department", "Role", "Signature", "Date"]
    for i, h in enumerate(app_headers):
        cell = tbl_app.cell(0, i)
        set_cell_background(cell, COLOR_HEADER_BG)
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.bold = True

    app_data = [
        ["Lahari Chikoti", "Engineering", "Lead Developer", "L. Chikoti", "19/11/2026"],
        ["Technical Reviewer", "Architecture", "Solution Architect", "Approved", "19/11/2026"]
    ]
    for row_idx, r_data in enumerate(app_data, start=1):
        for col_idx, val in enumerate(r_data):
            cell = tbl_app.cell(row_idx, col_idx)
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_before = Pt(16)

    p_hist = doc.add_paragraph()
    r_hist = p_hist.add_run("Document Change History")
    r_hist.font.name = "Calibri"
    r_hist.font.size = Pt(13)
    r_hist.font.bold = True
    r_hist.font.color.rgb = COLOR_PRIMARY

    tbl_hist = doc.add_table(rows=2, cols=4)
    tbl_hist.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hist)
    hist_headers = ["Document Version #", "Author", "Date", "Description"]
    for i, h in enumerate(hist_headers):
        cell = tbl_hist.cell(0, i)
        set_cell_background(cell, COLOR_HEADER_BG)
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.bold = True

    hist_data = ["1.0", "Lahari Chikoti", "19/11/2026", "Pharmacy Management System LLD Initial Baseline"]
    for i, v in enumerate(hist_data):
        cell = tbl_hist.cell(1, i)
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        run = p.add_run(v)
        run.font.name = "Calibri"
        run.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_before = Pt(20)

    # --------------------------------------------------------------------------
    # TABLE OF CONTENTS
    # --------------------------------------------------------------------------
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_toc = p_toc.add_run("Table of Contents")
    r_toc.font.name = "Calibri"
    r_toc.font.size = Pt(16)
    r_toc.font.bold = True
    r_toc.font.color.rgb = COLOR_PRIMARY

    tbl_toc = doc.add_table(rows=20, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc)
    col_widths = [Inches(1.0), Inches(4.5), Inches(1.0)]

    for i, w in enumerate(col_widths):
        cell = tbl_toc.cell(0, i)
        cell.width = w
        set_cell_background(cell, COLOR_HEADER_BG)
        set_cell_margins(cell)

    tbl_toc.cell(0, 0).paragraphs[0].add_run("Section").font.bold = True
    tbl_toc.cell(0, 1).paragraphs[0].add_run("Title").font.bold = True
    tbl_toc.cell(0, 2).paragraphs[0].add_run("Page No.").font.bold = True

    toc_items = [
        ("1.0", "Document Purpose", "4"),
        ("2.0", "Intended Audience", "4"),
        ("3.0", "Project Background and Objectives", "5"),
        ("4.0", "Requirements", "5"),
        ("5.0", "Design Patterns", "7"),
        ("6.0", "Use Case Diagram", "8"),
        ("7.0", "Architecture Diagram", "9"),
        ("8.0", "Entity-Relationship Diagram", "10"),
        ("9.0", "Database Diagram", "11"),
        ("10.0", "Class Diagram", "12"),
        ("11.0", "Solution Steps", "13"),
        ("12.0", "Classes Names", "15"),
        ("13.0", "Validations", "18"),
        ("14.0", "API Catalogue", "18"),
        ("15.0", "HTTP Status Codes", "19"),
        ("16.0", "Integrations", "20"),
        ("17.0", "Sample API Requests", "20"),
        ("18.0", "Sample API Responses", "21"),
        ("19.0", "NUnit Unit Testing", "22")
    ]
    for idx, (sec_num, sec_title, p_num) in enumerate(toc_items, start=1):
        for col_i, w in enumerate(col_widths):
            tbl_toc.cell(idx, col_i).width = w
            set_cell_margins(tbl_toc.cell(idx, col_i), top=60, bottom=60)
        p0 = tbl_toc.cell(idx, 0).paragraphs[0]
        p0.add_run(sec_num).font.name = "Calibri"
        p1 = tbl_toc.cell(idx, 1).paragraphs[0]
        p1.add_run(sec_title).font.name = "Calibri"
        p2 = tbl_toc.cell(idx, 2).paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.add_run(p_num).font.name = "Calibri"

    doc.add_page_break()

    # Helper for adding standard section headings
    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title)
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = COLOR_DARK
        return p

    # --------------------------------------------------------------------------
    # 1.0 DOCUMENT PURPOSE
    # --------------------------------------------------------------------------
    add_section_header("1.0 Document Purpose")
    add_body_p(
        "This document describes the Low-Level Design (LLD) of the Pharmacy Management System. "
        "The system is built using C#, ASP.NET Core Web API, .NET 10, and a microservices architecture. "
        "It defines the service layout, database tables, business rules, validations, APIs, and unit testing approach."
    )
    add_body_p(
        "The application has five independent services: Auth Service, Inventory Service, Order Service, "
        "Payment Service, and SaleReport Service. Each service owns its private database. "
        "Services talk to each other through REST APIs, while the YARP API Gateway routes client requests. "
        "Swagger UI is used to test and document all endpoints."
    )

    # --------------------------------------------------------------------------
    # 2.0 INTENDED AUDIENCE
    # --------------------------------------------------------------------------
    add_section_header("2.0 Intended Audience")
    add_body_p("This document serves as a guide for project stakeholders:")

    tbl_aud = doc.add_table(rows=6, cols=2)
    tbl_aud.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_aud)
    tbl_aud.cell(0, 0).width = Inches(2.2)
    tbl_aud.cell(0, 1).width = Inches(4.3)
    set_cell_background(tbl_aud.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_aud.cell(0, 1), COLOR_HEADER_BG)
    tbl_aud.cell(0, 0).paragraphs[0].add_run("Role").font.bold = True
    tbl_aud.cell(0, 1).paragraphs[0].add_run("Engagement in Pharmacy Management Architecture").font.bold = True

    aud_data = [
        ("Product Owners / SMEs", "Confirm that the design covers all pharmacy requirements."),
        ("Business Analysts", "Map doctor and admin business workflows to technical APIs."),
        ("Enterprise Architects", "Review microservice boundaries, security rules, and database isolation."),
        ("Solution Architects", "Check the API contracts, service communications, and data flow."),
        ("Developers & QA Engineers", "Use this document to implement features and write unit tests.")
    ]
    for idx, (r_name, r_desc) in enumerate(aud_data, start=1):
        tbl_aud.cell(idx, 0).width = Inches(2.2)
        tbl_aud.cell(idx, 1).width = Inches(4.3)
        set_cell_margins(tbl_aud.cell(idx, 0))
        set_cell_margins(tbl_aud.cell(idx, 1))
        tbl_aud.cell(idx, 0).paragraphs[0].add_run(r_name).font.size = Pt(9.5)
        tbl_aud.cell(idx, 1).paragraphs[0].add_run(r_desc).font.size = Pt(9.5)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 3.0 PROJECT BACKGROUND AND OBJECTIVES
    # --------------------------------------------------------------------------
    add_section_header("3.0 Project Background and Objectives")
    
    p_b1 = doc.add_paragraph()
    p_b1.add_run("3.1 Project Background\n").font.bold = True
    p_b1.runs[0].font.size = Pt(11)
    p_b1.runs[0].font.color.rgb = COLOR_PRIMARY
    add_body_p(
        "Pharmacies need reliable software to manage medicine stocks, drug suppliers, doctor prescription orders, "
        "and sales accounting. Handling these records manually leads to misplaced orders, billing errors, or stock shortages.\n\n"
        "The Pharmacy Management System provides a clean backend solution. Doctors can check available medicines, "
        "add items to cart, and place orders. Admins can manage medicines, track supplier deliveries, verify orders, "
        "and view profit and sales reports."
    )

    p_b2 = doc.add_paragraph()
    p_b2.add_run("3.2 Project Objective\n").font.bold = True
    p_b2.runs[0].font.size = Pt(11)
    p_b2.runs[0].font.color.rgb = COLOR_PRIMARY
    add_body_p(
        "The objective is to develop a reliable and modular backend using C#, ASP.NET Core Web API, .NET 10, "
        "and microservices architecture. Key goals include:\n"
        "• Dividing operations into five services with separate SQL databases.\n"
        "• Securing endpoints using JWT Bearer authentication and role checks (Admin and Doctor).\n"
        "• Enabling doctors to browse medicines, place orders, and simulate payments.\n"
        "• Enabling admins to manage inventory, verify orders, and review sales analytics.\n"
        "• Documenting all endpoints in Swagger UI and validating logic with NUnit tests."
    )

    # --------------------------------------------------------------------------
    # 4.0 REQUIREMENTS
    # --------------------------------------------------------------------------
    add_section_header("4.0 Requirements")
    
    p_r1 = doc.add_paragraph()
    p_r1.add_run("4.1 Functional Requirements (FR)\n").font.bold = True
    p_r1.runs[0].font.size = Pt(11)
    p_r1.runs[0].font.color.rgb = COLOR_PRIMARY

    add_body_p("For Admin:")
    add_bullet("Login / Signup: Sign up and log in using name, email, contact number, and password.")
    add_bullet("View Drugs: Browse and view full details of all medicines in the pharmacy.")
    add_bullet("Manage Drugs: Add new drugs, edit drug details and prices, and delete drugs.")
    add_bullet("Manage Suppliers: View suppliers, add new suppliers, and update supplier information.")
    add_bullet("View Doctor Orders: Review orders placed by doctors and check their validity.")
    add_bullet("Verify Orders: Mark valid doctor orders as 'Verified'.")
    add_bullet("Order Handover: Move verified orders to the 'PickedUp' section once collected.")
    add_bullet("Sales Reports: View daily, weekly, monthly, and yearly sales summaries.")
    add_bullet("Download / Print: Export sales reports in CSV format for printing and bookkeeping.")
    add_bullet("Dashboard Analytics: Monitor low stock medicines, check expired drugs, analyze profit margins, and track top-selling medicines.")

    add_body_p("For Doctor User:")
    add_bullet("Login / Signup: Sign up and log in with name, email, contact number, and password.")
    add_bullet("View Drugs: Browse all available medicines with prices and current stock counts.")
    add_bullet("Buy Drugs & Cart: Add selected drugs to cart and create prescription orders.")
    add_bullet("Payment Simulation: Complete order payment checkout using simulated payment.")
    add_bullet("Track Order Status: Check order progress (Cart, Pending, Verified, PickedUp, or Cancelled).")
    add_bullet("Order History: View all previously placed orders and receipts.")

    p_r2 = doc.add_paragraph()
    p_r2.paragraph_format.space_before = Pt(8)
    p_r2.add_run("4.2 Non-Functional Requirements\n").font.bold = True
    p_r2.runs[0].font.size = Pt(11)
    p_r2.runs[0].font.color.rgb = COLOR_PRIMARY
    add_bullet("Microservices Architecture: 5 separate services with isolated databases.")
    add_bullet("Security: Protected APIs require valid JWT Bearer tokens with role claims.")
    add_bullet("REST APIs: Synchronous communication between services using typed HTTP clients.")
    add_bullet("Routing: YARP API Gateway acts as a single entry point for all client requests.")
    add_bullet("Validation & Error Handling: Clear validation messages and standard HTTP status codes.")
    add_bullet("Testing: Comprehensive NUnit unit tests and interactive testing via Swagger UI.")

    p_r3 = doc.add_paragraph()
    p_r3.paragraph_format.space_before = Pt(8)
    p_r3.add_run("4.3 Technology Stack\n").font.bold = True
    p_r3.runs[0].font.size = Pt(11)
    p_r3.runs[0].font.color.rgb = COLOR_PRIMARY

    tbl_tech = doc.add_table(rows=11, cols=3)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tech)
    tbl_tech.cell(0, 0).width = Inches(1.8)
    tbl_tech.cell(0, 1).width = Inches(2.2)
    tbl_tech.cell(0, 2).width = Inches(2.5)
    set_cell_background(tbl_tech.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_tech.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_tech.cell(0, 2), COLOR_HEADER_BG)
    tbl_tech.cell(0, 0).paragraphs[0].add_run("Category").font.bold = True
    tbl_tech.cell(0, 1).paragraphs[0].add_run("Technology").font.bold = True
    tbl_tech.cell(0, 2).paragraphs[0].add_run("Purpose").font.bold = True

    tech_data = [
        ("Language", "C# 12", "Primary programming language for all services."),
        ("Framework", "ASP.NET Core Web API", "Framework used to build RESTful microservice APIs."),
        ("Runtime", ".NET 10", "Cross-platform runtime to build and run the services."),
        ("ORM", "Entity Framework Core 8", "Maps C# models to SQL tables using Code-First approach."),
        ("Database", "Microsoft SQL Server 2022", "Hosts 5 separate databases for microservice data isolation."),
        ("Security", "JWT Bearer & PBKDF2", "Authenticates users and hashes passwords securely."),
        ("Authorization", "Role-Based Access (RBAC)", "Restricts API access based on Admin and Doctor roles."),
        ("API Gateway", "YARP", "Routes incoming requests to the appropriate microservices."),
        ("API Documentation", "Swagger / OpenAPI 3.0", "Documents and interactively tests backend APIs."),
        ("Testing", "NUnit & Moq", "Automated unit test suite verifying service layer business logic.")
    ]
    for idx, (c1, c2, c3) in enumerate(tech_data, start=1):
        tbl_tech.cell(idx, 0).width = Inches(1.8)
        tbl_tech.cell(idx, 1).width = Inches(2.2)
        tbl_tech.cell(idx, 2).width = Inches(2.5)
        set_cell_margins(tbl_tech.cell(idx, 0))
        set_cell_margins(tbl_tech.cell(idx, 1))
        set_cell_margins(tbl_tech.cell(idx, 2))
        tbl_tech.cell(idx, 0).paragraphs[0].add_run(c1).font.size = Pt(9.5)
        tbl_tech.cell(idx, 1).paragraphs[0].add_run(c2).font.size = Pt(9.5)
        tbl_tech.cell(idx, 2).paragraphs[0].add_run(c3).font.size = Pt(9.5)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 5.0 DESIGN PATTERNS
    # --------------------------------------------------------------------------
    add_section_header("5.0 Design Patterns")
    add_body_p("The architecture uses standard enterprise design patterns to maintain clean separation of concerns:")

    tbl_pat = doc.add_table(rows=9, cols=2)
    tbl_pat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pat)
    tbl_pat.cell(0, 0).width = Inches(2.2)
    tbl_pat.cell(0, 1).width = Inches(4.3)
    set_cell_background(tbl_pat.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_pat.cell(0, 1), COLOR_HEADER_BG)
    tbl_pat.cell(0, 0).paragraphs[0].add_run("Name").font.bold = True
    tbl_pat.cell(0, 1).paragraphs[0].add_run("Description").font.bold = True

    pat_data = [
        ("REST API", "HTTP-based REST APIs are used for client calls and service-to-service communication."),
        ("Microservices Architecture", "The system is divided into five independent services: Auth, Inventory, Order, Payment, and SaleReport."),
        ("Layered Architecture", "Each microservice follows a Controller, Service, and Repository structure to separate concerns."),
        ("Repository Pattern", "Repositories handle database access, keeping data logic separate from business rules."),
        ("Dependency Injection", "Services and repositories are injected via built-in DI containers for testability."),
        ("Database per Service", "Each microservice owns its private database. No direct cross-service SQL joins are allowed."),
        ("API Gateway Pattern", "YARP provides a centralized entry point and routes client requests to microservices."),
        ("DTO Pattern", "Request and response DTOs define clean API contracts and prevent over-posting.")
    ]
    for idx, (p_name, p_desc) in enumerate(pat_data, start=1):
        tbl_pat.cell(idx, 0).width = Inches(2.2)
        tbl_pat.cell(idx, 1).width = Inches(4.3)
        set_cell_margins(tbl_pat.cell(idx, 0))
        set_cell_margins(tbl_pat.cell(idx, 1))
        tbl_pat.cell(idx, 0).paragraphs[0].add_run(p_name).font.size = Pt(9.5)
        tbl_pat.cell(idx, 1).paragraphs[0].add_run(p_desc).font.size = Pt(9.5)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 6.0 USE CASE DIAGRAM
    # --------------------------------------------------------------------------
    add_section_header("6.0 Use Case Diagram")
    usecase_img = os.path.join(DIAGRAMS_DIR, "02_Use_Case_Diagram.jpg")
    if os.path.exists(usecase_img):
        doc.add_picture(usecase_img, width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 6.0 – Use Case Diagram")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    p_d6 = doc.add_paragraph()
    p_d6.add_run("Description").font.bold = True
    add_body_p(
        "The use case diagram outlines the core operational workflows and interactions between the primary user roles and the Pharmacy Management System. The system supports two distinct actors, namely Doctor and Admin, each equipped with role-specific privileges alongside shared capabilities for account registration and secure login. Doctors utilize the system to search the live pharmaceutical catalog, examine detailed medication formulations, stage required items into an active digital shopping cart, and submit verified prescription orders. The checkout flow incorporates simulated payment verification across multiple instruments, followed by real-time order status tracking from submission to fulfillment. On the administrative side, pharmacy managers maintain total catalog governance by adding, updating, and removing medicines, evaluating stock levels through low-stock alerts, and monitoring upcoming expiration dates. Administrators also oversee vendor profiles, inspect incoming doctor prescriptions, verify order validity, transition fulfilled items into the picked-up section, review consolidated sales analytics, and generate downloadable or printable financial summaries."
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 7.0 ARCHITECTURE DIAGRAM
    # --------------------------------------------------------------------------
    add_section_header("7.0 Architecture Diagram")
    arch_img = os.path.join(DIAGRAMS_DIR, "01_Solution_Architecture_Diagram.jpg")
    if os.path.exists(arch_img):
        doc.add_picture(arch_img, width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 7.0 – Solution Architecture Diagram")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    p_d7 = doc.add_paragraph()
    p_d7.add_run("Description").font.bold = True
    add_body_p(
        "The solution architecture diagram illustrates the enterprise multi-tier structure of the Pharmacy Management System, detailing the separation of concerns across presentation, routing, application, and persistence tiers. Client interactions originate at the presentation layer via responsive web interfaces and interactive Swagger UI documentation endpoints. Client requests pass through the YARP API Gateway layer, which acts as a centralized reverse proxy and security gatekeeper responsible for enforcing JWT bearer authentication and distributing incoming traffic. The application tier comprises five independent, loosely coupled microservices: Auth Service for identity and credentials management, Inventory Service for drug catalog and supplier stock operations, Order Service for prescription handling and cart management, Payment Service for 1:1 transaction simulations, and SaleReport Service for sales intelligence and profit computation. At the data layer, each microservice connects strictly to its own dedicated SQL Server database, guaranteeing complete data isolation, fault tolerance, and independent scalability."
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 8.0 ENTITY-RELATIONSHIP DIAGRAM
    # --------------------------------------------------------------------------
    add_section_header("8.0 Entity-Relationship Diagram")
    er_img = os.path.join(DIAGRAMS_DIR, "05_ER_Diagram.jpg")
    if os.path.exists(er_img):
        doc.add_picture(er_img, width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 8.0 – Entity-Relationship Diagram (Database-Per-Service Boxes)")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    p_d8 = doc.add_paragraph()
    p_d8.add_run("Description").font.bold = True
    add_body_p(
        "The entity-relationship diagram depicts the data models, primary keys, foreign keys, and structural associations organized within distinct database perimeters for each microservice. User DB encapsulates the User entity which records login credentials, contact numbers, and security roles. Inventory DB maintains Supplier, Drugs, and Inventory entities, where each registered supplier supplies multiple inventory shipments in a one-to-many relationship, and each drug is replenished across multiple inventory batches. Order DB encompasses Order and OrderItem entities, structuring each doctor prescription into a parent order containing one or more ordered medicine items. Payment DB isolates the Payment entity, enforcing a strict one-to-one unique constraint with the parent order to ensure every order is fulfilled by exactly one financial transaction. SaleReport DB operates as an analytical store holding pre-computed sales summaries without direct database-level dependencies. Relationships across microservices remain logical and are verified via REST APIs, while relational integrity is maintained internally within each isolated database."
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 9.0 DATABASE DIAGRAM
    # --------------------------------------------------------------------------
    add_section_header("9.0 Database Diagram")
    db_img = os.path.join(DIAGRAMS_DIR, "06_Database_Schema_Diagram.jpg")
    if os.path.exists(db_img):
        doc.add_picture(db_img, width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 9.0 – Database Schema Diagram")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    p_d9 = doc.add_paragraph()
    p_d9.add_run("Description").font.bold = True
    add_body_p(
        "The database diagram defines the physical schema definitions, column data types, nullability rules, and primary and foreign key constraints across the five relational databases. The Users table in Pharmacy_UserDB enforces unique constraints on email addresses while storing hashed passwords and role flags. Within Pharmacy_InventoryDB, the Drugs table tracks trade names, descriptions, therapeutic categories, selling prices, current stock levels, and minimum stock threshold limits used to trigger automated low-stock warnings. The Suppliers table holds vendor contact data, and the Inventory table records incoming wholesale shipments, purchase prices, supply dates, and batch references. Pharmacy_OrderDB contains the Orders and OrderItems tables, recording prescription dates, status values from Cart to PickedUp, and itemized quantities and unit prices. Pharmacy_PaymentDB enforces a unique index on the OrderId column of the Payments table, preventing duplicate payments for any order. Finally, Pharmacy_SaleReportDB stores periodic financial metrics including total order volume, gross revenues, and calculated net profits for official reporting."
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 10.0 CLASS DIAGRAM
    # --------------------------------------------------------------------------
    add_section_header("10.0 Class Diagram")
    cls_img = os.path.join(DIAGRAMS_DIR, "03_Class_Diagram.jpg")
    if os.path.exists(cls_img):
        doc.add_picture(cls_img, width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 10.0 – Domain Class Diagram")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    p_d10 = doc.add_paragraph()
    p_d10.add_run("Description").font.bold = True
    add_body_p(
        "The class diagram details the object-oriented structure of domain models, highlighting their private attributes, public properties, and core business operations across the system. The User class encapsulates authentication state, password hashing logic, and role definitions while providing sign-up and login capabilities. The Drug class encapsulates pharmaceutical catalog attributes, unit selling prices, and stock decrement logic, collaborating with the Supplier class which manages distributor contacts and wholesale replenishment. The Order and OrderItem classes govern prescription management, line item calculations, order validation, and status transitions from Cart through Verified to PickedUp. The Payment class manages transaction attributes, payment simulation methods, and one-to-one order binding. The SaleReport class encapsulates financial aggregation routines, calculating gross turnover, cost of goods, and net profit margins across custom date ranges. Interactions between classes reflect concrete business workflows, such as users placing orders, orders containing order items, suppliers restocking drugs, and payments completing orders."
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 11.0 SOLUTION STEPS
    # --------------------------------------------------------------------------
    add_section_header("11.0 Solution Steps")

    steps_data = [
        ("11.1 User Registration and Login",
         "The user initiates registration by providing basic account details including full name, contact phone number, email address, password, and assigned role as an Admin or Doctor. The Auth Service validates the submitted inputs and cryptographically hashes the plain-text password using PBKDF2 with a unique cryptographic salt before storing the user record in User DB. During login, the user provides their registered email and password credentials. The Auth Service verifies the password against the stored hash and generates a signed JSON Web Token (JWT) containing user identity, role, and expiration claims. The client application attaches this token to the Authorization header of all subsequent API requests to securely access protected endpoints."),

        ("11.2 Admin Manages Drugs and Suppliers",
         "The administrator authenticates into the system and provides the JWT token to manage pharmacy inventory resources. Operating through the Inventory Service, the administrator performs full lifecycle management of pharmaceuticals by adding new drug profiles, modifying pricing or descriptions, and retiring obsolete items. Critical attributes such as therapeutic category, selling price, expiry date, and minimum stock threshold limits are established to automate inventory health monitoring. To replenish stock, the administrator registers verified wholesale suppliers and enters incoming shipments into the Inventory table with purchase prices, supplied quantities, and batch tracking numbers. The Inventory Service updates stock levels in real time and persists all changes to Inventory DB."),

        ("11.3 Doctor Searches Drugs and Adds to Cart",
         "The doctor logs into the clinical portal and explores the live pharmaceutical catalog through keyword searches and category filters. The Inventory Service inspects current inventory and returns only active, non-expired medications with positive stock balances. The doctor reviews clinical descriptions, unit pricing, and stock availability before selecting desired medications and specifying quantities. The doctor then adds the selected items to an active shopping cart. The Order Service creates or updates a staged Cart order record in Order DB, computing line item totals and the overall balance while preserving available physical inventory until checkout confirmation."),

        ("11.4 Doctor Places Order and Simulates Payment",
         "When the doctor confirms the shopping cart, the Order Service transitions the order into an active 'Pending' status. The Order Service sends an inter-service stock deduction request to the Inventory Service, which validates item availability and deducts the requested quantities from on-hand inventory. The doctor is then presented with the payment simulation interface to select a preferred payment method such as Credit Card, Debit Card, UPI, Net Banking, or Cash. The Payment Service simulates payment gateway processing, creates a dedicated payment record with a unique OrderId constraint in Payment DB, assigns an authentic transaction reference, and updates the payment status to 'Completed'."),

        ("11.5 Admin Verifies Order and Marks PickedUp",
         "The administrator accesses the order management dashboard to monitor incoming prescription orders submitted across the hospital network. The administrator runs an automated order validation check to verify item counts, positive order amounts, and doctor credentials. Upon successful validation, the administrator verifies the order, transitioning its status to 'Verified' so dispensary personnel can prepare the medications for collection. When the doctor or authorized representative arrives at the dispensary counter, the administrator confirms physical handover and updates the order status to 'PickedUp', archiving the completed order inside the picked-up orders section."),

        ("11.6 Admin Generates and Downloads Sales Reports",
         "The administrator navigates to the sales analytics portal and selects a reporting timeframe such as Daily, Weekly, Monthly, or Yearly intervals. The SaleReport Service aggregates completed and picked-up prescription orders, computes total sales turnover, and calculates net profits by deducting corresponding wholesale purchase costs from selling prices. The generated financial summary is persisted in SaleReport DB and displayed on executive analytics dashboards, highlighting total order volume, overall revenue, net margins, and top-selling medications. The administrator can also export the official report as a CSV spreadsheet or produce a formatted printable receipt for auditing.")
    ]

    for s_title, s_para in steps_data:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        r = p.add_run(s_title)
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = COLOR_PRIMARY
        add_body_p(s_para)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 12.0 CLASSES NAMES
    # --------------------------------------------------------------------------
    add_section_header("12.0 Classes Names")

    # Table 1: Entities (Models)
    p_t1 = doc.add_paragraph()
    p_t1.add_run("Entities (Models)\n").font.bold = True
    p_t1.runs[0].font.size = Pt(11)

    tbl_e = doc.add_table(rows=9, cols=3)
    tbl_e.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_e)
    tbl_e.cell(0, 0).width = Inches(0.6)
    tbl_e.cell(0, 1).width = Inches(2.2)
    tbl_e.cell(0, 2).width = Inches(3.7)
    set_cell_background(tbl_e.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_e.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_e.cell(0, 2), COLOR_HEADER_BG)
    tbl_e.cell(0, 0).paragraphs[0].add_run("S.No").font.bold = True
    tbl_e.cell(0, 1).paragraphs[0].add_run("Class Name").font.bold = True
    tbl_e.cell(0, 2).paragraphs[0].add_run("Description").font.bold = True

    e_data = [
        ("1", "User.cs", "Represents user account information, password hash, and assigned role (Admin or Doctor)."),
        ("2", "Drug.cs", "Represents medicine details, description, selling price, expiry date, quantity, and minimum stock limit."),
        ("3", "Supplier.cs", "Represents supplier contact information, email, phone number, and address."),
        ("4", "Inventory.cs", "Represents incoming stock shipments, purchase prices, supply dates, and supplier links."),
        ("5", "Order.cs", "Represents prescription orders placed by doctors, order date, total amount, and status."),
        ("6", "OrderItem.cs", "Represents individual medicine line items belonging to an order with unit price."),
        ("7", "Payment.cs", "Represents simulated payment records with 1:1 order linking and transaction references."),
        ("8", "SaleReport.cs", "Represents financial sales reports, total order counts, revenue, and profit calculations.")
    ]
    for idx, (c1, c2, c3) in enumerate(e_data, start=1):
        tbl_e.cell(idx, 0).width = Inches(0.6)
        tbl_e.cell(idx, 1).width = Inches(2.2)
        tbl_e.cell(idx, 2).width = Inches(3.7)
        set_cell_margins(tbl_e.cell(idx, 0))
        set_cell_margins(tbl_e.cell(idx, 1))
        set_cell_margins(tbl_e.cell(idx, 2))
        tbl_e.cell(idx, 0).paragraphs[0].add_run(c1).font.size = Pt(9.5)
        tbl_e.cell(idx, 1).paragraphs[0].add_run(c2).font.size = Pt(9.5)
        tbl_e.cell(idx, 2).paragraphs[0].add_run(c3).font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_before = Pt(8)

    # Table 2: Controllers (API Layer)
    p_t2 = doc.add_paragraph()
    p_t2.add_run("Controllers (API Layer)\n").font.bold = True
    p_t2.runs[0].font.size = Pt(11)

    tbl_c = doc.add_table(rows=8, cols=3)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_c)
    tbl_c.cell(0, 0).width = Inches(0.6)
    tbl_c.cell(0, 1).width = Inches(2.2)
    tbl_c.cell(0, 2).width = Inches(3.7)
    set_cell_background(tbl_c.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_c.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_c.cell(0, 2), COLOR_HEADER_BG)
    tbl_c.cell(0, 0).paragraphs[0].add_run("S.No").font.bold = True
    tbl_c.cell(0, 1).paragraphs[0].add_run("Class Name").font.bold = True
    tbl_c.cell(0, 2).paragraphs[0].add_run("Description").font.bold = True

    c_data = [
        ("1", "AuthController.cs", "Handles user registration, login, and profile retrieval APIs."),
        ("2", "DrugsController.cs", "Handles drug catalog search, drug creation, updates, and low-stock alerts."),
        ("3", "SuppliersController.cs", "Handles supplier registration, retrieval, and profile updates."),
        ("4", "InventoryController.cs", "Handles stock inward shipments, batch updates, and stock deduction."),
        ("5", "OrdersController.cs", "Handles order creation, status tracking, admin verification, and pickup handover."),
        ("6", "PaymentsController.cs", "Handles checkout payment simulation and transaction verification."),
        ("7", "SaleReportsController.cs", "Handles sales report generation, profit analytics, and CSV download APIs.")
    ]
    for idx, (c1, c2, c3) in enumerate(c_data, start=1):
        tbl_c.cell(idx, 0).width = Inches(0.6)
        tbl_c.cell(idx, 1).width = Inches(2.2)
        tbl_c.cell(idx, 2).width = Inches(3.7)
        set_cell_margins(tbl_c.cell(idx, 0))
        set_cell_margins(tbl_c.cell(idx, 1))
        set_cell_margins(tbl_c.cell(idx, 2))
        tbl_c.cell(idx, 0).paragraphs[0].add_run(c1).font.size = Pt(9.5)
        tbl_c.cell(idx, 1).paragraphs[0].add_run(c2).font.size = Pt(9.5)
        tbl_c.cell(idx, 2).paragraphs[0].add_run(c3).font.size = Pt(9.5)

    doc.add_page_break()

    # Table 3: Services (Business Logic)
    p_t3 = doc.add_paragraph()
    p_t3.add_run("Services (Business Logic)\n").font.bold = True
    p_t3.runs[0].font.size = Pt(11)

    tbl_s = doc.add_table(rows=8, cols=3)
    tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_s)
    tbl_s.cell(0, 0).width = Inches(0.6)
    tbl_s.cell(0, 1).width = Inches(2.2)
    tbl_s.cell(0, 2).width = Inches(3.7)
    set_cell_background(tbl_s.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_s.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_s.cell(0, 2), COLOR_HEADER_BG)
    tbl_s.cell(0, 0).paragraphs[0].add_run("S.No").font.bold = True
    tbl_s.cell(0, 1).paragraphs[0].add_run("Class Name").font.bold = True
    tbl_s.cell(0, 2).paragraphs[0].add_run("Description").font.bold = True

    s_data = [
        ("1", "AuthService.cs", "Implements user registration, password verification, and login logic."),
        ("2", "TokenService.cs", "Generates signed JWT tokens with user claims and expiration."),
        ("3", "DrugService.cs", "Handles medicine availability checks, stock updates, and low-stock alerts."),
        ("4", "SupplierService.cs", "Manages supplier records, contact updates, and vendor associations."),
        ("5", "OrderService.cs", "Coordinates order creation, stock reservation, verification, and handover."),
        ("6", "PaymentService.cs", "Simulates payment processing and enforces 1:1 transaction rules."),
        ("7", "SaleReportService.cs", "Computes revenue, purchase costs, profit, and builds CSV report files.")
    ]
    for idx, (c1, c2, c3) in enumerate(s_data, start=1):
        tbl_s.cell(idx, 0).width = Inches(0.6)
        tbl_s.cell(idx, 1).width = Inches(2.2)
        tbl_s.cell(idx, 2).width = Inches(3.7)
        set_cell_margins(tbl_s.cell(idx, 0))
        set_cell_margins(tbl_s.cell(idx, 1))
        set_cell_margins(tbl_s.cell(idx, 2))
        tbl_s.cell(idx, 0).paragraphs[0].add_run(c1).font.size = Pt(9.5)
        tbl_s.cell(idx, 1).paragraphs[0].add_run(c2).font.size = Pt(9.5)
        tbl_s.cell(idx, 2).paragraphs[0].add_run(c3).font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_before = Pt(8)

    # Table 4: Repositories (Data Access Layer)
    p_t4 = doc.add_paragraph()
    p_t4.add_run("Repositories (Data Access Layer)\n").font.bold = True
    p_t4.runs[0].font.size = Pt(11)

    tbl_r = doc.add_table(rows=8, cols=3)
    tbl_r.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_r)
    tbl_r.cell(0, 0).width = Inches(0.6)
    tbl_r.cell(0, 1).width = Inches(2.2)
    tbl_r.cell(0, 2).width = Inches(3.7)
    set_cell_background(tbl_r.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_r.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_r.cell(0, 2), COLOR_HEADER_BG)
    tbl_r.cell(0, 0).paragraphs[0].add_run("S.No").font.bold = True
    tbl_r.cell(0, 1).paragraphs[0].add_run("Class Name").font.bold = True
    tbl_r.cell(0, 2).paragraphs[0].add_run("Description").font.bold = True

    r_data = [
        ("1", "UserRepository.cs", "Manages database operations for user accounts in User DB."),
        ("2", "DrugRepository.cs", "Handles CRUD database queries for medicines in Inventory DB."),
        ("3", "SupplierRepository.cs", "Manages database queries for supplier records in Inventory DB."),
        ("4", "InventoryRepository.cs", "Manages stock inward entries and batch history in Inventory DB."),
        ("5", "OrderRepository.cs", "Handles order and order item queries with EF Core in Order DB."),
        ("6", "PaymentRepository.cs", "Saves and queries payment records with unique order IDs in Payment DB."),
        ("7", "SaleReportRepository.cs", "Stores and queries sales summary records in SaleReport DB.")
    ]
    for idx, (c1, c2, c3) in enumerate(r_data, start=1):
        tbl_r.cell(idx, 0).width = Inches(0.6)
        tbl_r.cell(idx, 1).width = Inches(2.2)
        tbl_r.cell(idx, 2).width = Inches(3.7)
        set_cell_margins(tbl_r.cell(idx, 0))
        set_cell_margins(tbl_r.cell(idx, 1))
        set_cell_margins(tbl_r.cell(idx, 2))
        tbl_r.cell(idx, 0).paragraphs[0].add_run(c1).font.size = Pt(9.5)
        tbl_r.cell(idx, 1).paragraphs[0].add_run(c2).font.size = Pt(9.5)
        tbl_r.cell(idx, 2).paragraphs[0].add_run(c3).font.size = Pt(9.5)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 14.0 VALIDATIONS
    # --------------------------------------------------------------------------
    add_section_header("13.0 Validations")
    add_bullet("User Input Validations: Ensure required fields (name, valid email format, contact phone number, password length) are provided.")
    add_bullet("Role Authorization: Ensure only Admin can add/edit drugs, manage suppliers, verify orders, and view sales reports.")
    add_bullet("Doctor Isolation: Ensure Doctors can only view and manage their own orders.")
    add_bullet("Stock Availability: Verify that requested medicine quantities do not exceed available stock before creating an order.")
    add_bullet("Low Stock Trigger: Automatically identify medicines whose stock is at or below MinimumStockQuantity.")
    add_bullet("Expiry Validation: Prevent selling medicines that have passed their expiration date.")
    add_bullet("Order Status Flow: Orders progress through Cart -> Pending -> Verified -> PickedUp (or Cancelled).")
    add_bullet("1:1 Payment Rule: Exactly one payment is allowed per order. Duplicate payments for the same order are rejected.")
    add_bullet("Token Security: Every protected API validates JWT signature, issuer, expiration, and role claims.")

    # --------------------------------------------------------------------------
    # 15.0 API CATALOGUE (NO PORT NUMBERS!)
    # --------------------------------------------------------------------------
    add_section_header("14.0 API Catalogue")
    add_body_p("The table below lists all endpoints exposed by the microservices (routed through YARP API Gateway):")

    tbl_api = doc.add_table(rows=22, cols=4)
    tbl_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_api)
    tbl_api.cell(0, 0).width = Inches(1.3)
    tbl_api.cell(0, 1).width = Inches(2.7)
    tbl_api.cell(0, 2).width = Inches(0.9)
    tbl_api.cell(0, 3).width = Inches(1.6)
    set_cell_background(tbl_api.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_api.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_api.cell(0, 2), COLOR_HEADER_BG)
    set_cell_background(tbl_api.cell(0, 3), COLOR_HEADER_BG)
    tbl_api.cell(0, 0).paragraphs[0].add_run("Module").font.bold = True
    tbl_api.cell(0, 1).paragraphs[0].add_run("Endpoint").font.bold = True
    tbl_api.cell(0, 2).paragraphs[0].add_run("Method").font.bold = True
    tbl_api.cell(0, 3).paragraphs[0].add_run("Access").font.bold = True

    api_data = [
        ("Auth", "/api/auth/register", "POST", "Public"),
        ("Auth", "/api/auth/login", "POST", "Public"),
        ("Auth", "/api/auth/me", "GET", "Admin / Doctor"),
        ("Inventory", "/api/drugs", "GET", "Admin / Doctor"),
        ("Inventory", "/api/drugs/{id}", "GET", "Admin / Doctor"),
        ("Inventory", "/api/drugs", "POST", "Admin"),
        ("Inventory", "/api/drugs/{id}", "PUT", "Admin"),
        ("Inventory", "/api/drugs/{id}", "DELETE", "Admin"),
        ("Inventory", "/api/drugs/low-stock", "GET", "Admin"),
        ("Inventory", "/api/suppliers", "GET", "Admin"),
        ("Inventory", "/api/suppliers", "POST", "Admin"),
        ("Inventory", "/api/inventory/inward", "POST", "Admin"),
        ("Order", "/api/orders", "POST", "Doctor"),
        ("Order", "/api/orders", "GET", "Admin"),
        ("Order", "/api/orders/my-orders", "GET", "Doctor"),
        ("Order", "/api/orders/{id}", "GET", "Admin / Doctor"),
        ("Order", "/api/orders/{id}/verify", "PUT", "Admin"),
        ("Order", "/api/orders/{id}/pickup", "PUT", "Admin"),
        ("Order", "/api/orders/{id}/cancel", "PUT", "Doctor / Admin"),
        ("Payment", "/api/payments/simulate", "POST", "Doctor / Internal"),
        ("SaleReport", "/api/salereports/generate", "POST", "Admin")
    ]
    for idx, (m, ep, meth, acc) in enumerate(api_data, start=1):
        tbl_api.cell(idx, 0).width = Inches(1.3)
        tbl_api.cell(idx, 1).width = Inches(2.7)
        tbl_api.cell(idx, 2).width = Inches(0.9)
        tbl_api.cell(idx, 3).width = Inches(1.6)
        set_cell_margins(tbl_api.cell(idx, 0), top=50, bottom=50)
        set_cell_margins(tbl_api.cell(idx, 1), top=50, bottom=50)
        set_cell_margins(tbl_api.cell(idx, 2), top=50, bottom=50)
        set_cell_margins(tbl_api.cell(idx, 3), top=50, bottom=50)
        tbl_api.cell(idx, 0).paragraphs[0].add_run(m).font.size = Pt(9)
        tbl_api.cell(idx, 1).paragraphs[0].add_run(ep).font.size = Pt(8.5)
        tbl_api.cell(idx, 2).paragraphs[0].add_run(meth).font.size = Pt(9)
        tbl_api.cell(idx, 3).paragraphs[0].add_run(acc).font.size = Pt(9)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 16.0 HTTP STATUS CODES
    # --------------------------------------------------------------------------
    add_section_header("15.0 HTTP Status Codes")

    tbl_stat = doc.add_table(rows=10, cols=3)
    tbl_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_stat)
    tbl_stat.cell(0, 0).width = Inches(1.1)
    tbl_stat.cell(0, 1).width = Inches(1.5)
    tbl_stat.cell(0, 2).width = Inches(3.9)
    set_cell_background(tbl_stat.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_stat.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_stat.cell(0, 2), COLOR_HEADER_BG)
    tbl_stat.cell(0, 0).paragraphs[0].add_run("Status Code").font.bold = True
    tbl_stat.cell(0, 1).paragraphs[0].add_run("Status").font.bold = True
    tbl_stat.cell(0, 2).paragraphs[0].add_run("Description").font.bold = True

    stat_data = [
        ("200", "OK", "The request succeeded and returned the requested data."),
        ("201", "Created", "A new user, drug, order, payment, or report was created successfully."),
        ("204", "No Content", "The request succeeded and no response body is needed (e.g. deletion)."),
        ("400", "Bad Request", "The request is invalid, missing data, or failed validation checks."),
        ("401", "Unauthorized", "The JWT token is missing, expired, or invalid."),
        ("403", "Forbidden", "The user does not have permission for this action (e.g. Doctor calling Admin API)."),
        ("404", "Not Found", "The requested drug, order, supplier, or user record was not found."),
        ("409", "Conflict", "A conflict occurred, such as duplicate email or duplicate payment for an order."),
        ("500", "Internal Server Error", "An unexpected error occurred while processing the request.")
    ]
    for idx, (c1, c2, c3) in enumerate(stat_data, start=1):
        tbl_stat.cell(idx, 0).width = Inches(1.1)
        tbl_stat.cell(idx, 1).width = Inches(1.5)
        tbl_stat.cell(idx, 2).width = Inches(3.9)
        set_cell_margins(tbl_stat.cell(idx, 0))
        set_cell_margins(tbl_stat.cell(idx, 1))
        set_cell_margins(tbl_stat.cell(idx, 2))
        tbl_stat.cell(idx, 0).paragraphs[0].add_run(c1).font.size = Pt(9.5)
        tbl_stat.cell(idx, 1).paragraphs[0].add_run(c2).font.size = Pt(9.5)
        tbl_stat.cell(idx, 2).paragraphs[0].add_run(c3).font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_before = Pt(8)

    # --------------------------------------------------------------------------
    # 17.0 INTEGRATIONS
    # --------------------------------------------------------------------------
    add_section_header("16.0 Integrations")
    add_bullet("YARP API Gateway: Provides a central entry point and routes client requests to the appropriate microservice.")
    add_bullet("REST APIs: Enable synchronous communication between Order, Inventory, and Payment services using typed HTTP clients.")
    add_bullet("JWT Bearer Authentication: Secures APIs with signed tokens and supports role-based access for Admin and Doctor.")
    add_bullet("SQL Server 2022: Maintains five separate databases ensuring data isolation per service.")
    add_bullet("Entity Framework Core 8: Manages database access, Code-First mappings, and schema updates.")
    add_bullet("Swagger UI & OpenAPI: Provide interactive API documentation and testing for all microservices.")
    add_bullet("NUnit & Moq: Automated unit test suite verifying service layer logic using mocked dependencies.")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 18.0 SAMPLE API REQUESTS
    # --------------------------------------------------------------------------
    add_section_header("17.0 Sample API Requests")
    add_body_p("Sample POST request to create an order (/api/orders):")

    order_req_json = (
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
    add_callout_box(doc, order_req_json, "Order Creation Request Payload")

    # --------------------------------------------------------------------------
    # 19.0 SAMPLE API RESPONSES
    # --------------------------------------------------------------------------
    add_section_header("18.0 Sample API Responses")
    add_body_p("Successful response returned after order creation:")

    order_res_json = (
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
    add_callout_box(doc, order_res_json, "Status Code: 201 Created")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 20.0 NUNIT UNIT TESTING
    # --------------------------------------------------------------------------
    add_section_header("19.0 NUnit Unit Testing")
    add_body_p("The unit testing suite validates key business logic and error scenarios using NUnit and Moq:")

    tbl_test = doc.add_table(rows=21, cols=4)
    tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_test)
    tbl_test.cell(0, 0).width = Inches(0.8)
    tbl_test.cell(0, 1).width = Inches(1.2)
    tbl_test.cell(0, 2).width = Inches(2.2)
    tbl_test.cell(0, 3).width = Inches(2.3)
    set_cell_background(tbl_test.cell(0, 0), COLOR_HEADER_BG)
    set_cell_background(tbl_test.cell(0, 1), COLOR_HEADER_BG)
    set_cell_background(tbl_test.cell(0, 2), COLOR_HEADER_BG)
    set_cell_background(tbl_test.cell(0, 3), COLOR_HEADER_BG)
    tbl_test.cell(0, 0).paragraphs[0].add_run("Test Case ID").font.bold = True
    tbl_test.cell(0, 1).paragraphs[0].add_run("Module").font.bold = True
    tbl_test.cell(0, 2).paragraphs[0].add_run("Test Scenario").font.bold = True
    tbl_test.cell(0, 3).paragraphs[0].add_run("Expected Result").font.bold = True

    test_cases = [
        ("TC-01", "Auth", "Register user with valid details.", "User is created with hashed password and role."),
        ("TC-02", "Auth", "Register with duplicate email.", "Registration fails with a duplicate email error."),
        ("TC-03", "Auth", "Login with valid credentials.", "Login succeeds and returns a signed JWT token."),
        ("TC-04", "Auth", "Login with incorrect password.", "Login fails with 401 Unauthorized."),
        ("TC-05", "Inventory", "Add medicine with valid details.", "Medicine is saved with price and stock count."),
        ("TC-06", "Inventory", "Add medicine with negative price.", "Validation fails with 400 Bad Request."),
        ("TC-07", "Inventory", "Update medicine price and stock.", "Medicine record is updated successfully in SQL."),
        ("TC-08", "Inventory", "Query medicines below min stock.", "Returns medicines where quantity <= min stock level."),
        ("TC-09", "Inventory", "Deduct stock when sufficient.", "Medicine stock is reduced by the requested quantity."),
        ("TC-10", "Inventory", "Deduct stock when insufficient.", "Throws exception and stock remains unchanged."),
        ("TC-11", "Order", "Create order with valid items.", "Order is created in Pending status with total amount."),
        ("TC-12", "Order", "Create order with empty cart.", "Validation fails with 400 Bad Request."),
        ("TC-13", "Order", "Doctor views own order history.", "Returns only orders matching the logged-in doctor ID."),
        ("TC-14", "Order", "Admin verifies pending order.", "Order status changes from 'Pending' to 'Verified'."),
        ("TC-15", "Order", "Admin marks order as picked up.", "Order status updates to 'PickedUp' in pickup section."),
        ("TC-16", "Order", "Doctor cancels order before pickup.", "Order status updates to 'Cancelled' and stock is released."),
        ("TC-17", "Payment", "Simulate payment for pending order.", "Payment record created with status 'Completed'."),
        ("TC-18", "Payment", "Simulate duplicate payment.", "Rejected due to 1:1 unique constraint on OrderId."),
        ("TC-19", "SaleReport", "Generate report for date range.", "Calculates total orders, total revenue, and profit."),
        ("TC-20", "SaleReport", "Export sales report to CSV.", "Generates CSV file byte array for download.")
    ]

    for idx, (tc_id, mod, scen, exp) in enumerate(test_cases, start=1):
        tbl_test.cell(idx, 0).width = Inches(0.8)
        tbl_test.cell(idx, 1).width = Inches(1.2)
        tbl_test.cell(idx, 2).width = Inches(2.2)
        tbl_test.cell(idx, 3).width = Inches(2.3)
        set_cell_margins(tbl_test.cell(idx, 0), top=40, bottom=40)
        set_cell_margins(tbl_test.cell(idx, 1), top=40, bottom=40)
        set_cell_margins(tbl_test.cell(idx, 2), top=40, bottom=40)
        set_cell_margins(tbl_test.cell(idx, 3), top=40, bottom=40)
        tbl_test.cell(idx, 0).paragraphs[0].add_run(tc_id).font.size = Pt(8.5)
        tbl_test.cell(idx, 1).paragraphs[0].add_run(mod).font.size = Pt(8.5)
        tbl_test.cell(idx, 2).paragraphs[0].add_run(scen).font.size = Pt(8.5)
        tbl_test.cell(idx, 3).paragraphs[0].add_run(exp).font.size = Pt(8.5)

    doc.save(output_path)
    print(f"Generated Word DOCX successfully: {output_path}")

if __name__ == "__main__":
    build_docx(WORKSPACE_DOCX)
    build_docx(ARTIFACT_DOCX)
