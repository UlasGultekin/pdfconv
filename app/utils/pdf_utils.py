import os
import tempfile
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF


# Çok dilli destekli TTF font yolu (backend/fonts altında)
FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "fonts", "NotoSans-Regular.ttf")


def convert_pdf_to_text(content: bytes, filename: str) -> str:
    """PDF → TXT (Unicode destekli)"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    os.remove(tmp_path)

    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path


def convert_pdf_to_word(pdf_bytes: bytes, filename: str) -> str:
    """PDF → DOCX (Unicode destekli)"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    word_doc = Document()

    for page in doc:
        text = page.get_text()
        if text.strip():
            word_doc.add_paragraph(text.strip())

    output_path = f"{filename.rsplit('.', 1)[0]}.docx"
    word_doc.save(output_path)
    return output_path


def convert_text_to_pdf(content: bytes, filename: str) -> str:
    """TXT → PDF (Unicode destekli - TTF fontlu)"""
    text = content.decode("utf-8")
    base_name = filename.rsplit('.', 1)[0]
    output_path = f"{base_name}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # 🎯 NotoSans fontunu ekle
    pdf.add_font("NotoSans", "", FONT_PATH, uni=True)
    pdf.set_font("NotoSans", size=12)

    for line in text.splitlines():
        pdf.multi_cell(0, 10, txt=line)

    pdf.output(output_path)
    return output_path
