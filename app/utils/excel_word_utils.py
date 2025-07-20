import os
import tempfile
import pandas as pd
from docx import Document
import io

def convert_excel_to_word(content: bytes, filename: str) -> str:
    # Excel içeriğini geçici dosyaya yaz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Excel dosyasını oku (Unicode uyumlu)
    df = pd.read_excel(tmp_path, engine='openpyxl')
    os.remove(tmp_path)

    # Word belgesine yaz (her satır bir paragraf)
    doc = Document()
    for _, row in df.iterrows():
        # Hücreleri Unicode uyumlu şekilde birleştir
        paragraph = ', '.join(str(cell) if not pd.isna(cell) else '' for cell in row.values)
        doc.add_paragraph(paragraph)

    # Kaydet
    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.docx"
    doc.save(output_path)

    return output_path


def convert_word_to_excel(content: bytes, filename: str) -> str:
    # Word içeriğini geçici dosyaya yaz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Word içeriğini oku (Unicode destekli)
    doc = Document(tmp_path)
    os.remove(tmp_path)

    # Paragrafları satır olarak al
    data = []
    for para in doc.paragraphs:
        if para.text.strip():
            # Virgül ile ayırarak hücrelere böl
            data.append([cell.strip() for cell in para.text.split(',')])

    df = pd.DataFrame(data)

    # Excel olarak kaydet
    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.xlsx"
    df.to_excel(output_path, index=False, engine='openpyxl')

    return output_path
