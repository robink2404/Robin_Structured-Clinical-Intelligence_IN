"""
Additional Sample Clinical Datasets Generator.
Creates 3 new diverse clinical scenarios for testing:
1. Cardiology Emergency Note (Acute Chest Pain / Troponin elevation / Sulfa allergy)
2. Pediatric Urgent Care Note (High fever / Otitis Media / Weight-based dosage)
3. Oncology Post-Chemo Lab Report (Severe Neutropenia WBC 1.8 / Low Platelets)
"""

import fitz
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent


CARDIOLOGY_TEXT = """ST. VINCENT CARDIOLOGY CONSULTATION REPORT
Date: November 02, 2024 | Location: Cardiac Care Unit (CCU)

PATIENT DEMOGRAPHICS
Name: Michael Chang
Age: 58 | Gender: Male | MRN: CCU-882194
Consulting Physician: Dr. Sarah Jenkins, MD (Cardiology)

REASON FOR CONSULTATION
STAT Cardiology evaluation for acute onset substernal chest pressure (8/10 severity) radiating to jaw, accompanied by diaphoresis and dyspnea.

PAST MEDICAL HISTORY
1. Type 2 Diabetes Mellitus (15 years)
2. Hyperlipidemia
3. Coronary Artery Disease (s/p PCI with drug-eluting stent in 2020)

ALLERGIES
Sulfa Drugs (Anaphylaxis documented in 2016)

VITAL SIGNS & CLINICAL EXAM
BP: 168/98 mmHg | HR: 110 bpm | RR: 24/min | SpO2: 93% on room air | Temp: 98.8 F

STAT LABORATORY & DIAGNOSTIC FINDINGS
- Cardiac Troponin I: 0.85 ng/mL (Reference Range: 0.00 - 0.04 ng/mL) [CRITICAL HIGH]
- Glucose (Fasting): 210 mg/dL (Reference Range: 70 - 99 mg/dL) [HIGH]
- B-Type Natriuretic Peptide (BNP): 680 pg/mL (Reference Range: <100 pg/mL) [HIGH]
- ECG: 2mm ST-segment elevation in leads V2-V4 consistent with Acute Anterior STEMI.

DISCHARGE / TRANSFER MEDICATIONS
1. Aspirin 325 mg PO immediately
2. Heparin IV drip protocol
3. Atorvastatin 80 mg PO daily
4. Trimethoprim-Sulfamethoxazole (Bactrim) DS 1 tab PO daily (Note: Check allergy profile)

RECOMMENDED NEXT STEPS & CLINICAL PLAN
1. Emergency Cardiac Catheterization / Primary PCI immediately.
2. Transfer to Cardiac Intensive Care Unit (CICU).
3. Contraindication alert: Cancel Bactrim prescription due to severe Sulfa allergy.
"""

PEDIATRIC_TEXT = """SUNSHINE PEDIATRIC URGENT CARE NOTE
Date: November 05, 2024 | Department: Pediatrics

PATIENT DEMOGRAPHICS
Name: Tommy Vance
Age: 6 | Gender: Male | Weight: 22 kg | MRN: PED-44102
Parent/Guardian: Lisa Vance (Mother)

CHIEF COMPLAINT & HISTORY OF PRESENT ILLNESS
6-year-old male brought in by mother with severe right ear pain (otalgia), pulling at ear, irritability, and high fever (103.1 F) for 48 hours. Reduced oral intake.

ALLERGIES
Peanuts (Severe Anaphylaxis - carries EpiPen)
No Known Drug Allergies (NKDA)

PHYSICAL EXAMINATION
Vitals: Temp 103.1 F | HR 122 bpm | RR 26/min | SpO2 98% room air
ENT: Right tympanic membrane is bulging, erythematous, with clouding and purulent fluid behind membrane. Left TM clear.
Oropharynx: Moist mucous membranes, no exudates.

LABORATORY FINDINGS
- WBC Count: 18.5 K/uL (Reference Range: 4.5 - 13.5 K/uL for pediatrics) [HIGH]
- C-Reactive Protein (CRP): 42.0 mg/L (Reference Range: 0.0 - 5.0 mg/L) [HIGH]

ASSESSMENT / DIAGNOSIS
1. Acute Suppurative Otitis Media (Right Ear)
2. High-grade Pediatric Pyrexia

DISCHARGE MEDICATIONS & PLAN
1. Amoxicillin-Clavulanate (Augmentin) 600 mg/5 mL suspension: 9 mL PO twice daily for 10 days.
2. Children's Ibuprofen 100 mg/5 mL: 10 mL PO every 6 hours as needed for fever/pain.
3. Strict instructions: Avoid all peanut products. Follow up with Pediatrician in 5 days.
"""

