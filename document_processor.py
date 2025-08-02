# document_processor.py
import fitz  # PyMuPDF
import requests
from typing import List, Dict

def download_pdf(url: str, save_path: str = "temp_policy.pdf") -> str:
    """Downloads a PDF from a URL and saves it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
    except requests.RequestException as e:
        print(f"Error downloading PDF: {e}")
        return None

def extract_chunks(pdf_path: str) -> List[Dict]:
    """Extracts text chunks from a PDF, keeping paragraphs together."""
    doc = fitz.open(pdf_path)
    chunks = []
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        # Split text by paragraphs and filter out empty or whitespace-only strings
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for para in paragraphs:
            # Normalize newlines and multiple spaces within paragraphs
            normalized_text = ' '.join(para.replace('\n', ' ').split())
            chunks.append({
                "text": normalized_text,
                "metadata": {"page": page_num + 1}
            })
    return chunks