# 🏥 Clinical Document Intelligence Hub

An AI-powered clinical decision-support proof-of-concept that ingests unstructured clinical documents (PDFs, Images, plain text notes), extracts structured key information into validated Pydantic schemas, applies a deterministic clinical safety risk engine, and surfaces decision-ready insights on an interactive Streamlit dashboard.

---

## 🚀 Key Features

1. **Multi-Format Document Ingestion**: Supports `.pdf` (PyMuPDF text layer extraction), `.txt` plain text, and image scans (`.png`, `.jpg`, `.jpeg`).
2. **Strict Pydantic Structured Output**: Enforces valid JSON structure for Patient Demographics, Chief Complaint, Diagnoses, Medications, Allergies, Lab Results (with reference ranges), Risk Flags, and Recommended Next Steps.
3. **Hybrid AI & Deterministic Safety Engine**:
   - **LLM Engine**: Extracts unstructured narrative facts and estimates confidence scores.
   - **Deterministic Risk Rules**: Evaluates hard clinical thresholds (e.g. Leukocytosis `WBC > 11.0 K/uL`, Inflammation `CRP > 10.0 mg/L`, and Beta-Lactam drug-allergy contraindications).
4. **Evidence Traceability & Confidence Scoring**: Assigns 0–100% confidence scores and cites exact source quotes for every extracted lab and risk flag.
5. **Zero-Friction Multi-Provider Fallback**: Seamlessly runs on OpenAI (`gpt-4o-mini`), Google Gemini (`gemini-2.5-flash`), or an offline zero-dependency **Mock Engine** without requiring API keys for evaluation.

---

## 📐 Architecture & Data Flow

```
[ Clinical Doc (PDF / Image / TXT) ]
                │
                ▼
      [ Document Processor ] ── (PyMuPDF / Text Extraction)
                │
                ▼
     [ LLM Extraction Engine ] ── (OpenAI / Gemini / Fallback Engine)
                │
                ▼
    [ Pydantic Schema Validation ]
                │
                ▼
    [ Deterministic Risk Engine ] ── (Lab Thresholds & Allergy Rules)
                │
                ▼
 [ Streamlit Clinical Dashboard ] ── (Patient Card, Risk Flags, Labs, JSON Export)
```

---

## 🛠️ Quickstart & Setup Instructions

### 1. Prerequisites
- Python 3.9+ installed on system.

### 2. Installation
```bash
# Clone or navigate to the project directory
cd clinical-document-intelligence

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```bash
streamlit run app.py
```
The application will open automatically at `http://localhost:8501`.

*(Optional)* Set API keys in environment or `.env` file to use live LLMs:
```bash
export OPENAI_API_KEY="your-openai-api-key"
# OR
export GEMINI_API_KEY="your-gemini-api-key"
```
If no key is set, the app automatically runs in zero-dependency Mock Engine mode.

---

## 📄 Example Input & Output

### Sample Input (`discharge_summary.pdf`)
```text
PATIENT DISCHARGE SUMMARY
Patient Name: John Doe | Age: 67 | Gender: Male | MRN: 984210-A
Chief Complaint: Shortness of breath and fever for 3 days.
Allergies: Penicillin (Severe rash and hives documented in 2018)
Diagnosis: Community Acquired Pneumonia (Right Lower Lobe), Hypertension
Labs: WBC: 15.2 K/uL (Ref: 4.0-11.0), CRP: 82.0 mg/L (Ref: 0.0-5.0)
Discharge Meds: Amoxicillin 500 mg PO TID x 7 days
```

### Extracted Structured Output (`ClinicalSummary` JSON)
```json
{
  "patient": {
    "name": "John Doe",
    "age": 67,
    "gender": "Male",
    "mrn": "984210-A"
  },
  "document_type": "Discharge Summary",
  "chief_complaint": "Shortness of breath, productive cough, and high-grade fever",
  "diagnoses": [
    "Community Acquired Pneumonia (Right Lower Lobe)",
    "Essential Hypertension"
  ],
  "allergies": [
    "Penicillin"
  ],
  "medications": [
    {
      "name": "Amoxicillin",
      "dose": "500 mg",
      "frequency": "PO three times daily",
      "route": "Oral",
      "status": "Active"
    }
  ],
  "lab_results": [
    {
      "test_name": "WBC Count",
      "value": "15.2",
      "unit": "K/uL",
      "reference_range": "4.0 - 11.0 K/uL",
      "status": "HIGH",
      "confidence": 0.96,
      "evidence": "WBC Count: 15.2 K/uL (Reference Range: 4.0 - 11.0 K/uL) [HIGH]"
    }
  ],
  "risk_flags": [
    {
      "severity": "HIGH",
      "issue": "Leukocytosis (Elevated WBC: 15.2 K/uL)",
      "evidence": "WBC Count: 15.2 K/uL [HIGH]",
      "confidence": 0.99,
      "source": "Deterministic Rule Engine (WBC > 11.0)"
    },
    {
      "severity": "HIGH",
      "issue": "CRITICAL SAFETY CONTRAINDICATION: Beta-Lactam / Penicillin Allergy & Medication Overlap",
      "evidence": "Allergies: Penicillin | Medications: Amoxicillin",
      "confidence": 1.0,
      "source": "Deterministic Safety Rule Engine"
    }
  ],
  "summary": "Patient John Doe, a 67-year-old male, was admitted with shortness of breath and fever...",
  "recommended_next_step": "Urgent clinical review recommended due to elevated WBC (15.2 K/uL) and CRP (82 mg/L). Verify penicillin allergy status prior to dispensing amoxicillin."
}
```

---

## 🏛️ Project Directory Structure

```
clinical-document-intelligence/
├── app.py                          # Streamlit Clinical Dashboard (Main UI)
├── config.py                       # Provider & Environment Configuration
├── models/
│   └── clinical_models.py          # Pydantic Schemas
├── services/
│   ├── document_processor.py       # PDF/TXT/Image Ingestion Service
│   ├── clinical_ai.py              # LLM Structured Extraction Service
│   └── risk_analyzer.py            # Deterministic Clinical Risk Engine
├── prompts/
│   └── clinical_extraction.txt     # System Prompt Instructions
├── sample_data/                    # Sample PDFs and Text Documents
├── slides/
│   ├── build_deck.py               # Presentation PDF generator
│   └── summary_deck.pdf            # 5-Slide PDF Presentation
├── requirements.txt
├── README.md                       # This File
└── DEMO_SCRIPT.md                  # 3-Minute Presentation Transcript
```

---

## 🔮 Future Enhancements (Roadmap)

- **FHIR R4 Integration**: Direct JSON export formatted as `Patient`, `Observation`, and `MedicationRequest` FHIR resources.
- **EHR Direct Connect**: OAuth2 integration with Epic, Cerner, and AthenaHealth API endpoints.
- **Clinician Review Loop**: 1-click "Approve / Edit Flag" workflow for clinical governance and auditing.
