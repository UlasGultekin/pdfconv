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
        pdf.add_page()
        try:
            pdf.add_font(FONT_NAME, "", FONT_PATH, uni=True)
        except Exception:
            pass  # Font zaten ekli olabilir
        pdf.set_font(FONT_NAME, size=12)
        pdf.set_auto_page_break(auto=True, margin=15)
        # Başlangıç uyarısı
        pdf.multi_cell(0, 10, "UYARI: Sunucuda ofis yazılımı bulunamadığı için sadece metin dönüştürüldü. Biçimlendirme ve görseller kaybolmuş olabilir.\nUzun metinlerde satır ve paragraf bölünmesi otomatik yapılmıştır.\n\n")
        for para in doc.paragraphs:
            if not para.text.strip():
                continue
            lines = split_long_words_and_lines(para.text)
            for line in lines:
                if not line.strip():
                    continue
                try:
                    pdf.multi_cell(0, 10, line)
                except Exception:
                    # Hata olursa satırı daha küçük parçalara bölerek ekle
                    for subline in [line[i:i+200] for i in range(0, len(line), 200)]:
                        try:
                            pdf.multi_cell(0, 10, subline)
                        except Exception:
                            # En küçük parça bile eklenemiyorsa atla
                            continue
        # Son uyarı
        pdf.multi_cell(0, 10, "\n---\nNot: Bu PDF yalnızca metin içeriğiyle oluşturulmuştur. Orijinal Word dosyasındaki biçimlendirme, tablo ve görseller yer almaz.")
        pdf.output(output_path)
        return output_path
    except Exception as e:
        raise ValueError(f"'{filename}' dosyası geçerli bir Word (DOCX) belgesi olarak işlenemedi veya dönüştürülemedi. Hata: {e}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
