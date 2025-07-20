# app/routes/excel_word.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.excel_word_utils import convert_excel_to_word, convert_word_to_excel
import os

router = APIRouter(prefix="/convert", tags=["Excel ↔ Word"])

@router.post("/excel-to-word")
async def excel_to_word(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_excel_to_word(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@router.post("/word-to-excel")
async def word_to_excel(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_word_to_excel(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
