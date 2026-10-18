
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


def generate_pdf(report):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="BrowserMindTitle",
        parent=styles["Title"],
        fontSize=23,
        leading=29,
        textColor=colors.HexColor("#3448A5"),
        alignment=TA_CENTER,
        spaceAfter=16,
    ))

    styles.add(ParagraphStyle(
        name="BrowserMindBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=9,
        wordWrap="CJK",
    ))

    story = []

    def add_text(value):
        for line in str(value or "").splitlines():
            if line.strip():
                story.append(Paragraph(
                    escape(line),
                    styles["BrowserMindBody"]
                ))
            else:
                story.append(Spacer(1, 7))

    def section(title):
        story.append(Spacer(1, 14))
        story.append(Paragraph(
            escape(title),
            styles["Heading2"]
        ))

    data = report.get("research", report)

    story.append(Paragraph(
        "BrowserMind",
        styles["BrowserMindTitle"]
    ))

    story.append(Paragraph(
        "AI Research Report",
        styles["Heading2"]
    ))

    story.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor("#8B9DFF")
    ))

    section("Research Question")
    add_text(data.get("question", ""))

    section("Research Plan")
    for index, task in enumerate(data.get("tasks", []), 1):
        add_text(f"{index}. {task}")

    section("Research Analysis")
    add_text(data.get("analysis", ""))

    section("Verification")
    add_text(data.get("verdict", "uncertain"))

    section("Sources")
    for source in data.get("sources", []):
        add_text(source.get("url", ""))

    section("Disclaimer")
    add_text(
        "This report was generated with AI assistance. "
        "Verification is preliminary and does not "
        "guarantee factual accuracy."
    )

    document.build(story)
    buffer.seek(0)

    return buffer.getvalue()
