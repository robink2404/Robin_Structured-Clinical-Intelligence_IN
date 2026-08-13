"""
Sample Data Generator Script.
Creates realistic sample clinical documents (PDF and TXT) for testing and demonstration.
"""

from pathlib import Path
from fpdf import FPDF

SAMPLE_DIR = Path(__file__).parent
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


DISCHARGE_SUMMARY_TEXT = """PATIENT DISCHARGE SUMMARY
St. Jude Regional Medical Center
Department of Internal Medicine

PATIENT DEMOGRAPHICS
Patient Name: John Doe
Age: 67 | Gender: Male
MRN: 984210-A
Admission Date: October 14, 2024
Discharge Date: October 18, 2024

CHIEF COMPLAINT & ADMISSION REASON
Shortness of breath, productive cough, and high-grade fever (102.4 F) for 3 days prior to admission.

PAST MEDICAL HISTORY
1. Essential Hypertension (10 years, managed on Lisinopril)
2. Hyperlipidemia

ALLERGIES
Penicillin (Severe rash and hives documented in 2018)

DIAGNOSIS & DISPOSITION
Primary Diagnosis: Community Acquired Pneumonia (Right Lower Lobe)
Secondary Diagnosis: Essential Hypertension
Disposition: Discharged home in stable condition with outpatient follow-up.

LABORATORY & DIAGNOSTIC FINDINGS
- WBC Count: 15.2 K/uL (Reference Range: 4.0 - 11.0 K/uL) [HIGH]
- Hemoglobin: 13.4 g/dL (Reference Range: 12.0 - 16.0 g/dL) [NORMAL]
- C-Reactive Protein (CRP): 82.0 mg/L (Reference Range: 0.0 - 5.0 mg/L) [HIGH]
- Chest X-Ray: Right lower lobe alveolar consolidation consistent with bacterial pneumonia.

DISCHARGE MEDICATIONS
1. Amoxicillin 500 mg PO three times daily for 7 days (Note: Verify allergy status before dispensing)
2. Lisinopril 10 mg PO once daily
3. Acetaminophen 500 mg PO every 6 hours as needed for fever/pain

RECOMMENDED NEXT STEPS & DISCHARGE INSTRUCTIONS
1. Complete full 7-day course of antibiotic therapy.
2. Follow up with Primary Care Physician in 3 to 5 days.
3. Return to Emergency Department immediately if chest pain, severe dyspnea, or persistent fever (>101 F) occurs.
"""

LAB_REPORT_TEXT = """OUTPATIENT LABORATORY DIAGNOSTICS REPORT
Metro Diagnostic Laboratories
Report ID: LAB-2024-88419

PATIENT INFORMATION
Name: Jane Smith
Age: 52 | Gender: Female | DOB: 05/12/1972
Ordering Physician: Dr. Robert Vance, MD

COMPLETE BLOOD COUNT (CBC) & METABOLIC PANEL
Test Name           Result      Units     Reference Range   Status
------------------------------------------------------------------
WBC Count           16.8        K/uL      4.5 - 11.0        HIGH
RBC Count           4.10        M/uL      4.00 - 5.20       NORMAL
Hemoglobin          9.4         g/dL      12.0 - 16.0       LOW
Hematocrit          29.5        %         36.0 - 46.0       LOW
Platelets           240         K/uL      150 - 450         NORMAL
Glucose (Fasting)   142         mg/dL     70 - 99           HIGH
C-Reactive Protein  94.5        mg/L      0.0 - 5.0         CRITICAL

ALLERGY PROFILE
- Sulfa Drugs: Documented Moderate Anaphylactoid Reaction

PHYSICIAN IMPRESSION
Marked leukocytosis and systemic inflammatory markers with moderate normocytic anemia and fasting hyperglycemia. Urgent clinical correlation required.
"""

PHYSICIAN_NOTE_TEXT = """EMERGENCY DEPARTMENT PHYSICIAN PROGRESS NOTE
City General Hospital - ED Section 4

PATIENT: Robert Miller | AGE: 45 | GENDER: Male | MRN: 441029

SUBJECTIVE:
45-year-old male presents with acute onset sharp left-sided chest pain starting 2 hours ago during exercise. Pain radiates to left shoulder. Accompanied by diaphoresis and mild nausea. Denies fever or cough.

PAST MEDICAL HISTORY:
Type 2 Diabetes Mellitus, Hypercholesterolemia. No prior cardiac events.

ALLERGIES: No Known Drug Allergies (NKDA).

OBJECTIVE / PHYSICAL EXAM:
Vitals: BP 154/96 mmHg | HR 102 bpm | RR 22/min | SpO2 96% on room air | Temp 98.6 F
Cardiovascular: Tachycardic, regular rhythm, S1/S2 present, no murmurs.
Lungs: Clear to auscultation bilaterally.

ASSESSMENT:
1. Acute Chest Pain - Rule out Acute Coronary Syndrome (ACS) vs Severe Muscle Strain.
2. Uncontrolled Hypertension.

PLAN & NEXT STEPS:
1. STAT 12-lead ECG and serial Troponin I lab draws at 0 and 3 hours.
2. Aspirin 325 mg chewed immediately.
3. Sublingual Nitroglycerin as needed for chest discomfort.
4. Cardiology consultation requested.
"""


import fitz

def create_pdf(filename: Path, text: str, title: str):
    """Generate a clean clinical PDF document using PyMuPDF."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842) # A4 size
    rect = fitz.Rect(40, 40, 555, 800)
    
    full_content = f"{title}\n{'=' * len(title)}\n\n{text}"
    page.insert_textbox(rect, full_content, fontsize=10, fontname="helv")
    doc.save(str(filename))
    doc.close()


def main():
    # Save TXT files
    (SAMPLE_DIR / "discharge_summary.txt").write_text(DISCHARGE_SUMMARY_TEXT, encoding="utf-8")
    (SAMPLE_DIR / "lab_report.txt").write_text(LAB_REPORT_TEXT, encoding="utf-8")
    (SAMPLE_DIR / "physician_note.txt").write_text(PHYSICIAN_NOTE_TEXT, encoding="utf-8")

    # Generate PDF files
    create_pdf(SAMPLE_DIR / "discharge_summary.pdf", DISCHARGE_SUMMARY_TEXT, "ST. JUDE MEDICAL CENTER - DISCHARGE SUMMARY")
    create_pdf(SAMPLE_DIR / "lab_report.pdf", LAB_REPORT_TEXT, "METRO DIAGNOSTICS - CLINICAL LAB REPORT")
    create_pdf(SAMPLE_DIR / "physician_note.pdf", PHYSICIAN_NOTE_TEXT, "CITY GENERAL HOSPITAL - ED PROGRESS NOTE")

    print("Sample clinical documents created successfully!")


if __name__ == "__main__":
    main()