ONCOLOGY_TEXT = """HOPE CANCER CENTER - LAB & CHEMOTHERAPY MONITORING REPORT
Date: November 10, 2024 | Department: Hematology / Oncology

PATIENT INFORMATION
Name: Eleanor Rigby
Age: 62 | Gender: Female | MRN: ONC-774102
Attending Oncologist: Dr. Marcus Vance, MD

CLINICAL CONTEXT
Day 10 Post-Cycle 3 Chemotherapy (AC-T regimen for Stage II Breast Cancer). Patient reports fatigue, chills, and oral mucositis.

LABORATORY RESULTS (STAT CBC & DIFFERENTIAL)
Test Name                 Result      Units     Reference Range   Status
------------------------------------------------------------------------
WBC Count                 1.8         K/uL      4.0 - 11.0        CRITICAL LOW
Absolute Neutrophils(ANC) 450         /uL       1500 - 8000       CRITICAL LOW
Platelet Count            45          K/uL      150 - 450         CRITICAL LOW
Hemoglobin (Hb)           8.2         g/dL      12.0 - 16.0       LOW
Hematocrit                24.5        %         36.0 - 46.0       LOW
Temperature               101.4       F         97.0 - 99.0       HIGH

ONCOLOGY IMPRESSION & RISK FLAGS
1. FEBRILE NEUTROPENIA (ANC < 500 /uL + Temp > 101 F): HIGH RISK FOR SEVERE INFECTION.
2. THROMBOCYTOPENIA (Platelets 45 K/uL): HIGH BLEEDING RISK.
3. MODERATE CHEMOTHERAPY-INDUCED ANEMIA (Hb 8.2 g/dL).

RECOMMENDED URGENT ACTIONS
1. STAT Admission to Inpatient Oncology Unit for IV empiric broad-spectrum antibiotics (Cefepime).
2. Filgrastim (G-CSF) 300 mcg SC daily injection to stimulate neutrophil recovery.
3. Hold next chemotherapy cycle until ANC > 1500 /uL and Platelets > 100 K/uL.
"""


def create_pdf(filename: Path, text: str, title: str):
    """Generate clean clinical PDF using PyMuPDF."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4
    rect = fitz.Rect(40, 40, 555, 800)
    full_content = f"{title}\n{'=' * len(title)}\n\n{text}"
    page.insert_textbox(rect, full_content, fontsize=10, fontname="helv")
    doc.save(str(filename))
    doc.close()


def main():
    # Save TXT
    (SAMPLE_DIR / "cardiology_consultation.txt").write_text(CARDIOLOGY_TEXT, encoding="utf-8")
    (SAMPLE_DIR / "pediatric_intake.txt").write_text(PEDIATRIC_TEXT, encoding="utf-8")
    (SAMPLE_DIR / "oncology_chemo_lab.txt").write_text(ONCOLOGY_TEXT, encoding="utf-8")

    # Save PDF
    create_pdf(SAMPLE_DIR / "cardiology_consultation.pdf", CARDIOLOGY_TEXT, "ST. VINCENT CARDIOLOGY CONSULTATION REPORT")
    create_pdf(SAMPLE_DIR / "pediatric_intake.pdf", PEDIATRIC_TEXT, "SUNSHINE PEDIATRIC URGENT CARE NOTE")
    create_pdf(SAMPLE_DIR / "oncology_chemo_lab.pdf", ONCOLOGY_TEXT, "HOPE CANCER CENTER - STAT LAB MONITORING")

    print("Additional clinical sample datasets created successfully!")


if __name__ == "__main__":
    main()
