from flask import Flask, request
import os

app = Flask(__name__)

# Burada debug modunu açıyoruz
app.config['DEBUG'] = True  # Bu satır da debug için geçerli olabilir

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "rastiel_token")

@app.route("/", methods=["GET"])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return str(challenge)
    return "Invalid verification token", 403

@app.route("/", methods=["POST"])
def receive_message():
    payload = request.get_json()
    print("📩 Gelen mesaj:", payload)  # Burada gelen mesajı terminalde logluyoruz
    return "OK", 200

# Flask debug modunu burada açıyoruz
if __name__ == "__main__":
    app.run(debug=True)  # Flask'ı debug modunda başlatıyoruz
