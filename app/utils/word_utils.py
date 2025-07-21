from docx2pdf import convert
import os
import tempfile
import shutil
import platform

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_word_to_pdf(content: bytes, filename: str) -> str:
    """
    DOCX dosyasını PDF'e dönüştürür.
    Sadece Windows sistemlerde çalışır çünkü docx2pdf yalnızca Windows/macOS destekler.
    """
    # Yalnızca Windows ve macOS destekleniyor
    if platform.system() not in ["Windows", "Darwin"]:
        raise EnvironmentError("docx2pdf only works on Windows and macOS.")

    # Geçici klasör oluştur
    with tempfile.TemporaryDirectory() as tmp_dir:
        # .docx dosyasını geçici klasöre yaz
        tmp_docx_path = os.path.join(tmp_dir, filename)
        with open(tmp_docx_path, "wb") as f:
            f.write(content)

        # Dönüştürme işlemi
        try:
            convert(tmp_docx_path, tmp_dir)
        except Exception as e:
            raise RuntimeError(f"Dönüştürme sırasında hata oluştu: {e}")

        # PDF dosyasını bul
        base_name = os.path.splitext(filename)[0]
        pdf_name = f"{base_name}.pdf"
        pdf_path = os.path.join(tmp_dir, pdf_name)

        # Hedef klasöre taşı
        final_output_path = os.path.join(OUTPUT_DIR, pdf_name)
        shutil.move(pdf_path, final_output_path)

        return final_output_path
