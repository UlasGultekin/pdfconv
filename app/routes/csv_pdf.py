# app/routes/csv_pdf.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.csv_pdf_utils import convert_csv_to_pdf, convert_pdf_to_csv
import os

router = APIRouter(prefix="/convert", tags=["CSV ↔ PDF"])

@router.post("/csv-to-pdf")
async def csv_to_pdf(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_csv_to_pdf(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/pdf"
    )

@router.post("/pdf-to-csv")
async def pdf_to_csv(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_pdf_to_csv(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/csv"
    )
