# app/routes/speech.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.utils.speech_utils import convert_speech_to_text, convert_text_to_speech
import os

router = APIRouter(prefix="/convert", tags=["Speech"])

@router.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_speech_to_text(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="text/plain"
    )

@router.post("/text-to-speech")
async def text_to_speech(file: UploadFile = File(...)):
    content = await file.read()
    output_path = convert_text_to_speech(content, file.filename)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="audio/mpeg"
    )
