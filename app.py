import os
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from dotenv import load_dotenv
import requests
from datetime import datetime

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# Facebook Access Token ve Doğrulama Token'larını ortamdan al
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'rastiel_token')

# Flask uygulamasını başlat
app = Flask(__name__)

# Log klasörü ve dosyasını tanımla
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)  # klasör yoksa oluştur
log_path = os.path.join(log_folder, "log.txt")

# Logging yapılandırması: log.txt dosyasına yazacak şekilde ayarlanır
logger = logging.getLogger("webhook_logger")
logger.setLevel(logging.INFO)

# RotatingFileHandler sayesinde log dosyası 5MB’yi geçince döner
handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=5)

# Log formatı: tarih, seviye, mesaj
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# GET isteği ile Facebook Webhook doğrulaması
@app.route('/', methods=['GET'])
def verify():
    challenge = request.args.get('hub.challenge')
    token = request.args.get('hub.verify_token')

    if token == VERIFY_TOKEN:
        logger.info("Webhook doğrulama başarılı.")
        return challenge
    else:
        logger.warning("Webhook doğrulama başarısız. Yanlış token.")
        return 'Invalid verification token', 403

# POST isteği ile gelen mesajları yakalayıp işleyen webhook endpoint
@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    # Gelen isteği log dosyasına detaylı şekilde kaydet
    logger.info(f"[{request.remote_addr}] {request.method} {request.path} - Gelen veri: {json.dumps(data)}")

    # Facebook mesaj içeriğini ayıklayıp cevap gönder
    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                for messaging in entry['messaging']:
                    sender_id = messaging['sender']['id']
                    message_text = messaging['message']['text']
                    send_message(sender_id, message_text)

    return "EVENT_RECEIVED", 200

# Facebook'a cevap mesajı gönderen yardımcı fonksiyon
def send_message(sender_id, message_text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={FB_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": f"mesaj: {message_text}"}
    }

    # Facebook'a POST isteği gönder
    response = requests.post(url, json=payload, headers=headers)

    # Cevabı log dosyasına kaydet
    logger.info(f"Facebook'a gönderilen cevap: {response.text}")

# Uygulama doğrudan çalıştırıldığında başlatılacak sunucu (geliştirme için)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
