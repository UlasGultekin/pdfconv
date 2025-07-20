# app/routes/image.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.image_utils import convert_image_to_text
import os

router = APIRouter(prefix="/convert", tags=["Image"])

@router.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_image_to_text(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/plain"
    )
