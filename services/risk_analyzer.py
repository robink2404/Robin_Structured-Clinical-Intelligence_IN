"""
Deterministic Risk Engine Service.
Applies deterministic medical rules and safety checks on extracted clinical data 
to identify high-risk conditions, abnormal lab thresholds, and drug-allergy contraindications.
"""

import re
from typing import List
from models.clinical_models import ClinicalSummary, RiskFlag, LabResult


def evaluate_deterministic_risks(summary: ClinicalSummary) -> ClinicalSummary:
    """
    Augments the extracted ClinicalSummary object with deterministic risk flags 
    and verifies laboratory abnormal status flags.
    """
    existing_flags = list(summary.risk_flags)
    new_risk_flags: List[RiskFlag] = []

    # 1. Laboratory Threshold Checks & Abnormal Lab Auto-Flagging
    for lab in summary.lab_results:
        clean_name = lab.test_name.upper().strip()
        val_match = re.search(r"(\d+(?:\.\d+)?)", str(lab.value))
        num_val = float(val_match.group(1)) if val_match else 0.0

        # Glucose Check
        if "GLUCOSE" in clean_name and num_val > 140:
            lab.status = "HIGH"
            new_risk_flags.append(
                RiskFlag(
                    severity="HIGH" if num_val > 200 else "MEDIUM",
                    issue=f"Fasting Hyperglycemia (Glucose: {lab.value} {lab.unit or 'mg/dL'})",
                    evidence=lab.evidence or f"Glucose: {lab.value} {lab.unit or ''}",
                    confidence=0.98,
                    source="Deterministic Rule Engine (Glucose > 140 mg/dL)"
                )
            )

        # Creatinine & Renal Check
        elif "CREATININE" in clean_name and num_val > 1.2:
            lab.status = "HIGH"
            new_risk_flags.append(
                RiskFlag(
                    severity="HIGH",
                    issue=f"Impaired Renal Function / Elevated Creatinine ({lab.value} {lab.unit or 'mg/dL'})",
                    evidence=lab.evidence or f"Creatinine: {lab.value} {lab.unit or ''}",
                    confidence=0.99,
                    source="Deterministic Rule Engine (Creatinine > 1.2 mg/dL)"
                )
            )

        # eGFR Check
        elif "EGFR" in clean_name and num_val < 60 and num_val > 0:
            lab.status = "LOW"
            new_risk_flags.append(
                RiskFlag(
                    severity="HIGH" if num_val < 30 else "MEDIUM",
                    issue=f"Reduced eGFR / Kidney Function Impairment (eGFR: {lab.value} {lab.unit or ''})",
                    evidence=lab.evidence or f"eGFR: {lab.value}",
                    confidence=0.98,
                    source="Deterministic Rule Engine (eGFR < 60)"
                )
            )

        # Cholesterol & LDL Check
        elif ("LDL" in clean_name or "CHOLESTEROL" in clean_name) and num_val > 130:
            lab.status = "HIGH"
            new_risk_flags.append(
                RiskFlag(
                    severity="MEDIUM",
                    issue=f"Hyperlipidemia / Elevated Lipids ({lab.test_name}: {lab.value} {lab.unit or ''})",
                    evidence=lab.evidence or f"{lab.test_name}: {lab.value}",
                    confidence=0.96,
                    source="Deterministic Rule Engine (Lipid Panel Threshold)"
                )
            )

        # WBC Check
        elif ("WBC" in clean_name or "WHITE BLOOD" in clean_name) and num_val > 0:
            if num_val > 11.0:
                lab.status = "HIGH"
                new_risk_flags.append(
                    RiskFlag(
                        severity="HIGH",
                        issue=f"Leukocytosis (Elevated WBC: {lab.value} {lab.unit or 'K/uL'})",
                        evidence=lab.evidence or f"WBC: {lab.value}",
                        confidence=0.99,
                        source="Deterministic Rule Engine (WBC > 11.0)"
                    )
                )
            elif num_val < 4.0:
                lab.status = "CRITICAL" if num_val < 2.0 else "HIGH"
                new_risk_flags.append(
                    RiskFlag(
                        severity="HIGH",
                        issue=f"Leukopenia / Neutropenia (Low WBC: {lab.value} {lab.unit or 'K/uL'})",
                        evidence=lab.evidence or f"WBC: {lab.value}",
                        confidence=0.99,
                        source="Deterministic Rule Engine (WBC < 4.0)"
                    )
                )

        # CRP Check
        elif ("CRP" in clean_name or "C-REACTIVE" in clean_name) and num_val > 10.0:
            lab.status = "HIGH"
            new_risk_flags.append(
                RiskFlag(
                    severity="HIGH",
                    issue=f"Severe Systemic Inflammation (CRP: {lab.value} {lab.unit or 'mg/L'})",
                    evidence=lab.evidence or f"CRP: {lab.value}",
                    confidence=0.99,
                    source="Deterministic Rule Engine (CRP > 10.0 mg/L)"
                )
            )

        # Hemoglobin Check
        elif ("HEMOGLOBIN" in clean_name or "HB" in clean_name or "HGB" in clean_name) and num_val > 0:
            if num_val < 11.5:
                lab.status = "LOW"
                new_risk_flags.append(
                    RiskFlag(
                        severity="MEDIUM",
                        issue=f"Anemia / Low Hemoglobin ({lab.value} {lab.unit or 'g/dL'})",
                        evidence=lab.evidence or f"Hemoglobin: {lab.value}",
                        confidence=0.98,
                        source="Deterministic Rule Engine (Hb < 11.5 g/dL)"
                    )
                )

        # Generic Abnormal Catch for any other HIGH or CRITICAL labs
        elif lab.status in ["HIGH", "CRITICAL", "LOW"]:
            new_risk_flags.append(
                RiskFlag(
                    severity="HIGH" if lab.status == "CRITICAL" else "MEDIUM",
                    issue=f"Abnormal Finding: {lab.test_name} ({lab.value} {lab.unit or ''} - {lab.status})",
                    evidence=lab.evidence or f"{lab.test_name}: {lab.value}",
                    confidence=0.95,
                    source="Deterministic Risk Engine"
                )
            )

    # 2. Drug-Allergy Interaction Check
    allergies_upper = [a.upper() for a in summary.allergies]
    meds_upper = [m.name.upper() for m in summary.medications]

    has_penicillin_allergy = any("PENICILLIN" in a or "AMOXICILLIN" in a or "BETA-LACTAM" for a in allergies_upper)
    prescribed_penicillin_family = any(
        any(pen in m for pen in ["AMOXICILLIN", "AMPICILLIN", "PENICILLIN", "AUGMENTIN"])
        for m in meds_upper
    )

    if has_penicillin_allergy and prescribed_penicillin_family:
        new_risk_flags.append(
            RiskFlag(
                severity="HIGH",
                issue="CRITICAL SAFETY CONTRAINDICATION: Beta-Lactam / Penicillin Allergy & Medication Overlap",
                evidence=f"Allergies: {', '.join(summary.allergies)} | Medications: {', '.join([m.name for m in summary.medications])}",
                confidence=1.00,
                source="Deterministic Safety Rule Engine"
            )
        )

    # De-duplicate risk flags by issue title
    combined = existing_flags + new_risk_flags
    unique_flags = {}
    for flag in combined:
        if flag.issue not in unique_flags:
            unique_flags[flag.issue] = flag

    summary.risk_flags = list(unique_flags.values())
    return summary
