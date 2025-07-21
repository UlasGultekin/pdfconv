import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import tempfile
import os
import fitz  # PyMuPDF

# Çıktı klasörünü belirle ve oluştur
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Font yolu ve adı
FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'DejaVuSans.ttf')
FONT_NAME = "DejaVuSans"

# Fontu kaydet
if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

def convert_csv_to_pdf(content: bytes, filename: str) -> str:
    tmp_path = None
    try:
        # Geçici olarak CSV dosyası yaz
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='wb') as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        # CSV içeriğini oku
        df = pd.read_csv(tmp_path, encoding='utf-8')
        data = [df.columns.tolist()] + df.values.tolist()

        # Çıktı PDF dosya yolu
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.pdf")

        # PDF döküman oluştur
        doc = SimpleDocTemplate(output_path, pagesize=letter)

        # Tablo oluştur ve fontu uygula
        table = Table(data)
        style = TableStyle([
            ('FONT_NAME', (0, 0), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # PDF'e yaz
        doc.build([table])
        
    finally:
        # Geçici CSV dosyasını sil
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
            
    return output_path

def convert_pdf_to_csv(content: bytes, filename: str) -> str:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)
        
        # Her sayfadaki tabloları bul ve birleştir
        all_tables = []
        for page in doc:
            tables = page.find_tables()
            for table in tables:
                all_tables.extend(table.extract())

        if not all_tables:
            # Tablo bulunamazsa, düz metin çıkarma yöntemini kullan
            text = ""
            for page in doc:
                text += page.get_text()
            lines = [line.strip().split() for line in text.splitlines() if line.strip()]
            df = pd.DataFrame(lines)
        else:
            # İlk satırı başlık olarak kullan
            df = pd.DataFrame(all_tables[1:], columns=all_tables[0])
            
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.csv")
    df.to_csv(output_path, index=False, encoding='utf-8')

    return output_path
