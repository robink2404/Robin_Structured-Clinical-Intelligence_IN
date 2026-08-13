"""
Presentation Slide Deck Generator.
Recreates the high-end 5-slide PDF presentation deck matching the design theme:
Dark Teal (#09252C) / Emerald Teal (#00A887) / Crisp Light Typography.
"""

import fitz
from pathlib import Path

SLIDES_DIR = Path(__file__).parent
OUTPUT_PDF = SLIDES_DIR / "summary_deck.pdf"


def hex_to_rgb(hex_str: str):
    """Convert hex string (e.g. #09252C) to normalized RGB tuple (0.0 - 1.0)."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))


# Color Palette
BG_DARK = hex_to_rgb("#09252C")
CARD_DARK = hex_to_rgb("#10353F")
BORDER_TEAL = hex_to_rgb("#006B5B")
TEAL_ACCENT = hex_to_rgb("#00A887")
TEXT_WHITE = hex_to_rgb("#FFFFFF")
TEXT_LIGHT = hex_to_rgb("#D1E5E7")
BG_LIGHT = hex_to_rgb("#F4F8F8")
TEXT_DARK_TITLE = hex_to_rgb("#09252C")


def build_slide_1(doc):
    """Slide 1: Problem Understanding & Objective (Dark Theme)"""
    page = doc.new_page(width=960, height=540)
    page.draw_rect(fitz.Rect(0, 0, 960, 540), color=BG_DARK, fill=BG_DARK)

    # Top Tag
    page.insert_text(fitz.Point(50, 45), "PROOF OF CONCEPT  ·  CLINICAL AI", fontsize=11, fontname="helv", color=TEAL_ACCENT)
    
    # Title & Subtitle
    page.insert_text(fitz.Point(50, 85), "Clinical Document Intelligence Hub", fontsize=28, fontname="helv", color=TEXT_WHITE)
    page.insert_text(fitz.Point(50, 115), "Automating Healthcare Document Processing", fontsize=14, fontname="helv", color=TEXT_LIGHT)

    # Card 1: Problem Context
    rect_c1 = fitz.Rect(50, 145, 460, 290)
    page.draw_rect(rect_c1, color=BORDER_TEAL, fill=CARD_DARK)
    page.insert_text(fitz.Point(75, 175), "Problem Context", fontsize=14, fontname="helv", color=TEAL_ACCENT)
    page.insert_textbox(fitz.Rect(75, 195, 435, 275), "Healthcare providers spend thousands of hours manually reviewing unstructured clinical documents — discharge summaries, lab reports, intake forms.", fontsize=11, fontname="helv", color=TEXT_LIGHT)

    # Card 2: Core Bottlenecks
    rect_c2 = fitz.Rect(480, 145, 890, 290)
    page.draw_rect(rect_c2, color=BORDER_TEAL, fill=CARD_DARK)
    page.insert_text(fitz.Point(505, 175), "Core Bottlenecks", fontsize=14, fontname="helv", color=TEAL_ACCENT)
    page.insert_textbox(fitz.Rect(505, 195, 865, 275), "Manual data entry is slow, inconsistent, and highly error-prone — creating administrative delays in patient care pathways.", fontsize=11, fontname="helv", color=TEXT_LIGHT)

    # Card 3 (Banner): Project Objective
    rect_c3 = fitz.Rect(50, 310, 890, 390)
    page.draw_rect(rect_c3, color=TEAL_ACCENT, fill=TEAL_ACCENT)
    page.insert_text(fitz.Point(75, 335), "Project Objective", fontsize=13, fontname="helv", color=BG_DARK)
    page.insert_textbox(fitz.Rect(75, 345, 865, 380), "Build a working proof-of-concept AI prototype that ingests unstructured clinical inputs (PDF, TXT, Image) and surfaces decision-ready structured intelligence.", fontsize=11, fontname="helv", color=BG_DARK)

    # Value Prop & Big Metric
    page.insert_text(fitz.Point(50, 420), "Value Proposition", fontsize=12, fontname="helv", color=TEAL_ACCENT)
    page.insert_textbox(fitz.Rect(50, 435, 650, 490), "Transform fragmented document text into standardized clinical outputs, risk alerts, and evidence-backed next steps.", fontsize=11, fontname="helv", color=TEXT_LIGHT)

    page.insert_text(fitz.Point(770, 455), "70%+", fontsize=36, fontname="helv", color=TEAL_ACCENT)
    page.insert_text(fitz.Point(740, 480), "reduction in manual workload", fontsize=10, fontname="helv", color=TEXT_LIGHT)

    # Footer
    page.insert_text(fitz.Point(50, 520), "Clinical Document Intelligence Hub", fontsize=9, fontname="helv", color=BORDER_TEAL)
    page.insert_text(fitz.Point(890, 520), "1 / 5", fontsize=9, fontname="helv", color=BORDER_TEAL)


def build_slide_2(doc):
    """Slide 2: Solution Architecture & Design Flow (Light Theme)"""
    page = doc.new_page(width=960, height=540)
    page.draw_rect(fitz.Rect(0, 0, 960, 540), color=BG_LIGHT, fill=BG_LIGHT)

    # Header
    page.insert_text(fitz.Point(50, 55), "Solution Architecture & Design Flow", fontsize=26, fontname="helv", color=TEXT_DARK_TITLE)
    page.insert_text(fitz.Point(50, 80), "Hybrid AI Ingestion, Extraction, and Safety Verification Architecture", fontsize=13, fontname="helv", color=hex_to_rgb("#4B6B75"))

    steps = [
        ("1", "Document Ingestion Layer", "Multi-format parsing accepting PDFs (PyMuPDF), text files, and image scans."),
        ("2", "Clinical LLM Extraction", "Prompt-engineered structured extraction forcing strict Pydantic JSON schema adherence."),
        ("3", "Deterministic Safety & Risk Engine", "Rules engine post-processes extracted facts — e.g. WBC > 11.0, Penicillin + Amoxicillin allergy contraindications."),
        ("4", "Confidence & Evidence Layer", "Assigns confidence scores (0–100%) and extracts exact source-text evidence quotes for total clinical auditability."),
        ("5", "Streamlit Dashboard UI", "Clean clinical interface featuring Patient Overview Cards, Risk Flags, Diagnoses/Meds, Lab Tables, and JSON Export.")
    ]

    start_y = 120
    for num, title, desc in steps:
        # Circle badge
        page.draw_circle(fitz.Point(75, start_y + 20), 18, color=TEAL_ACCENT, fill=TEAL_ACCENT)
        page.insert_text(fitz.Point(71, start_y + 25), num, fontsize=13, fontname="helv", color=TEXT_WHITE)

        # Title & Desc
        page.insert_text(fitz.Point(120, start_y + 16), title, fontsize=13, fontname="helv", color=TEXT_DARK_TITLE)
        page.insert_text(fitz.Point(120, start_y + 34), desc, fontsize=10, fontname="helv", color=hex_to_rgb("#334E57"))

        start_y += 72

    # Footer
    page.insert_text(fitz.Point(50, 520), "Clinical Document Intelligence Hub", fontsize=9, fontname="helv", color=hex_to_rgb("#8AA4AD"))
    page.insert_text(fitz.Point(890, 520), "2 / 5", fontsize=9, fontname="helv", color=hex_to_rgb("#8AA4AD"))


def build_slide_3(doc):
    """Slide 3: Implementation Highlights (Light Theme)"""
    page = doc.new_page(width=960, height=540)
    page.draw_rect(fitz.Rect(0, 0, 960, 540), color=BG_LIGHT, fill=BG_LIGHT)

    # Header
    page.insert_text(fitz.Point(50, 55), "Implementation Highlights", fontsize=26, fontname="helv", color=TEXT_DARK_TITLE)
    page.insert_text(fitz.Point(50, 80), "Technical Decisions, AI Logic & System Quality Controls", fontsize=13, fontname="helv", color=hex_to_rgb("#4B6B75"))

    cards = [
        ("{}", "Structured JSON Schema", "Enforced using Pydantic models — Patient, Medication, LabResult, RiskFlag, ClinicalSummary.", 50, 115),
        ("⚙", "Hybrid Reasoning Architecture", "LLM used for unstructured text extraction, paired with deterministic code rules for high-stakes medical thresholds.", 480, 115),
        ("”", "Evidence Traceability", "Every risk flag and abnormal lab includes exact quote citations from the source document.", 50, 305),
        ("⇄", "Zero-Downtime Multi-Provider Strategy", "Seamless support for OpenAI GPT-4o, Google Gemini 2.5, and a zero-dependency deterministic fallback engine.", 480, 305)
    ]

    for icon, title, desc, x, y in cards:
        rect = fitz.Rect(x, y, x + 430, y + 165)
        page.draw_rect(rect, color=hex_to_rgb("#D6E4E7"), fill=hex_to_rgb("#EFF6F7"))

        # Icon Circle
        page.draw_circle(fitz.Point(x + 40, y + 45), 20, color=TEAL_ACCENT, fill=TEAL_ACCENT)
        page.insert_text(fitz.Point(x + 32, y + 51), icon, fontsize=14, fontname="helv", color=TEXT_WHITE)

        page.insert_text(fitz.Point(x + 75, y + 50), title, fontsize=14, fontname="helv", color=TEXT_DARK_TITLE)
        page.insert_textbox(fitz.Rect(x + 30, y + 80, x + 400, y + 150), desc, fontsize=11, fontname="helv", color=hex_to_rgb("#334E57"))

    # Footer
    page.insert_text(fitz.Point(50, 520), "Clinical Document Intelligence Hub", fontsize=9, fontname="helv", color=hex_to_rgb("#8AA4AD"))
    page.insert_text(fitz.Point(890, 520), "3 / 5", fontsize=9, fontname="helv", color=hex_to_rgb("#8AA4AD"))


def build_slide_4(doc):
    """Slide 4: Challenges & Learnings (Dark Theme)"""
    page = doc.new_page(width=960, height=540)
    page.draw_rect(fitz.Rect(0, 0, 960, 540), color=BG_DARK, fill=BG_DARK)

    # Header
    page.insert_text(fitz.Point(50, 55), "Challenges & Learnings", fontsize=26, fontname="helv", color=TEXT_WHITE)
    page.insert_text(fitz.Point(50, 80), "Addressing Hallucinations, Safety Scoping, and Unstructured Data Variability", fontsize=13, fontname="helv", color=TEXT_LIGHT)

    cols = [
        ("1", "Hallucination Prevention", "Strictly constrained LLM prompt rules to extract ONLY explicitly stated facts; unmentioned fields return null.", 50),
        ("2", "Clinical Safety", "Scoped all recommendations as decision-support suggestions rather than autonomous diagnoses.", 345),
        ("3", "Document Formatting Variance", "Standardized multi-format text extraction pipeline to handle noisy PDFs and plain text notes uniformly.", 640)
    ]

    for num, title, desc, x in cols:
        rect = fitz.Rect(x, 115, x + 270, 350)
        page.draw_rect(rect, color=BORDER_TEAL, fill=CARD_DARK)

        page.draw_circle(fitz.Point(x + 35, 155), 18, color=TEAL_ACCENT, fill=TEAL_ACCENT)
        page.insert_text(fitz.Point(x + 30, 160), num, fontsize=13, fontname="helv", color=BG_DARK)

        page.insert_text(fitz.Point(x + 25, 205), title, fontsize=13, fontname="helv", color=TEXT_WHITE)
        page.insert_textbox(fitz.Rect(x + 25, 225, x + 245, 330), desc, fontsize=10, fontname="helv", color=TEXT_LIGHT)

    # Key Takeaway Banner
    rect_takeaway = fitz.Rect(50, 370, 890, 480)
    page.draw_rect(rect_takeaway, color=TEAL_ACCENT, fill=TEAL_ACCENT)
    page.insert_text(fitz.Point(75, 395), "KEY TAKEAWAY", fontsize=10, fontname="helv", color=BG_DARK)
    page.insert_textbox(fitz.Rect(75, 410, 865, 465), "Combining LLM semantic flexibility with deterministic rule validation provides the ideal balance of accuracy and safety in healthcare software.", fontsize=13, fontname="helv", color=BG_DARK)

    # Footer
    page.insert_text(fitz.Point(50, 520), "Clinical Document Intelligence Hub", fontsize=9, fontname="helv", color=BORDER_TEAL)
    page.insert_text(fitz.Point(890, 520), "4 / 5", fontsize=9, fontname="helv", color=BORDER_TEAL)


def build_slide_5(doc):
    """Slide 5: Demo Summary & Next Steps (Light Theme)"""
    page = doc.new_page(width=960, height=540)
    page.draw_rect(fitz.Rect(0, 0, 960, 540), color=BG_LIGHT, fill=BG_LIGHT)

    # Header
    page.insert_text(fitz.Point(50, 55), "Demo Summary & Next Steps", fontsize=26, fontname="helv", color=TEXT_DARK_TITLE)
    page.insert_text(fitz.Point(50, 80), "Working Prototype Deliverables & Strategic Roadmap", fontsize=13, fontname="helv", color=hex_to_rgb("#4B6B75"))

    # Delivered Artifacts Banner
    rect_art = fitz.Rect(50, 110, 890, 185)
    page.draw_rect(rect_art, color=hex_to_rgb("#007D8B"), fill=hex_to_rgb("#007D8B"))
    page.insert_text(fitz.Point(75, 133), "Delivered Artifacts", fontsize=11, fontname="helv", color=TEXT_WHITE)
    page.insert_textbox(fitz.Rect(75, 145, 865, 175), "Full working Streamlit application, sample datasets (PDF/TXT), and 1-page executive README.", fontsize=11, fontname="helv", color=TEXT_WHITE)

    page.insert_text(fitz.Point(50, 215), "Next Steps — Strategic Roadmap", fontsize=13, fontname="helv", color=TEXT_DARK_TITLE)

    cols_rs = [
        ("1", "Healthcare Integration", "HL7 / FHIR API export for direct EHR integration — Epic, Cerner, AthenaHealth.", 50),
        ("2", "Safety & Security", "Enterprise HIPAA compliance, PHI de-identification (PII/PHI anonymization pipeline), and OAuth2 RBAC.", 350),
        ("3", "Clinical Workflow", "Human-in-the-loop clinician sign-off workflow and multi-document longitudinal patient timelines.", 650)
    ]

    for num, title, desc, x in cols_rs:
        rect = fitz.Rect(x, 235, x + 260, 480)
        page.draw_rect(rect, color=hex_to_rgb("#D6E4E7"), fill=hex_to_rgb("#FFFFFF"))

        page.draw_circle(fitz.Point(x + 35, 275), 18, color=TEAL_ACCENT, fill=TEAL_ACCENT)
        page.insert_text(fitz.Point(x + 30, 280), num, fontsize=13, fontname="helv", color=TEXT_WHITE)

        page.insert_text(fitz.Point(x + 25, 325), title, fontsize=13, fontname="helv", color=TEXT_DARK_TITLE)
        page.insert_textbox(fitz.Rect(x + 25, 350, x + 235, 460), desc, fontsize=10, fontname="helv", color=hex_to_rgb("#334E57"))

    # Footer
    page.insert_text(fitz.Point(50, 520), "Clinical Document Intelligence Hub", fontsize=9, fontname="helv", color=hex_to_rgb("#8AA4AD"))
    page.insert_text(fitz.Point(890, 520), "5 / 5", fontsize=9, fontname="helv", color=hex_to_rgb("#8AA4AD"))


def main():
    doc = fitz.open()
    build_slide_1(doc)
    build_slide_2(doc)
    build_slide_3(doc)
    build_slide_4(doc)
    build_slide_5(doc)
    doc.save(str(OUTPUT_PDF))
    doc.close()
    print(f"Summary deck generated at {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
