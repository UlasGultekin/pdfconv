import os
import tempfile
import pandas as pd
import io

def convert_excel_to_csv(content: bytes, filename: str) -> str:
    # Excel içeriğini geçici dosyaya yaz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Excel dosyasını oku
    df = pd.read_excel(tmp_path, engine='openpyxl')  # Daha geniş format desteği için
    os.remove(tmp_path)

    # Dosya adını düzenle ve CSV olarak yaz
    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")  # UTF-8 BOM: Excel'de doğru görüntülenir

    return output_path

def convert_csv_to_excel(content: bytes, filename: str) -> str:
    # CSV içeriğini bellek üzerinden oku (Unicode destekli)
    df = pd.read_csv(io.BytesIO(content), encoding="utf-8")

    # Dosya adını düzenle ve Excel olarak yaz
    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.xlsx"
    df.to_excel(output_path, index=False, engine='openpyxl')  # Daha geniş destek için

    return output_path
