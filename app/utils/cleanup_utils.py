# app/utils/cleanup_utils.py
import os
import time
from glob import glob

def cleanup_directory(directory: str, max_age_seconds: int):
    """
    Belirtilen bir dizindeki dosyaları, maksimum yaş sınırından (saniye cinsinden) 
    daha eskiyseler siler.

    :param directory: Temizlenecek dizinin yolu.
    :param max_age_seconds: Bir dosyanın silinmeden önce sahip olabileceği maksimum yaş (saniye).
    """
    if not os.path.isdir(directory):
        print(f"Uyarı: Temizlenecek dizin bulunamadı: {directory}")
        return

    try:
        # Zaman damgası `max_age_seconds`'dan daha eski olan dosyaları bul
        cutoff_time = time.time() - max_age_seconds
        
        # Dizin içindeki tüm öğeleri kontrol et
        for item_path in glob(os.path.join(directory, '*')):
            if os.path.isfile(item_path):
                try:
                    # Dosyanın son değiştirilme zamanını al
                    file_mod_time = os.path.getmtime(item_path)
                    if file_mod_time < cutoff_time:
                        os.remove(item_path)
                        print(f"Temizlendi (eski dosya): {item_path}")
                except FileNotFoundError:
                    # Dosya başka bir işlem tarafından zaten silinmiş olabilir
                    continue
                except Exception as e:
                    print(f"'{item_path}' dosyası silinirken bir hata oluştu: {e}")
    except Exception as e:
        print(f"'{directory}' dizini temizlenirken bir hata oluştu: {e}") 