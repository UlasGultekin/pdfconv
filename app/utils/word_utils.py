import os
import tempfile
import shutil
import platform
import subprocess

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_word_to_pdf(content: bytes, filename: str) -> str:
    """
    DOCX dosyasını PDF'e dönüştürür.
    Platformdan bağımsız olarak LibreOffice kullanmayı dener.
    """
    # LibreOffice'in (soffice komutu) sistemde kurulu olup olmadığını kontrol et
    soffice_path = shutil.which("soffice")
    if not soffice_path:
        # Alternatif olarak docx2pdf'i dene (Windows/macOS için)
        if platform.system() in ["Windows", "Darwin"]:
            try:
                from docx2pdf import convert
                print("LibreOffice bulunamadı, docx2pdf ile deneniyor...")
                # docx2pdf geçici dosya ile çalışır
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_docx_path = os.path.join(tmp_dir, filename)
                    with open(tmp_docx_path, "wb") as f:
                        f.write(content)
                    
                    convert(tmp_docx_path, OUTPUT_DIR)
                    base_name = os.path.splitext(filename)[0]
                    return os.path.join(OUTPUT_DIR, f"{base_name}.pdf")
            except ImportError:
                raise EnvironmentError("Word'den PDF'e dönüştürme için sisteminizde LibreOffice veya docx2pdf kütüphanesi kurulu olmalıdır.")
            except Exception as e:
                 raise RuntimeError(f"docx2pdf ile dönüştürme sırasında hata oluştu: {e}")
        
        raise EnvironmentError("Word'den PDF'e dönüştürme için sisteminizde LibreOffice kurulu olmalıdır.")

    # LibreOffice ile dönüştürme
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_docx_path = os.path.join(tmp_dir, filename)
        
        # Gelen içeriği geçici bir .docx dosyasına yaz
        with open(tmp_docx_path, "wb") as f:
            f.write(content)
        
        # LibreOffice'i komut satırından çalıştır
        try:
            subprocess.run(
                [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, tmp_docx_path],
                check=True,
                capture_output=True,
                timeout=60 # 60 saniye zaman aşımı
            )
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode("utf-8", errors="ignore")
            raise RuntimeError(f"LibreOffice ile dönüştürme sırasında bir hata oluştu: {error_message}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("LibreOffice ile dönüştürme işlemi zaman aşımına uğradı.")
        
        # Oluşturulan PDF dosyasını bul ve taşı
        base_name = os.path.splitext(filename)[0]
        generated_pdf_path = os.path.join(tmp_dir, f"{base_name}.pdf")
        
        if os.path.exists(generated_pdf_path):
            final_output_path = os.path.join(OUTPUT_DIR, f"{base_name}.pdf")
            shutil.move(generated_pdf_path, final_output_path)
            return final_output_path
        else:
            raise FileNotFoundError("LibreOffice tarafından PDF dosyası oluşturulamadı.")
