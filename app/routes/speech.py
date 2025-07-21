# app/routes/speech.py

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.utils.speech_utils import convert_speech_to_text, convert_text_to_speech
import os
import aiofiles

INPUT_DIR = "inputs"
os.makedirs(INPUT_DIR, exist_ok=True)

router = APIRouter(prefix="/convert", tags=["Speech"])

@router.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...), language: str = Form("tr-TR")):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)
        
    output_path = convert_speech_to_text(content, file.filename, language)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/plain"
    )

@router.post("/text-to-speech")
async def text_to_speech(file: UploadFile = File(...), language: str = Form("tr")):
    input_path = os.path.join(INPUT_DIR, file.filename)
    content = await file.read()
    async with aiofiles.open(input_path, 'wb') as out_file:
        await out_file.write(content)
        
    output_path = convert_text_to_speech(content, file.filename, language)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="audio/mpeg"
    )
