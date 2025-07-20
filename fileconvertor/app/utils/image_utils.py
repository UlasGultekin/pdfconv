import os
import tempfile
from PIL import Image
import pytesseract

def convert_image_to_text(content: bytes, filename: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    image = Image.open(tmp_path)
    text = pytesseract.image_to_string(image, lang="tur")

    os.remove(tmp_path)

    base_name = os.path.splitext(filename)[0]
    output_path = f"{base_name}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path
