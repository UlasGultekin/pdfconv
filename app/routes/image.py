# app/routes/image.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.image_utils import convert_image_to_text
import os
import aiofiles

INPUT_DIR = "inputs"
os.makedirs(INPUT_DIR, exist_ok=True)

router = APIRouter(prefix="/convert", tags=["Image"])

@router.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)
        
    output_path = convert_image_to_text(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/plain"
    )
