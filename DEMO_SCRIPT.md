# 🎥 3-Minute Video Presentation & Demo Script

**Project Title:** Clinical Document Intelligence Hub  
**Speaker:** Developer / Presenter  
**Target Duration:** 3 Minutes (180 Seconds)  

---

## ⏱️ Timeline Breakdown

| Time | Slide / Screen | Core Message / Talking Points |
| :--- | :--- | :--- |
| **0:00 - 0:30** | Slide 1 (Problem) | **Context & Problem Statement**: "Healthcare providers spend thousands of hours manually reading unstructured discharge summaries and lab reports. Data extraction is slow, inconsistent, and error-prone." |
| **0:30 - 1:00** | Slide 2 (Architecture) | **Architecture & Hybrid Design**: "We built a solution using PyMuPDF for document parsing, LLM prompt engineering with Pydantic for structured JSON extraction, and a deterministic safety risk engine for critical lab thresholds and drug allergy checks." |
| **1:00 - 2:15** | Live App Demo (`app.py`) | **Live System Walkthrough**: Upload document, showcase Patient Card, highlight 🔴 High Risk Flags with confidence scores (99%) & evidence quotes, point out Lab Results table, and demonstrate 1-click JSON export. |
| **2:15 - 2:45** | Slide 4 (Challenges) | **Key Technical Decisions & Trade-offs**: "We deliberately didn't delegate every decision to the LLM. We combined LLMs for unstructured narrative parsing with deterministic code rules for high-stakes medical thresholds to prevent hallucination." |
| **2:45 - 3:00** | Slide 5 (Next Steps) | **Conclusion & Roadmap**: "Our prototype is ready out-of-the-box. Next steps include FHIR R4 interoperability, EHR integration with Epic/Cerner, and clinician review workflows." |

---

## 📜 Full Script Transcript

### 🎙️ [0:00 - 0:30] Introduction & Problem
> "Hello everyone. Today I'm presenting the **Clinical Document Intelligence Hub** — an AI prototype designed to solve a critical operational bottleneck in healthcare.
> 
> Healthcare providers spend significant time manually reviewing patient documents — intake forms, discharge summaries, and lab reports — to extract key information. This manual process is slow, inconsistent, and prone to costly clinical errors."

### 🎙️ [0:30 - 1:00] Solution Architecture
> "To address this, we developed a working end-to-end prototype.
> 
> Our system architecture follows a clean pipeline: Unstructured documents in PDF, Image, or Text format are ingested via PyMuPDF. The text is processed by a Clinical LLM constrained strictly by Pydantic JSON schemas. 
> 
> Crucially, extracted facts are then passed through a **Deterministic Risk Engine** that checks laboratory thresholds — such as WBC count above 11 — and flags critical safety contraindications, like prescribing Penicillin antibiotics to a patient with a documented Penicillin allergy."

### 🎙️ [1:00 - 2:15] Live Application Demo
> *(Switch screen to active Streamlit application at `http://localhost:8501`)*
> 
> "Let's see the application in action.
> 
> On the left, we can load a sample **Inpatient Discharge Summary PDF**. On the right, the Clinical Intelligence Dashboard immediately extracts structured patient data — John Doe, 67, Male, MRN 984210.
> 
> Under **Risk Flags**, notice how the system flags two critical warnings: First, Leukocytosis with 99% confidence, supported by the exact evidence quote from the document: *'WBC Count: 15.2 K/uL'*. Second, a **CRITICAL Drug-Allergy Warning** because Amoxicillin was prescribed to a Penicillin-allergic patient.
> 
> In the **Lab Findings** tab, lab values are automatically formatted with reference ranges and HIGH/LOW badges. Finally, under **Executive Summary**, the system generates an actionable, decision-ready next step for the clinical team."

### 🎙️ [2:15 - 2:45] Technical Highlights & Challenges
> "One of our key architectural decisions was implementing a **hybrid reasoning model**.
> 
> We used the LLM for semantic extraction of unstructured narrative text, but used deterministic Python code for high-stakes medical rules. This guarantees predictable, non-hallucinated alerts for critical lab values and drug safety checks. 
> 
> To ensure total auditability, every extracted risk flag includes source text evidence quotes and confidence scores."

### 🎙️ [2:45 - 3:00] Conclusion & Roadmap
> "Our prototype includes multi-provider support for OpenAI, Google Gemini, and a zero-dependency fallback engine that runs offline out-of-the-box. 
> 
> Future enhancements include FHIR R4 API integration, EHR connectivity with Epic and Cerner, and clinician sign-off workflows. Thank you!"
