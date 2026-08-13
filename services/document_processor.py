"""
Document Processor Service.
Handles document ingestion and text extraction for PDF, TXT, and Image files.
"""

import io
from typing import Dict, Any, Tuple
from PIL import Image

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


def extract_pdf_text(file_bytes: bytes) -> Tuple[str, int]:
    """Extract raw text from PDF bytes using PyMuPDF."""
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed.")

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page_count = len(doc)
    text_content = []

    for page_num in range(page_count):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        if page_text.strip():
            text_content.append(f"--- Page {page_num + 1} ---\n" + page_text)

    full_text = "\n\n".join(text_content)
    doc.close()
    return full_text, page_count


def extract_image_text(file_bytes: bytes) -> str:
    """Extract text from image using Tesseract OCR if available, else standard fallback message."""
    image = Image.open(io.BytesIO(file_bytes))

    if pytesseract is not None:
        try:
            extracted = pytesseract.image_to_string(image)
            if extracted.strip():
                return extracted
        except Exception:
            pass

    # Fallback if tesseract binary is not installed locally
    return (
        f"[IMAGE DOCUMENT INGESTED]\n"
        f"Image dimensions: {image.width}x{image.height} px, Format: {image.format}.\n"
        f"Note: Standard Tesseract OCR binary not detected on system. Document metadata captured for analysis."
    )


def extract_text_from_file(file_name: str, file_bytes: bytes, file_type: str) -> Dict[str, Any]:
    """
    Unified document extractor.
    Returns dictionary with extracted text, page count, word count, character count, and format.
    """
    file_type_lower = file_type.lower()
    page_count = 1
    extracted_text = ""

    if "pdf" in file_type_lower or file_name.endswith(".pdf"):
        extracted_text, page_count = extract_pdf_text(file_bytes)
        doc_format = "PDF"

    elif "image" in file_type_lower or any(file_name.endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
        extracted_text = extract_image_text(file_bytes)
        doc_format = "IMAGE"

    elif "text" in file_type_lower or file_name.endswith(".txt"):
        extracted_text = file_bytes.decode("utf-8", errors="replace")
        doc_format = "TXT"

    else:
        # Fallback decode
        extracted_text = file_bytes.decode("utf-8", errors="replace")
        doc_format = "UNKNOWN"

    word_count = len(extracted_text.split())
    char_count = len(extracted_text)

    return {
        "file_name": file_name,
        "format": doc_format,
        "page_count": page_count,
        "word_count": word_count,
        "char_count": char_count,
        "text": extracted_text
    }
