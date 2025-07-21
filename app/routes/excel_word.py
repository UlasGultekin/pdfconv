# app/routes/excel_word.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.excel_word_utils import convert_excel_to_word, convert_word_to_excel
import os
import aiofiles

INPUT_DIR = "inputs"
os.makedirs(INPUT_DIR, exist_ok=True)

router = APIRouter(prefix="/convert", tags=["Excel ↔ Word"])

@router.post("/excel-to-word")
async def excel_to_word(file: UploadFile = File(...)):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)
        
    output_path = convert_excel_to_word(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@router.post("/word-to-excel")
async def word_to_excel(file: UploadFile = File(...)):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)
        
    output_path = convert_word_to_excel(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
