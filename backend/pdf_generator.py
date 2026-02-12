"""
Federal Disclosure Form PDF Generator
=======================================
Generates a professional-looking government-style PDF form
for AI Training Data Disclosure pursuant to the CLEAR Act of 2026.
"""

import io
from datetime import datetime
from typing import List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

from .models import AuditResult, DisclosureFormData, RiskLevel


def generate_disclosure_pdf(form_data: DisclosureFormData, audit: Optional[AuditResult] = None) -> bytes:
    """Generate a Federal Disclosure Form PDF and return as bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        "FormTitle", parent=styles["Title"],
        fontSize=16, spaceAfter=4, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "FormSubtitle", parent=styles["Normal"],
        fontSize=10, spaceAfter=12, fontName="Helvetica",
        alignment=TA_CENTER, textColor=colors.HexColor("#444444"),
    ))
    styles.add(ParagraphStyle(
        "SectionHeader", parent=styles["Heading2"],
        fontSize=11, fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=6,
        borderWidth=0, borderPadding=0, borderColor=colors.black,
        textColor=colors.HexColor("#1a1a1a"),
    ))
    styles.add(ParagraphStyle(
        "FieldLabel", parent=styles["Normal"],
        fontSize=8, fontName="Helvetica", textColor=colors.HexColor("#666666"),
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "FieldValue", parent=styles["Normal"],
        fontSize=10, fontName="Helvetica-Bold", spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "BodyText", parent=styles["Normal"],
        fontSize=9, fontName="Helvetica", alignment=TA_JUSTIFY,
        spaceAfter=6, leading=12,
    ))
    styles.add(ParagraphStyle(
        "Footer", parent=styles["Normal"],
        fontSize=7, fontName="Helvetica", textColor=colors.HexColor("#999999"),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "SmallText", parent=styles["Normal"],
        fontSize=8, fontName="Helvetica", textColor=colors.HexColor("#555555"),
        spaceAfter=4,
    ))

    elements = []

    # ── Header ────────────────────────────────────────
    elements.append(Paragraph("UNITED STATES FEDERAL REGISTER", styles["FormSubtitle"]))
    elements.append(Paragraph("AI TRAINING DATA DISCLOSURE FORM", styles["FormTitle"]))
    elements.append(Paragraph("Pursuant to the Comprehensive Licensing and Ethical AI Regulation (CLEAR) Act of 2026", styles["FormSubtitle"]))
    elements.append(Paragraph("OMB Control No. 3245-0001  |  Expiration Date: 12/31/2027", styles["Footer"]))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.black))
    elements.append(Spacer(1, 12))

    # ── Section 1: Organization Information ───────────
    elements.append(Paragraph("SECTION 1 — ORGANIZATION INFORMATION", styles["SectionHeader"]))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    elements.append(Spacer(1, 6))

    org_data = [
        ["Organization Name:", form_data.organization_name, "Date of Filing:", form_data.date],
        ["AI Model / System Name:", form_data.model_name, "Form Prepared By:", form_data.contact_name or "N/A"],
        ["Contact Email:", form_data.contact_email or "N/A", "", ""],
    ]
    org_table = Table(org_data, colWidths=[1.5 * inch, 2.5 * inch, 1.3 * inch, 1.7 * inch])
    org_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#555555")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#555555")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (1, 0), (1, -1), 0.5, colors.HexColor("#cccccc")),
        ("LINEBELOW", (3, 0), (3, -1), 0.5, colors.HexColor("#cccccc")),
    ]))
    elements.append(org_table)
    elements.append(Spacer(1, 12))

    # ── Section 2: Disclosure Summary ─────────────────
    elements.append(Paragraph("SECTION 2 — TRAINING DATA SOURCE SUMMARY", styles["SectionHeader"]))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    elements.append(Spacer(1, 6))

    if audit:
        s = audit.summary
        summary_data = [
            ["METRIC", "COUNT", "PERCENTAGE"],
            ["Total Data Sources Reviewed", str(s.total_sources), "100%"],
            ["High-Risk Sources (Copyrighted / Litigious)", str(s.high_risk_count),
             f"{s.high_risk_percentage:.1f}%"],
            ["Medium-Risk Sources (Restricted / TOS)", str(s.medium_risk_count),
             f"{s.medium_risk_count / s.total_sources * 100:.1f}%" if s.total_sources else "0%"],
            ["Low-Risk Sources (Open / Permissive)", str(s.low_risk_count),
             f"{s.low_risk_count / s.total_sources * 100:.1f}%" if s.total_sources else "0%"],
            ["Unclassified Sources", str(s.unknown_risk_count),
             f"{s.unknown_risk_count / s.total_sources * 100:.1f}%" if s.total_sources else "0%"],
        ]
    else:
        summary_data = [
            ["METRIC", "COUNT", "PERCENTAGE"],
            ["Total Data Sources Reviewed", "N/A", "N/A"],
            ["High-Risk Sources", "N/A", "N/A"],
            ["Medium-Risk Sources", "N/A", "N/A"],
            ["Low-Risk Sources", "N/A", "N/A"],
            ["Unclassified Sources", "N/A", "N/A"],
        ]

    summary_table = Table(summary_data, colWidths=[3.5 * inch, 1.5 * inch, 2 * inch])
    summary_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d2d2d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 16))

    # ── Section 3: High-Risk Source Details ───────────
    elements.append(Paragraph("SECTION 3 — HIGH-RISK SOURCE DETAILS", styles["SectionHeader"]))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    elements.append(Spacer(1, 6))

    if audit:
        high_risk_rows = [r for r in audit.rows if r.risk_level == RiskLevel.HIGH]
        if high_risk_rows:
            elements.append(Paragraph(
                f"The following {len(high_risk_rows)} source(s) have been identified as HIGH RISK "
                "due to active litigation, strict copyright enforcement, or restrictive licensing terms:",
                styles["BodyText"],
            ))
            elements.append(Spacer(1, 6))

            hr_data = [["#", "DOMAIN", "PUBLISHER", "CONTENT TYPE", "WORD COUNT", "RISK REASON"]]
            for i, row in enumerate(high_risk_rows, 1):
                hr_data.append([
                    str(i), row.domain, row.publisher or "Unknown",
                    row.content_type, f"{row.word_count:,}" if row.word_count else "N/A",
                    row.risk_reason[:50],
                ])

            hr_table = Table(hr_data, colWidths=[0.3 * inch, 1.2 * inch, 1.3 * inch, 0.9 * inch, 0.8 * inch, 2.5 * inch])
            hr_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#8b0000")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fff5f5"), colors.white]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            elements.append(hr_table)
        else:
            elements.append(Paragraph("No high-risk sources identified.", styles["BodyText"]))
    else:
        elements.append(Paragraph("No audit data provided. Upload a dataset manifest to generate details.", styles["BodyText"]))

    elements.append(Spacer(1, 16))

    # ── Section 4: Medium-Risk Summary ────────────────
    elements.append(Paragraph("SECTION 4 — MEDIUM-RISK SOURCE SUMMARY", styles["SectionHeader"]))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    elements.append(Spacer(1, 6))

    if audit:
        med_rows = [r for r in audit.rows if r.risk_level == RiskLevel.MEDIUM]
        if med_rows:
            domains = {}
            for r in med_rows:
                domains.setdefault(r.domain, 0)
                domains[r.domain] += 1
            domain_list = ", ".join(f"{d} ({c})" for d, c in sorted(domains.items(), key=lambda x: -x[1]))
            elements.append(Paragraph(
                f"{len(med_rows)} medium-risk source(s) identified from the following domains: {domain_list}. "
                "These sources require attribution verification and TOS compliance review.",
                styles["BodyText"],
            ))
        else:
            elements.append(Paragraph("No medium-risk sources identified.", styles["BodyText"]))
    else:
        elements.append(Paragraph("No audit data provided.", styles["BodyText"]))

    elements.append(Spacer(1, 20))

    # ── Section 5: Attestation ────────────────────────
    elements.append(Paragraph("SECTION 5 — ATTESTATION AND CERTIFICATION", styles["SectionHeader"]))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        "I hereby certify that the information provided in this disclosure form is true, accurate, "
        "and complete to the best of my knowledge. I understand that willful misrepresentation "
        "of training data sources may result in penalties under Section 7(c) of the CLEAR Act of 2026, "
        "including fines up to $500,000 per violation and mandatory model withdrawal.",
        styles["BodyText"],
    ))
    elements.append(Spacer(1, 24))

    sig_data = [
        ["Signature: ________________________________________", "Date: ____________________"],
        [f"Name: {form_data.contact_name or '____________________'}", f"Title: ____________________"],
        [f"Organization: {form_data.organization_name}", f"Email: {form_data.contact_email or '____________________'}"],
    ]
    sig_table = Table(sig_data, colWidths=[4 * inch, 3 * inch])
    sig_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(sig_table)
    elements.append(Spacer(1, 20))

    # ── Footer ────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        f"Form CLEAR-2026-001  |  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  |  "
        "This form is machine-generated by ProjectSpark Compliance Engine",
        styles["Footer"],
    ))
    elements.append(Paragraph(
        "Paperwork Reduction Act Statement: This collection of information is estimated to take "
        "approximately 2 hours per response. Send comments regarding this burden estimate to the "
        "Office of AI Governance, Washington, DC 20580.",
        styles["Footer"],
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()
