FROM python:3.11-slim

# Sistem bağımlılıklarını ve fontları yükle
RUN apt-get update && \
    apt-get install -y libreoffice fonts-dejavu fonts-noto && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python bağımlılıklarını yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port ayarla (ör. FastAPI için)
EXPOSE 8000

# Uygulama başlatma komutu
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 