from flask import Flask, request
import os

app = Flask(__name__)

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
    print("📩 Gelen mesaj:", payload)
    return "OK", 200
