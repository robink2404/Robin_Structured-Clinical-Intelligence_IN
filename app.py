"""
Clinical Document Intelligence Hub - Streamlit Application
A modern AI-powered dashboard for unstructured clinical document parsing,
structured data extraction, confidence scoring, evidence traceability, 
and deterministic risk evaluation.
"""

import json
import streamlit as st
from pathlib import Path

from config import OPENAI_API_KEY, GEMINI_API_KEY, get_active_provider
from services.document_processor import extract_text_from_file
from services.clinical_ai import analyze_document
from models.clinical_models import ClinicalSummary

# Set Page Config
st.set_page_config(
    page_title="Clinical Document Intelligence Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Premium Clinical Aesthetics & Theme
st.markdown("""
<style>
    /* Main Screen Background: RGB(27, 23, 40) */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: rgb(27, 23, 40) !important;
        color: #f1f5f9 !important;
    }
    
    /* Sidebar Background: #3D1E6D */
    section[data-testid="stSidebar"] {
        background-color: #3D1E6D !important;
        border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Stylish Sidebar Toggle Button (<< / >>) */
    button[data-testid="stSidebarCollapseButton"], 
    button[data-testid="stSidebarExpandButton"],
    [data-testid="stHeader"] button {
        background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.6) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    button[data-testid="stSidebarCollapseButton"]:hover, 
    button[data-testid="stSidebarExpandButton"]:hover {
        transform: scale(1.12) !important;
        box-shadow: 0 6px 20px rgba(217, 70, 239, 0.8) !important;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
    }

    /* Header Banner */
    .main-header {
        background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 100%);
        padding: 24px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .header-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 1rem;
        color: #c084fc;
        margin-top: 4px;
    }

    /* Cards & Containers for Dark Mode */
    .patient-card {
        background-color: #272138;
        border: 1px solid #4c3b71;
        border-left: 5px solid #a855f7;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .risk-high {
        background-color: #3b1820;
        border: 1px solid #7f1d1d;
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        color: #fee2e2;
    }
    .risk-medium {
        background-color: #382512;
        border: 1px solid #78350f;
        border-left: 5px solid #f59e0b;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        color: #fef3c7;
    }
    .risk-low {
        background-color: #122c20;
        border: 1px solid #14532d;
        border-left: 5px solid #22c55e;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        color: #dcfce7;
    }
    .badge-high {
        background-color: #ef4444;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .evidence-box {
        background-color: #201a30;
        font-style: italic;
        font-size: 0.88rem;
        padding: 10px 14px;
        border-radius: 6px;
        border: 1px dashed #6b5597;
        margin-top: 8px;
        color: #cbd5e1;
    }
    .confidence-tag {
        float: right;
        font-size: 0.8rem;
        color: #c084fc;
        font-weight: 600;
    }

    /* Style Text Areas & Inputs */
    .stTextArea textarea {
        background-color: #201b30 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4c3b71 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


def load_sample_file(sample_name: str) -> tuple:
    """Load pre-packaged sample document text and filename."""
    sample_dir = Path(__file__).parent / "sample_data"
    
    mapping = {
        "Inpatient Discharge Summary (PDF)": ("discharge_summary.pdf", "discharge_summary.txt"),
        "Outpatient Lab Report (PDF)": ("lab_report.pdf", "lab_report.txt"),
        "ED Physician Note (TXT)": ("physician_note.txt", "physician_note.txt"),
        "Cardiology STEMI Consult (PDF)": ("cardiology_consultation.pdf", "cardiology_consultation.txt"),
        "Pediatric Urgent Care Note (PDF)": ("pediatric_intake.pdf", "pediatric_intake.txt"),
        "Oncology Chemotherapy Lab (PDF)": ("oncology_chemo_lab.pdf", "oncology_chemo_lab.txt")
    }

    if sample_name in mapping:
        pdf_file, txt_file = mapping[sample_name]
        pdf_path = sample_dir / pdf_file
        if pdf_path.exists() and pdf_file.endswith(".pdf"):
            return pdf_path.read_bytes(), pdf_file, "application/pdf"
        txt_path = sample_dir / txt_file
        if txt_path.exists():
            return txt_path.read_bytes(), txt_file, "text/plain"

    return b"Sample document not found.", "sample.txt", "text/plain"


def main():
    # Header Banner
    st.markdown("""
    <div class="main-header">
        <div class="header-title">🏥 Clinical Document Intelligence Hub</div>
        <div class="header-subtitle">AI-Powered Extraction • Deterministic Risk Engine • Clinical Decision Support</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Settings
    st.sidebar.header("⚙️ Document & Model Settings")

    input_mode = st.sidebar.radio(
        "Choose Document Input Source:",
        ["Load Sample Document", "Upload Custom Document"]
    )

    file_bytes = None
    file_name = ""
    file_type = ""

    if input_mode == "Load Sample Document":
        sample_choice = st.sidebar.selectbox(
            "Select Realistic Clinical Sample:",
            [
                "Inpatient Discharge Summary (PDF)",
                "Outpatient Lab Report (PDF)",
                "ED Physician Note (TXT)",
                "Cardiology STEMI Consult (PDF)",
                "Pediatric Urgent Care Note (PDF)",
                "Oncology Chemotherapy Lab (PDF)"
            ]
        )
        file_bytes, file_name, file_type = load_sample_file(sample_choice)
        st.sidebar.info(f"Loaded sample file: `{file_name}`")

    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload Clinical Document:",
            type=["pdf", "png", "jpg", "jpeg", "txt"],
            help="Supported formats: PDF documents, plain text notes, PNG/JPG image scans."
        )
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name
            file_type = uploaded_file.type

    # Provider Selection & Key Inputs
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 AI Processing Engine")

    active_provider = get_active_provider()
    provider_options = ["auto (Auto-Detect)", "mock (Deterministic Engine)", "openai (OpenAI GPT-4o)", "gemini (Google Gemini 2.5)"]
    
    selected_provider_raw = st.sidebar.selectbox(
        "AI Provider:",
        provider_options,
        index=0
    )

    selected_provider = selected_provider_raw.split()[0]
    user_api_key = None

    # Dynamic API Key Input field when Gemini or OpenAI is selected
    if selected_provider == "gemini":
        user_api_key = st.sidebar.text_input(
            "🔑 Enter Gemini API Key:",
            value=GEMINI_API_KEY,
            type="password",
            help="Paste your Google Gemini API Key here to enable live AI extraction."
        )
    elif selected_provider == "openai":
        user_api_key = st.sidebar.text_input(
            "🔑 Enter OpenAI API Key:",
            value=OPENAI_API_KEY,
            type="password",
            help="Paste your OpenAI API Key here to enable live AI extraction."
        )

    # Key Resolution & Active Provider Logic
    effective_openai_key = user_api_key if selected_provider == "openai" else OPENAI_API_KEY
    effective_gemini_key = user_api_key if selected_provider == "gemini" else GEMINI_API_KEY

    if selected_provider == "auto":
        if OPENAI_API_KEY:
            selected_provider = "openai"
        elif GEMINI_API_KEY:
            selected_provider = "gemini"
        else:
            selected_provider = "mock"

    st.sidebar.caption(f"Active Provider: **{selected_provider.upper()}**")

    active_key = effective_openai_key if selected_provider == "openai" else (effective_gemini_key if selected_provider == "gemini" else None)

    if selected_provider == "openai" and not active_key:
        st.sidebar.info("💡 Running on **Universal Clinical Parser Engine** (Zero-Dependency Mode). Enter OpenAI key above to use live GPT-4o.")
    elif selected_provider == "gemini" and not active_key:
        st.sidebar.info("💡 Running on **Universal Clinical Parser Engine** (Zero-Dependency Mode). Enter Gemini key above to use live Gemini 2.5.")
    elif selected_provider == "mock":
        st.sidebar.success("✅ Running on **Universal Clinical Parser Engine**.")

    # Main Execution Area
    if file_bytes:
        # Ingestion & Extraction
        doc_info = extract_text_from_file(file_name, file_bytes, file_type)

        # Top Quick Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Document Name", doc_info["file_name"][:18] + "...")
        col2.metric("Format", doc_info["format"])
        col3.metric("Page Count", doc_info["page_count"])
        col4.metric("Word Count", f"{doc_info['word_count']} words")

        st.markdown("---")

        # Two-Column Layout: Raw Document vs Clinical Dashboard
        left_col, right_col = st.columns([1, 1.25])

        with left_col:
            st.subheader("📄 Raw Document Source")
            st.text_area(
                "Extracted Text View",
                value=doc_info["text"],
                height=520,
                disabled=True
            )

        with right_col:
            st.subheader("🧠 Structured Clinical Intelligence")

            # Process Document Button / Auto Run
            with st.spinner(f"Processing document through {selected_provider.upper()} & Risk Engine..."):
                clinical_output: ClinicalSummary = analyze_document(
                    doc_info["text"],
                    override_provider=selected_provider,
                    api_key=active_key
                )

            # Patient Overview Header Card
            patient = clinical_output.patient
            st.markdown(f"""
            <div class="patient-card">
                <div style="font-size: 1.1rem; font-weight: bold; color: #1e3a8a;">
                    👤 Patient: {patient.name or 'Unknown'}
                </div>
                <div style="font-size: 0.9rem; color: #475569; margin-top: 4px;">
                    <strong>Age:</strong> {patient.age or 'N/A'} yrs &nbsp;|&nbsp; 
                    <strong>Gender:</strong> {patient.gender or 'N/A'} &nbsp;|&nbsp; 
                    <strong>MRN:</strong> {patient.mrn or 'N/A'} &nbsp;|&nbsp; 
                    <strong>Type:</strong> <span style="color:#2563eb; font-weight:600;">{clinical_output.document_type}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tabs for Clinical Data Views
            tab_summary, tab_risks, tab_clinical, tab_labs, tab_json = st.tabs([
                "📋 Executive Summary",
                "🔴 Risk Flags",
                "💊 Diagnoses & Meds",
                "🧪 Lab Findings",
                "💻 Raw JSON"
            ])

            # Tab 1: Executive Summary & Recommendation
            with tab_summary:
                st.markdown("#### Clinical Narrative Summary")
                st.info(clinical_output.summary)

                if clinical_output.chief_complaint:
                    st.markdown(f"**Chief Complaint / Presenting Problem:** `{clinical_output.chief_complaint}`")

                st.markdown("#### 💡 Recommended Next Step (Decision Support)")
                st.success(clinical_output.recommended_next_step)
                st.caption("🔒 Decision support recommendation only. Must be validated by a licensed clinician.")

            # Tab 2: Risk Flags & Evidence
            with tab_risks:
                st.markdown("#### Clinical Safety & Risk Warnings")
                if not clinical_output.risk_flags:
                    st.success("No critical clinical risk flags detected.")
                else:
                    for risk in clinical_output.risk_flags:
                        card_class = "risk-high" if risk.severity == "HIGH" else ("risk-medium" if risk.severity == "MEDIUM" else "risk-low")
                        icon = "🔴" if risk.severity == "HIGH" else ("🟠" if risk.severity == "MEDIUM" else "🟢")

                        st.markdown(f"""
                        <div class="{card_class}">
                            <div style="font-weight: bold; font-size: 1rem;">
                                {icon} [{risk.severity}] {risk.issue}
                                <span class="confidence-tag">Confidence: {risk.confidence:.0%}</span>
                            </div>
                            <div class="evidence-box">
                                📌 <strong>Evidence Quote:</strong> "{risk.evidence}"
                            </div>
                            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">
                                Source: <em>{risk.source}</em>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Tab 3: Diagnoses & Medications
            with tab_clinical:
                col_d, col_m = st.columns(2)
                
                with col_d:
                    st.markdown("#### Diagnoses")
                    if clinical_output.diagnoses:
                        for d in clinical_output.diagnoses:
                            st.markdown(f"• **{d}**")
                    else:
                        st.write("No diagnoses documented.")

                    st.markdown("#### ⚠️ Documented Allergies")
                    if clinical_output.allergies:
                        for a in clinical_output.allergies:
                            st.warning(f" Allergic reaction: **{a}**")
                    else:
                        st.write("No allergies documented.")

                with col_m:
                    st.markdown("#### Prescribed Medications")
                    if clinical_output.medications:
                        for m in clinical_output.medications:
                            st.markdown(f"• **{m.name}** - {m.dose or ''} {m.frequency or ''} (`{m.route or 'Oral'}`)")
                    else:
                        st.write("No active medications documented.")

            # Tab 4: Lab Findings
            with tab_labs:
                st.markdown("#### Extracted Laboratory Results")
                if clinical_output.lab_results:
                    lab_data = []
                    for lab in clinical_output.lab_results:
                        lab_data.append({
                            "Test Name": lab.test_name,
                            "Value": f"{lab.value} {lab.unit or ''}",
                            "Reference Range": lab.reference_range or "N/A",
                            "Status": lab.status,
                            "Confidence": f"{lab.confidence:.0%}",
                            "Evidence": lab.evidence or ""
                        })
                    st.dataframe(lab_data)
                else:
                    st.write("No lab results detected in this document.")

            # Tab 5: Raw JSON
            with tab_json:
                st.markdown("#### Validated Pydantic Structured Output")
                json_str = clinical_output.model_dump_json(indent=2)
                st.code(json_str, language="json")
                st.download_button(
                    label="📥 Export Clinical JSON",
                    data=json_str,
                    file_name=f"clinical_intelligence_{file_name}.json",
                    mime="application/json"
                )

    else:
        st.info("👈 Please select a sample document or upload a file from the sidebar to begin analysis.")


if __name__ == "__main__":
    main()
