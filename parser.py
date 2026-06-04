import pdfplumber

def extract_text(pdf_file) -> str:
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join(
            page.extract_text() for page in pdf.pages
            if page.extract_text()
        )
    if not text.strip():
        raise ValueError("Could not extract text from this PDF. Try a text-based PDF, not a scanned image.")
    return text