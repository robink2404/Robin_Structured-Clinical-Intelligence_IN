"""
Pydantic Data Schemas for Clinical Document Intelligence.
Defines structured objects for patient demography, diagnoses, medications, 
lab results, risk flags, confidence scoring, and clinical recommendations.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PatientInfo(BaseModel):
    name: Optional[str] = Field(None, description="Full patient name if available, else None")
    age: Optional[int] = Field(None, description="Patient age in years")
    gender: Optional[str] = Field(None, description="Patient gender (Male, Female, Other, Unknown)")
    mrn: Optional[str] = Field(None, description="Medical Record Number / ID if present")


class Medication(BaseModel):
    name: str = Field(..., description="Medication generic or brand name")
    dose: Optional[str] = Field(None, description="Dosage amount e.g. 500 mg")
    frequency: Optional[str] = Field(None, description="Administration frequency e.g. 3 times daily")
    route: Optional[str] = Field(None, description="Route e.g. Oral, IV, Topical")
    status: Optional[str] = Field("Active", description="Medication status e.g. Active, Discontinued, New")


class LabResult(BaseModel):
    test_name: str = Field(..., description="Name of lab test e.g. WBC, Hemoglobin, CRP")
    value: str = Field(..., description="Numerical or text result value e.g. 15.2")
    unit: Optional[str] = Field(None, description="Measurement unit e.g. K/uL, g/dL, mg/L")
    reference_range: Optional[str] = Field(None, description="Normal reference range e.g. 4.0-11.0")
    status: str = Field("NORMAL", description="Evaluation: NORMAL, HIGH, LOW, or CRITICAL")
    confidence: float = Field(0.95, description="Extraction confidence score (0.0 to 1.0)")
    evidence: Optional[str] = Field(None, description="Exact text excerpt supporting this lab result")


class RiskFlag(BaseModel):
    severity: str = Field(..., description="Severity level: HIGH, MEDIUM, LOW")
    issue: str = Field(..., description="Short summary of the clinical issue or risk flag")
    evidence: str = Field(..., description="Exact textual evidence from document supporting this risk flag")
    confidence: float = Field(0.95, description="Confidence score from 0.0 to 1.0")
    source: str = Field("LLM Extraction", description="Origin: LLM Extraction or Deterministic Rule Engine")


class ClinicalSummary(BaseModel):
    patient: PatientInfo = Field(default_factory=PatientInfo)
    document_type: str = Field("Unspecified Clinical Note", description="Document type e.g. Discharge Summary, Lab Report, Physician Note")
    chief_complaint: Optional[str] = Field(None, description="Primary reason for visit or chief complaint")
    diagnoses: List[str] = Field(default_factory=list, description="List of confirmed or working diagnoses")
    medications: List[Medication] = Field(default_factory=list, description="List of documented medications")
    allergies: List[str] = Field(default_factory=list, description="List of documented patient allergies")
    lab_results: List[LabResult] = Field(default_factory=list, description="List of laboratory findings")
    risk_flags: List[RiskFlag] = Field(default_factory=list, description="Identified risk flags and clinical warnings")
    summary: str = Field(..., description="Comprehensive clinical narrative summary")
    recommended_next_step: str = Field(..., description="Actionable clinical decision support recommendation")
