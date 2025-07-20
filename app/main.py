from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Dosya Dönüştürücü API",
    description="PDF, Word, Excel, Görsel ve Ses dosyalarını birbirine dönüştürme servisi",
    version="1.0.0"
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
