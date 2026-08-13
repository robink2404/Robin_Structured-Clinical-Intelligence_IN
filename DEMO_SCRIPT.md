# 🎥 3-Minute Video Presentation & Demo Script

**Project Title:** Clinical Document Intelligence Hub  
**Speaker:** Developer / Presenter  
**Target Duration:** 3 Minutes (180 Seconds)  
**Live AI Provider Used:** Google Gemini 2.5 Flash API  

---

## ⏱️ Timeline Breakdown

| Time | Slide / Screen | Core Message / Talking Points |
| :--- | :--- | :--- |
| **0:00 - 0:35** | Slide 1 (Problem & Context) | **Healthcare Manual Burden**: "Clinicians and admin teams spend thousands of hours manually reviewing unstructured clinical notes. Extraction is slow, error-prone, and inconsistent." |
| **0:35 - 1:05** | Slide 2 (Architecture & Hybrid AI) | **System Workflow**: "Our solution ingests PDFs, TXTs, or Images, uses Google Gemini LLM API with Pydantic schema validation, and passes extracted facts through a deterministic safety risk engine." |
| **1:05 - 2:20** | Live Streamlit Dashboard (`http://localhost:8501`) | **Live Gemini Demo Walkthrough**: Select **Gemini AI Provider**, enter **Gemini API Key**, upload Discharge Summary PDF, highlight **John Carter**'s card, **Risk Flags** with confidence & evidence quotes, **Diagnoses & Meds**, **Lab Table**, and **Raw JSON**. |
| **2:20 - 2:45** | Slide 4 (Challenges & Scoping) | **Safety & Hybrid Precision**: "We combined LLM semantic extraction for narrative text with deterministic Python code rules for hard lab thresholds and allergy contraindications." |
| **2:45 - 3:00** | Slide 5 (Conclusion & Next Steps) | **Roadmap**: "The prototype is zero-downtime and evaluation-ready. Next steps include FHIR R4 API integration, Epic/Cerner EHR connectivity, and clinician review workflows." |

---

## 📜 Full Presentation Script Transcript

### 🎙️ [0:00 - 0:35] Introduction & Problem Statement
*(Screen showing Slide 1: Problem Understanding & Objective)*

> "Hello everyone. Today I am presenting the **Clinical Document Intelligence Hub** — an AI prototype designed to streamline unstructured clinical document processing in healthcare.
> 
> Healthcare providers and administrative staff spend significant time manually reviewing patient documents — intake forms, discharge summaries, and lab reports — to extract key information. This manual review is slow, inconsistent, and prone to clinical errors. Our objective is to transform this fragmented data into decision-ready, structured intelligence within seconds."

---

### 🎙️ [0:35 - 1:05] Solution Architecture & Design Flow
*(Screen showing Slide 2: Solution Architecture & Design Flow)*

> "To solve this challenge, we built a hybrid AI processing pipeline.
> 
> The application ingests clinical documents in PDF, TXT, or Image format. The text is processed by a Clinical LLM API — such as **Google Gemini 2.5** — strictly constrained by validated Pydantic JSON schemas. 
> 
> Crucially, extracted clinical facts are then evaluated by a **Deterministic Risk Engine** that checks laboratory thresholds — like WBC count over 11.0 or CRP over 10 — and flags safety contraindications, such as drug-allergy overlaps."

---

### 🎙️ [1:05 - 2:20] Live Application Demo (Google Gemini AI)
*(Switch screen to active Streamlit application at `http://localhost:8501`)*

> "Now, let's see the application operating live in real-time.
> 
> In the sidebar under **AI Processing Engine**, I select **Gemini (Google Gemini 2.5)** as our active provider and enter our **Gemini API Key**.
> 
> Next, I upload an inpatient **Discharge Summary PDF**. As soon as processing completes, the **Structured Clinical Intelligence Dashboard** populates:
> 
> 1. **Patient Card**: Instantly surfaces **John Carter**, a **67-year-old male**, MRN **SYN-1001**.
> 
> 2. **Risk Flags Tab**: Notice the high-priority risk callouts:
>    - 🔴 **[HIGH] Penicillin allergy** *(100% Confidence)* with exact source evidence: *'Penicillin — rash reported previously'*.
>    - 🔴 **[HIGH] Leukocytosis (Elevated WBC: 15.2 K/uL)** *(99% Confidence)* flagged by the **Deterministic Rule Engine**.
>    - 🔴 **[HIGH] Severe Systemic Inflammation (CRP: 82 mg/L)** *(99% Confidence)*.
>    - 🟠 **[MEDIUM] Mild hypoxemia on room air** *(90% Confidence)* supported by *'Oxygen Saturation 93% on room air'*.
> 
> 3. **Diagnoses & Meds Tab**: Surfaces confirmed diagnoses of **Community Acquired Pneumonia** and **Hypertension**, allergy warning for **Penicillin**, and prescribed meds: **Azithromycin 500 mg**, **Paracetamol 500 mg**, and **Amlodipine 5 mg**.
> 
> 4. **Lab Findings Tab**: Formats extracted lab values cleanly in a table showing **WBC 15.2 K/uL [HIGH]**, **CRP 82 mg/L [HIGH]**, **Oxygen Saturation 93% [LOW]**, **Hemoglobin 13.4 g/dL**, and **Creatinine 1.0 mg/dL**.
> 
> 5. **Raw JSON Tab**: Provides 1-click export of the validated Pydantic JSON payload for downstream EHR integration."

---

### 🎙️ [2:20 - 2:45] Technical Highlights & Challenges
*(Screen showing Slide 4: Challenges & Learnings)*

> "A major architectural decision was our **hybrid reasoning model**.
> 
> We used the LLM for flexible narrative text extraction and evidence quotes, but paired it with deterministic Python code rules for high-stakes medical thresholds. This guarantees zero hallucination for critical laboratory alerts. Every risk flag includes exact evidence quotes and confidence scores for total clinical auditability."

---

### 🎙️ [2:45 - 3:00] Conclusion & Roadmap
*(Screen showing Slide 5: Demo Summary & Next Steps)*

> "Our prototype features multi-provider support for OpenAI, Google Gemini, and an offline fallback engine.
> 
> Strategic next steps include FHIR R4 API export, direct EHR connectivity with Epic and Cerner, and clinician sign-off review loops. Thank you!"
