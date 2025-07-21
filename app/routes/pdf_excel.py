# app/routes/pdf_excel.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.pdf_excel_utils import convert_pdf_to_excel, convert_excel_to_pdf
import os
import aiofiles

INPUT_DIR = "inputs"
os.makedirs(INPUT_DIR, exist_ok=True)

router = APIRouter(prefix="/convert", tags=["PDF ↔ Excel"])

@router.post("/pdf-to-excel")
async def pdf_to_excel(file: UploadFile = File(...)):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)

    output_path = convert_pdf_to_excel(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/excel-to-pdf")
async def excel_to_pdf(file: UploadFile = File(...)):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)

    output_path = convert_excel_to_pdf(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/pdf"
    )
