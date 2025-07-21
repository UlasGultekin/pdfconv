import os
import tempfile
import speech_recognition as sr
import pyttsx3

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_speech_to_text(content: bytes, filename: str, language: str = "tr-TR") -> str:
    """
    Convert audio (WAV) to text using Google Web Speech API.
    :param content: Ses dosyası içeriği
    :param filename: Dosya adı
    :param language: Konuşma dili (varsayılan: Türkçe)
    """
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language=language)
    except sr.UnknownValueError:
        text = "[Ses anlaşılamadı]"
    except sr.RequestError:
        text = "[Google API hatası]"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path


def convert_text_to_speech(content: bytes, filename: str, language: str = "tr") -> str:
    """
    Convert text to speech and save as MP3.
    :param content: Metin içeriği (UTF-8 encoded)
    :param filename: Orijinal dosya adı
    :param language: Konuşma dili (dil ayarları sadece bazı TTS motorlarında etkilidir)
    """
    text = content.decode("utf-8").strip()
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")

    engine = pyttsx3.init()

    # Dile uygun ses bulmaya çalış
    if language:
        voices = engine.getProperty("voices")
        for voice in voices:
            # voice.languages genellikle ['en_US'] gibi bir liste döndürür
            if voice.languages and language in voice.languages[0].lower():
                engine.setProperty("voice", voice.id)
                break

    engine.setProperty("rate", 150)  # konuşma hızı
    engine.setProperty("volume", 1.0)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name
        
        engine.save_to_file(text, tmp_path)
        engine.runAndWait()
        
        # Dosya oluştuktan sonra taşı
        if os.path.exists(tmp_path):
            os.replace(tmp_path, output_path)
    finally:
        # Geçici dosya kalırsa sil
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return output_path
