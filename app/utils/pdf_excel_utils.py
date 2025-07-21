import os
import tempfile
import pandas as pd
import fitz  # PyMuPDF

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Çıktı klasörünü belirle ve oluştur
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Font yolu ve adı
FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'DejaVuSans.ttf')
FONT_NAME = "DejaVuSans"

# Fontu kaydet
if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def convert_pdf_to_excel(content: bytes, filename: str) -> str:
    """PDF -> Excel (çok dilli destekli ve tablo tanıma)"""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)
        
        all_tables = []
        for page in doc:
            tables = page.find_tables()
            for table in tables:
                all_tables.extend(table.extract())

        if not all_tables:
            text = ""
            for page in doc:
                text += page.get_text()
            rows = [line.strip().split() for line in text.strip().split("\\n") if line.strip()]
            df = pd.DataFrame(rows)
        else:
            df = pd.DataFrame(all_tables[1:], columns=all_tables[0])
            
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.xlsx")
    df.to_excel(output_path, index=False)
    
    return output_path


def convert_excel_to_pdf(content: bytes, filename: str) -> str:
    """Excel -> PDF (çok dilli fontla)"""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        df = pd.read_excel(tmp_path, engine='openpyxl')
        
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    data = [df.columns.tolist()] + df.values.tolist()

    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.pdf")

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    
    # Veriyi string'e çevir
    data = [[str(cell) for cell in row] for row in data]
    
    table = Table(data)

    # PDF içinde çok dilli yazım için font ve stil desteği
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table.setStyle(style)

    doc.build([table])
    return output_path
