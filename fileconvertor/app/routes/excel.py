# app/routes/excel.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.excel_utils import convert_excel_to_csv, convert_csv_to_excel
import os

router = APIRouter(prefix="/convert", tags=["Excel"])

@router.post("/excel-to-csv")
async def excel_to_csv(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_excel_to_csv(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/csv"
    )

@router.post("/csv-to-excel")
async def csv_to_excel(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_csv_to_excel(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
