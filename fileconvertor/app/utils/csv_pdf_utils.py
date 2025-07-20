import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib import fonts

import tempfile
import os

# Fontu register et
FONT_PATH = os.path.abspath("fileconvertor/app/fonts/NotoSans-Regular.ttf")
FONT_NAME = "NotoSans"
if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

def convert_csv_to_pdf(content: bytes, filename: str) -> str:
    # Geçici olarak CSV dosyası yaz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # CSV içeriğini oku
    df = pd.read_csv(tmp_path)
    data = [df.columns.tolist()] + df.values.tolist()

    # Çıktı PDF dosya yolu
    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.pdf"

    # PDF döküman oluştur
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    # Tablodaki her hücreye fontu uygula
    table = Table(data)
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # PDF'e yaz
    doc.build([table])

    # Geçici CSV dosyasını sil
    os.remove(tmp_path)
    return output_path

def convert_pdf_to_csv(content: bytes, filename: str) -> str:
    import fitz  # PyMuPDF

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Her satırı bölerek DataFrame'e aktar
    lines = [line.strip().split() for line in text.splitlines() if line.strip()]
    df = pd.DataFrame(lines)

    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.csv"
    df.to_csv(output_path, index=False)

    os.remove(tmp_path)
    return output_path
