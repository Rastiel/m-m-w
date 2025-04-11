import os
import json
import logging
import psycopg2
import requests
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# Facebook Access Token ve doğrulama token'larını al
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'rastiel_token')

# PostgreSQL bağlantı bilgileri
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = Flask(__name__)

# Logging ayarları
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_path = os.path.join(log_folder, "log.txt")

logger = logging.getLogger("webhook_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Facebook kullanıcı adını çeken fonksiyon
def get_user_name(user_id):
    try:
        url = f"https://graph.facebook.com/{user_id}?access_token={FB_ACCESS_TOKEN}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("name", "Bilinmeyen")
        else:
            return "Erişim Yok"
    except Exception as e:
        logger.error(f"Kullanıcı ismi alınamadı: {e}")
        return "Hata"

# Mesajı veritabanına loglama
def log_message(direction, sender_id, recipient_id, platform, message_text):
    sender_name = get_user_name(sender_id) if direction == "inbound" else "bot"

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO messages (direction, sender_id, recipient_id, platform, message_text, sender_name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (direction, sender_id, recipient_id, platform, message_text, sender_name))

        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Mesaj loglandı: {sender_name}")
    except Exception as e:
        logger.error(f"❌ Veritabanı loglama hatası: {e}")

# Webhook doğrulama endpoint
@app.route('/', methods=['GET'])
def verify():
    challenge = request.args.get('hub.challenge')
    token = request.args.get('hub.verify_token')
    if token == VERIFY_TOKEN:
        return challenge
    return 'Invalid verification token', 403

# Webhook mesaj alma endpoint
@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    logger.info(f"Gelen veri: {json.dumps(data)}")

    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                for messaging in entry['messaging']:
                    sender_id = messaging['sender']['id']
                    recipient_id = messaging['recipient']['id']
                    message_text = messaging['message']['text']

                    log_message("inbound", sender_id, recipient_id, "messenger", message_text)
                    send_message(sender_id, message_text)

    return "EVENT_RECEIVED", 200

# Mesajı Facebook'a geri gönderen fonksiyon
def send_message(sender_id, message_text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={FB_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}
    cevap_mesaji = f"Aldım: {message_text}"

    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": cevap_mesaji}
    }

    response = requests.post(url, json=payload, headers=headers)
    logger.info(f"Gönderilen cevap: {response.text}")
    log_message("outbound", "bot", sender_id, "messenger", cevap_mesaji)

# Sunucu çalıştır
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)