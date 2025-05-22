# tools/document_summarizer.py
import os
from agents.gemini_api import generate_content

def extract_text_from_pdf(pdf_path: str) -> str:
    import fitz  # PyMuPDF
    text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)

def extract_text_from_docx(docx_path: str) -> str:
    from docx import Document
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following text:\n\n{text}"
    # Gemini summaries should be concise
    return generate_content(prompt)

def summarize_document(file_path: str) -> str:
    """
    Reads a TXT, PDF, or DOCX file and returns a summary.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        return "Unsupported file type."

    if not text:
        return "Could not extract text from the document."

    # Use Gemini to summarize the extracted text
    return summarize_text(text)
