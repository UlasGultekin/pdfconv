# Dosya Dönüştürücü API

Bu proje, çeşitli dosya formatlarını (PDF, Word, Excel, CSV, Resim, Ses) birbirine dönüştürmek için tasarlanmış bir FastAPI tabanlı API sunucusudur.

## Özellikler

- **PDF İşlemleri**: PDF'i Word'e, Metne, Excel'e dönüştürme.
- **Word İşlemleri**: Word'ü PDF'e dönüştürme.
- **Excel İşlemleri**: Excel'i PDF'e, Word'e, CSV'ye dönüştürme.
- **CSV İşlemleri**: CSV'yi PDF'e, Excel'e dönüştürme.
- **Resim İşlemleri**: Resim (PNG, JPG vb.) dosyalarındaki metinleri okuma (OCR).
- **Ses İşlemleri**: Ses dosyalarını metne, metinleri ses dosyasına dönüştürme.
- Çok dilli karakter desteği için `DejaVuSans` fontu kullanılmaktadır.

## Kurulum

1.  **Projeyi Klonlayın:**
    ```bash
    git clone <proje-repo-adresi>
    cd fileconvertor
    ```

2.  **Python Sanal Ortamı Oluşturun ve Aktif Edin:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

## Dış Bağımlılıklar

Bu projenin bazı özellikleri, bilgisayarınızda ek yazılımların kurulu olmasını gerektirir:

-   **Tesseract OCR:** Resim dosyalarından metin çıkarmak (`/convert/image-to-text`) için gereklidir.
    -   [Tesseract Kurulum Kılavuzu](https://github.com/tesseract-ocr/tessdoc)
    -   Kurulum sırasında Türkçe veya desteklenmesini istediğiniz diğer dilleri de eklediğinizden emin olun.
    -   Kurulumdan sonra, Tesseract'in path'ini sisteminize tanıtmanız gerekebilir.

-   **Microsoft Word:** Word dosyalarını PDF'e dönüştürmek (`/convert/word-to-pdf`) için gereklidir.
    -   Bu özellik `docx2pdf` kütüphanesini kullanır ve bu kütüphane arkaplanda Word uygulamasını çalıştırır. Bu nedenle, sunucunun çalıştığı makinede MS Word'ün kurulu ve lisanslı olması gerekir.

## Kullanım

API sunucusunu başlatmak için projenin ana dizinindeyken aşağıdaki komutu çalıştırın:

```bash
uvicorn app.main:app --reload
```

Sunucu varsayılan olarak `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

API dokümantasyonunu ve interaktif test arayüzünü görmek için tarayıcınızda aşağıdaki adresleri ziyaret edebilirsiniz:

-   **Swagger UI:** `http://127.0.0.1:8000/docs`
-   **ReDoc:** `http://127.0.0.1:8000/redoc` 