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

    # 1. Laboratory Threshold Checks
    for lab in summary.lab_results:
        clean_name = lab.test_name.upper().strip()
        val_match = re.search(r"(\d+(\.\d+)?)", str(lab.value))
        
        if not val_match:
            continue
            
        num_val = float(val_match.group(1))

        # WBC Check
        if "WBC" in clean_name or "WHITE BLOOD" in clean_name:
            if num_val > 11.0:
                lab.status = "HIGH"
                new_risk_flags.append(
                    RiskFlag(
                        severity="HIGH",
                        issue=f"Leukocytosis (Elevated WBC: {lab.value} {lab.unit or 'K/uL'})",
                        evidence=lab.evidence or f"WBC: {lab.value} {lab.unit or ''}",
                        confidence=0.99,
                        source="Deterministic Rule Engine (WBC > 11.0)"
                    )
                )
            elif num_val < 4.0:
                lab.status = "LOW"
                new_risk_flags.append(
                    RiskFlag(
                        severity="HIGH",
                        issue=f"Leukopenia (Low WBC: {lab.value} {lab.unit or 'K/uL'})",
                        evidence=lab.evidence or f"WBC: {lab.value} {lab.unit or ''}",
                        confidence=0.99,
                        source="Deterministic Rule Engine (WBC < 4.0)"
                    )
                )

        # C-Reactive Protein (CRP) Check
        elif "CRP" in clean_name or "C-REACTIVE" in clean_name:
            if num_val > 10.0:
                lab.status = "HIGH"
                new_risk_flags.append(
                    RiskFlag(
                        severity="HIGH",
                        issue=f"Severe Systemic Inflammation (CRP: {lab.value} {lab.unit or 'mg/L'})",
                        evidence=lab.evidence or f"CRP: {lab.value} {lab.unit or ''}",
                        confidence=0.99,
                        source="Deterministic Rule Engine (CRP > 10.0 mg/L)"
                    )
                )

        # Hemoglobin (Hb) Check
        elif "HEMOGLOBIN" in clean_name or "HB" in clean_name or "HGB" in clean_name:
            if num_val < 10.0:
                lab.status = "LOW"
                new_risk_flags.append(
                    RiskFlag(
                        severity="MEDIUM",
                        issue=f"Anemia / Low Hemoglobin ({lab.value} {lab.unit or 'g/dL'})",
                        evidence=lab.evidence or f"Hemoglobin: {lab.value} {lab.unit or ''}",
                        confidence=0.98,
                        source="Deterministic Rule Engine (Hb < 10.0 g/dL)"
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
