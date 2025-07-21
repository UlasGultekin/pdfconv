from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from app.utils.cleanup_utils import cleanup_directory

# Rota modüllerini içe aktar
from app.routes import (
    pdf,
    word,
    excel,
    image,
    speech,
    excel_word,
    pdf_excel,
    csv_pdf
)

# Arka plan temizlik görevi
async def periodic_cleanup():
    while True:
        await asyncio.sleep(300)  # 5 dakika bekle (300 saniye)
        print("Periyodik temizlik görevi çalışıyor...")
        cleanup_directory("inputs", 120)  # 2 dakikadan (120 saniye) eski dosyaları sil
        cleanup_directory("outputs", 120) # 2 dakikadan (120 saniye) eski dosyaları sil

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Dosya Dönüştürücü API",
    description="PDF, Word, Excel, Görsel ve Ses dosyalarını birbirine dönüştürme servisi",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    # Arka plan görevini başlat
    asyncio.create_task(periodic_cleanup())

# Genel hata yakalayıcı (Exception Handler)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Beklenmedik bir sunucu hatası oluştu: {exc}"},
    )

# Geliştirme ortamı için tüm kaynaklara erişimi aç (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme ortamı için herkese açık; prod'da domain ile değiştir
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE vs.
    allow_headers=["*"],  # Authorization, Content-Type vs.
    expose_headers=["Content-Disposition"],
)

# Uygulamaya route’ları ekle
app.include_router(pdf.router,  tags=["PDF"])
app.include_router(word.router,  tags=["Word"])
app.include_router(excel.router,  tags=["Excel"])
app.include_router(image.router,  tags=["Image"])
app.include_router(speech.router,  tags=["Speech"])
app.include_router(excel_word.router,  tags=["Excel ↔ Word"])
app.include_router(pdf_excel.router,  tags=["PDF ↔ Excel"])
app.include_router(csv_pdf.router,  tags=["CSV ↔ PDF"])
