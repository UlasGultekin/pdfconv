import os
import tempfile
from PIL import Image
import pytesseract

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_image_to_text(content: bytes, filename: str) -> str:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        image = Image.open(tmp_path)
        # Dil parametresini kaldırarak daha genel bir tanıma sağla
        text = pytesseract.image_to_string(image)

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path
