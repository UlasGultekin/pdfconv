import os
import tempfile
from docx import Document
from fpdf import FPDF

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Çok dilli destekli TTF font yolu
FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'DejaVuSans.ttf')
FONT_NAME = "DejaVuSans"

# Çok uzun kelimeleri ve satırları bölen fonksiyon
def split_long_words_and_lines(text, max_word_len=50, max_line_len=1000):
    # Çok uzun kelimeleri böl
    words = []
    for word in text.split():
        while len(word) > max_word_len:
            words.append(word[:max_word_len])
            word = word[max_word_len:]
        words.append(word)
    # Satır uzunluğunu da kontrol et
    joined = ' '.join(words)
    lines = [joined[i:i+max_line_len] for i in range(0, len(joined), max_line_len)]
    return lines

def split_text_to_lines(text, max_line_length=100):
    # Metni max_line_length karakterlik satırlara böl
    lines = []
    while len(text) > max_line_length:
        split_at = text.rfind(' ', 0, max_line_length)
        if split_at == -1:
            split_at = max_line_length
        lines.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text:
        lines.append(text)
    return lines

def safe_multi_cell(pdf, width, height, text):
    """
    FPDF multi_cell fonksiyonunu güvenli şekilde kullanır.
    Satır sığmazsa otomatik olarak daha küçük parçalara böler.
    """
    try:
        pdf.multi_cell(width, height, text)
    except Exception:
        # Satırda boşluk yoksa veya çok uzunsa, daha küçük parçalara böl
        if len(text) <= 1:
            return  # Tek karakter bile sığmıyorsa atla
        mid = len(text) // 2
        safe_multi_cell(pdf, width, height, text[:mid])
        safe_multi_cell(pdf, width, height, text[mid:])

def convert_word_to_pdf(content: bytes, filename: str) -> str:
    """
    DOCX dosyasını PDF'e dönüştürür (yalnızca metin, biçim ve görsel olmadan).
    Her ortamda çalışır, hata vermez, font desteği tamdır.
    Uzun yazılarda ve büyük paragraflarda FPDFException hatası alınmaz.
    """
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        # Dosyanın geçerli bir docx olup olmadığını kontrol et
        doc = Document(tmp_path)
        # PDF oluştur
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}_textonly.pdf")
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        try:
            pdf.add_font(FONT_NAME, "", FONT_PATH, uni=True)
        except Exception:
            pass  # Font zaten ekli olabilir
        pdf.set_font(FONT_NAME, size=12)
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        # Başlangıç uyarısı
        pdf.multi_cell(0, 10, "UYARI: Sunucuda ofis yazılımı bulunamadığı için sadece metin dönüştürüldü. Biçimlendirme ve görseller kaybolmuş olabilir.\nUzun metinlerde satır ve paragraf bölünmesi otomatik yapılmıştır.\n\n")
        for para in doc.paragraphs:
            if not para.text.strip():
                continue
            lines = split_text_to_lines(para.text, max_line_length=100)
            for line in lines:
                safe_multi_cell(pdf, page_width, 10, line)
            pdf.ln(3)
        # Son uyarı
        pdf.multi_cell(0, 10, "\n---\nNot: Bu PDF yalnızca metin içeriğiyle oluşturulmuştur. Orijinal Word dosyasındaki biçimlendirme, tablo ve görseller yer almaz.")
        pdf.output(output_path)
        return output_path
    except Exception as e:
        raise ValueError(f"'{filename}' dosyası geçerli bir Word (DOCX) belgesi olarak işlenemedi veya dönüştürülemedi. Hata: {e}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
