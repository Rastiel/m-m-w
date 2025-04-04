import os, json, logging
from logging import handlers
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from sys import stdout

# .env dosyasındaki bilgileri yükle
load_dotenv()

# Facebook Access Token'ı .env dosyasından al
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN')

# Uygulama Başlatma
app = Flask(__name__)
logger = logging.getLogger("gunicorn.error")
logger.setLevel(logging.DEBUG) # set logger level
logFormatter = logging.Formatter\
("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

# Webhook doğrulaması için gerekli route
@app.route('/', methods=['GET'])
def verify():
    print("ab2")
    # Facebook'un Webhook doğrulama işlemi için gerekli parametreleri alıyoruz
    verify_token = os.getenv('VERIFY_TOKEN')  # .env dosyasındaki VERIFY_TOKEN'i kullanıyoruz
    challenge = request.args.get('hub.challenge')
    token = request.args.get('hub.verify_token')

    # Eğer verify token doğruysa, challenge'ı döndürüyoruz
    if token == verify_token:
        print("ok")
        return challenge
    else:
        print("not ok")
        return 'Invalid verification token', 403

# Webhook'tan gelen mesajları işlemek için POST route'u
@app.route('/', methods=['POST'])
def webhook():
    #print("ab1")
    data = request.json
    logger.info('Doing something')
    #print(json.dumps(request.json))
    with open("posted.log", "w") as fs:
         fs.write("dam ustunde un eler tombul tombul nineler")
    print("Webhook'tan gelen veri:", data)

    # Burada, gelen mesajları işleyebilir ve Facebook API'sine yanıt gönderebiliriz.
    # Örnek olarak, gelen mesajı yanıtlıyoruz:
    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                for messaging in entry['messaging']:
                    sender_id = messaging['sender']['id']
                    message_text = messaging['message']['text']
                    
                    # Facebook'a mesaj göndermek için bir API isteği yapıyoruz.
                    send_message(sender_id, message_text)

    return "EVENT_RECEIVED", 200

# Facebook'a mesaj göndermek için bir yardımcı fonksiyon
def send_message(sender_id, message_text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={FB_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": f"Mesajınızı aldım: {message_text}"}
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Facebook'a gönderilen cevap: {response.text}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
