import os
import tempfile
import shutil
import platform
import subprocess
from docx import Document
from fpdf import FPDF

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Çok dilli destekli TTF font yolu
FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'DejaVuSans.ttf')
FONT_NAME = "DejaVuSans"

def split_long_words(text, max_len=50):
    # Çok uzun kelimeleri böl
    words = []
    for word in text.split():
        while len(word) > max_len:
            words.append(word[:max_len])
            word = word[max_len:]
        words.append(word)
    return ' '.join(words)

def convert_word_to_pdf(content: bytes, filename: str) -> str:
    """
    DOCX dosyasını PDF'e dönüştürür.
    1. LibreOffice varsa onu kullanır (tam uyumlu)
    2. Windows/macOS'ta docx2pdf (MS Word) varsa onu kullanır (tam uyumlu)
    3. Hiçbiri yoksa, sadece metin tabanlı PDF üretir (biçimlendirme ve görseller kaybolur)
    """
    # 1. LibreOffice kontrolü
    soffice_path = shutil.which("soffice")
    if soffice_path:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_docx_path = os.path.join(tmp_dir, filename)
            with open(tmp_docx_path, "wb") as f:
                f.write(content)
            try:
                subprocess.run(
                    [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, tmp_docx_path],
                    check=True,
                    capture_output=True,
                    timeout=60
                )
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode("utf-8", errors="ignore")
                raise RuntimeError(f"LibreOffice ile dönüştürme sırasında bir hata oluştu: {error_message}")
            except subprocess.TimeoutExpired:
                raise RuntimeError("LibreOffice ile dönüştürme işlemi zaman aşımına uğradı.")
            base_name = os.path.splitext(filename)[0]
            generated_pdf_path = os.path.join(tmp_dir, f"{base_name}.pdf")
            if os.path.exists(generated_pdf_path):
                final_output_path = os.path.join(OUTPUT_DIR, f"{base_name}.pdf")
                shutil.move(generated_pdf_path, final_output_path)
                return final_output_path
            else:
                raise FileNotFoundError("LibreOffice tarafından PDF dosyası oluşturulamadı.")

    # 2. docx2pdf (MS Word) kontrolü
    if platform.system() in ["Windows", "Darwin"]:
        try:
            from docx2pdf import convert
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_docx_path = os.path.join(tmp_dir, filename)
                with open(tmp_docx_path, "wb") as f:
                    f.write(content)
                convert(tmp_docx_path, OUTPUT_DIR)
                base_name = os.path.splitext(filename)[0]
                return os.path.join(OUTPUT_DIR, f"{base_name}.pdf")
        except ImportError:
            pass
        except Exception:
            pass

    # 3. Sadece metin tabanlı PDF (her ortamda çalışır)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}_textonly.pdf")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    doc = Document(tmp_path)
    os.remove(tmp_path)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(FONT_NAME, "", FONT_PATH, uni=True)
    pdf.set_font(FONT_NAME, size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Uyarıyı PDF'e ekle
    pdf.multi_cell(0, 10, "UYARI: Sunucuda ofis yazılımı bulunamadığı için sadece metin dönüştürüldü. Biçimlendirme ve görseller kaybolmuş olabilir.\n\n")
    
    # Metni PDF'e ekle (uzun kelimeleri bölerek)
    for para in doc.paragraphs:
        safe_text = split_long_words(para.text)
        pdf.multi_cell(0, 10, safe_text)
        
    pdf.output(output_path)
    return output_path
