from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.pdf_utils import (
    convert_pdf_to_text,
    convert_pdf_to_word,
    convert_text_to_pdf
)
import os

router = APIRouter(prefix="/convert", tags=["PDF"])

@router.post("/pdf-to-text")
async def pdf_to_text(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_pdf_to_text(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/plain"
    )

@router.post("/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_pdf_to_word(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@router.post("/text-to-pdf")
async def text_to_pdf(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_text_to_pdf(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/pdf"
    )
