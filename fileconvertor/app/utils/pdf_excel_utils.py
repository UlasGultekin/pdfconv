import os
import tempfile
import pandas as pd
import fitz  # PyMuPDF

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Global font yolu (Tüm işletim sistemleri için uyumlu)
FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "fonts", "NotoSans-Regular.ttf")

# Raporlama için çok dilli font kaydı
pdfmetrics.registerFont(TTFont("NotoSans", FONT_PATH))


def convert_pdf_to_excel(content: bytes, filename: str) -> str:
    """PDF -> Excel (çok dilli destekli)"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Satırları ayır
    rows = [line.strip().split() for line in text.strip().split("\n") if line.strip()]
    df = pd.DataFrame(rows)

    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.xlsx"
    df.to_excel(output_path, index=False)

    os.remove(tmp_path)
    return output_path


def convert_excel_to_pdf(content: bytes, filename: str) -> str:
    """Excel -> PDF (çok dilli fontla)"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    df = pd.read_excel(tmp_path)
    data = [df.columns.tolist()] + df.values.tolist()

    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.pdf"

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    table = Table(data)

    # PDF içinde çok dilli yazım için font ve stil desteği
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table.setStyle(style)

    doc.build([table])
    os.remove(tmp_path)
    return output_path
