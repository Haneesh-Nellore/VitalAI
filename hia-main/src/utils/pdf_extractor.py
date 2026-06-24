import pdfplumber
import streamlit as st
from config.app_config import MAX_PDF_PAGES


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file — no strict medical content validation."""
    try:
        # Check file size
        file_size_mb = pdf_file.size / (1024 * 1024)
        if file_size_mb > MAX_PDF_PAGES:
            return f"File size ({file_size_mb:.1f}MB) exceeds the limit."

        # Check file type
        if pdf_file.type != "application/pdf":
            return "Invalid file type. Please upload a PDF file."

        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            if len(pdf.pages) > MAX_PDF_PAGES:
                return f"PDF exceeds maximum page limit of {MAX_PDF_PAGES} pages."

            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        if len(text.strip()) < 50:
            return "Could not extract text from this PDF. Please ensure it is not a scanned image."

        return text

    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"
