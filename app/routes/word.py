from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.word_utils import convert_word_to_pdf
import os
import aiofiles

INPUT_DIR = "inputs"
os.makedirs(INPUT_DIR, exist_ok=True)

# ✅ Prefix ekle
router = APIRouter(prefix="/convert", tags=["Word"])

@router.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)
        
    output_path = convert_word_to_pdf(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/pdf"
    )
