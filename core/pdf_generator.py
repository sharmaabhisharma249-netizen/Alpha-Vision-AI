from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def score_bar(score, maximum=135):

    filled = int((score / maximum) * 20)

    return "█" * filled + "░" * (20 - filled)


def create_pdf(report, filename):

    doc = SimpleDocTemplate(
        filename,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35,
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]

    normal = styles["BodyText"]
    # ==========================================
# CUSTOM STYLES
# ==========================================

    report_title = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=26,
        textColor=HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceAfter=18,
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=10,
    )

    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=18,
    )

    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.grey,
    )
    story = []

    # ==================================================
# PAGE 1
# EXECUTIVE SUMMARY
# ==================================================

    story.append(
        Paragraph(
            "AlphaVision AI",
            report_title,
        )
    )

    story.append(
        Paragraph(
            "<b>Professional Equity Research Report</b>",
            section_heading,
        )
    )

    story.append(Spacer(1,0.25*inch))

    story.append(
        Paragraph(
            f"<b>Company</b> : {report['Company']}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Symbol</b> : {report['Symbol']}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated</b> : {datetime.now().strftime('%d %B %Y')}",
            body,
        )
    )

    story.append(Spacer(1,0.30*inch))

    story.append(
        Paragraph(
            "<b>Overall Score</b>",
            section_heading,
        )
    )

    story.append(
        Paragraph(
            f"<font size='18'>{report['Score']} / 135</font>",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<font size='16'>{score_bar(report['Score'])}</font>",
            body,
        )
    )

    story.append(Spacer(1,0.20*inch))

    story.append(
        Paragraph(
            f"<b>Recommendation :</b> {report['Recommendation']}",
            body,
        )
    )

    story.append(Spacer(1,0.35*inch))
    story.append(Spacer(1, 0.25 * inch))

    score_data = [
        [
            f"<b>Fundamental</b><br/>{report['Fundamental']} / 70",
            f"<b>Technical</b><br/>{report['Technical']} / 20",
        ],
        [
            f"<b>Valuation</b><br/>{report['Valuation']} / 30",
            f"<b>Risk</b><br/>{report['Risk']} / 15",
        ],
    ]

    score_table = Table(
        score_data,
        colWidths=[250, 250],
        rowHeights=[60, 60],
    )

    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    story.append(score_table)

    story.append(Spacer(1, 0.30 * inch))
    story.append(
        Paragraph(
            "<b>Executive Summary</b>",
            section_heading,
        )
    )

    summary = f"""
    <b>{report['Company']}</b> achieved an overall AlphaVision AI score
    of <b>{report['Score']}/135</b>.

    The stock currently carries a recommendation of
    <b>{report['Recommendation']}</b> based on the combined evaluation of
    fundamental strength, technical momentum, valuation attractiveness,
    and financial risk.

    This report is intended to provide investors with a structured,
    AI-assisted overview before making investment decisions.
    """

    story.append(
        Paragraph(
            summary,
            body,
        )
    )
    story.append(PageBreak())
    # ==================================================
    # FINANCIAL TABLE
    # ==================================================

    story.append(
        Paragraph(
            "Financial Overview",
            heading,
        )
    )

    data = [
        ["Metric", "Value"],
        ["Current Price", report["Current Price"]],
        ["PE Ratio", report["PE"]],
        ["PB Ratio", report["PB"]],
        ["ROE", report["ROE"]],
        ["Debt / Equity", report["Debt"]],
        ["Fundamental Score", report["Fundamental"]],
        ["Technical Score", report["Technical"]],
        ["Valuation Score", report["Valuation"]],
        ["Risk Score", report["Risk"]],
    ]

    table = Table(
        data,
        colWidths=[220, 180],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 0.4 * inch))

    # ==================================================
    # INVESTMENT SUMMARY
    # ==================================================

    story.append(
        Paragraph(
            "Investment Summary",
            heading,
        )
    )

    if report["Score"] >= 110:

        summary = """
        <b>STRONG BUY</b><br/><br/>

        • Excellent overall score.<br/>
        • Strong business fundamentals.<br/>
        • Healthy technical trend.<br/>
        • Attractive valuation.<br/>
        • Suitable for long-term investment.
        """

    elif report["Score"] >= 90:

        summary = """
        <b>BUY</b><br/><br/>

        • Good overall fundamentals.<br/>
        • Positive trend.<br/>
        • Can be accumulated gradually.
        """

    elif report["Score"] >= 70:

        summary = """
        <b>WATCHLIST</b><br/><br/>

        • Mixed signals.<br/>
        • Wait for better entry.
        """

    else:

        summary = """
        <b>AVOID</b><br/><br/>

        • Weak score.<br/>
        • High investment risk.
        """

    story.append(
        Paragraph(
            summary,
            normal,
        )
    )

    story.append(Spacer(1, 0.5 * inch))

    story.append(
        Paragraph(
            "<font color='grey'>Generated by AlphaVision AI</font>",
            normal,
        )
    )

    story.append(
        Paragraph(
            "<font color='grey'>For Educational Purpose Only</font>",
            normal,
        )
    )

    doc.build(story)