import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def log_message(direction, sender_id, recipient_id, platform, message_text):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO messages (direction, sender_id, recipient_id, platform, message_text)
            VALUES (%s, %s, %s, %s, %s)
        """, (direction, sender_id, recipient_id, platform, message_text))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Mesaj veritabanına başarıyla kaydedildi.")
    except Exception as e:
        print(f"❌ Veritabanı bağlantı/kayıt hatası: {e}")

# Test için çalıştır
if __name__ == "__main__":
    log_message(
        direction="inbound",
        sender_id="user_123",
        recipient_id="bot_456",
        platform="whatsapp",
        message_text="Merhaba bu bir test mesajıdır."
    )
