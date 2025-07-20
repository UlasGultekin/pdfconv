from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.word_utils import convert_word_to_pdf
import os

# ✅ Prefix ekle
router = APIRouter(prefix="/convert", tags=["Word"])

@router.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_word_to_pdf(content, file.filename)

    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/pdf"
    )
