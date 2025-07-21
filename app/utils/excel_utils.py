import os
import pandas as pd
import io

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_excel_to_csv(content: bytes, filename: str) -> str:
    # Excel içeriğini bellek üzerinden oku
    try:
        df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
    except Exception as e:
        print(f"Excel'den CSV'ye dönüştürme hatası: {e}")
        # Hata durumunda boş bir DataFrame oluştur
        df = pd.DataFrame()

    # Dosya adını düzenle ve CSV olarak yaz
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")  # UTF-8 BOM: Excel'de doğru görüntülenir

    return output_path

def convert_csv_to_excel(content: bytes, filename: str) -> str:
    # CSV içeriğini bellek üzerinden oku (Unicode destekli)
    try:
        df = pd.read_csv(io.BytesIO(content), encoding="utf-8")
    except Exception as e:
        print(f"CSV'den Excel'e dönüştürme hatası: {e}")
        df = pd.DataFrame()


    # Dosya adını düzenle ve Excel olarak yaz
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.xlsx")
    df.to_excel(output_path, index=False, engine='openpyxl')

    return output_path
