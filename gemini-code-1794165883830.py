import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Grab your bot token and secret webhook key from cloud environment variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Simple in-memory or database token vault for the Hsyko Method
VALID_KEYS = {"HSYKO-8K120-ELITE", "HSYKO-VIP-PASS"}

@app.route("/", methods=["GET"])
def health_check():
    return "⚡ Hsyko_bot is online and guarding the 8K pipeline!", 200

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        username = update["message"]["from"].get("username", "Editor")

        if text.startswith("/start"):
            send_message(chat_id, f"Yo @{username} ⚡ Welcome to the **Hsyko Method** verification gateway.\n\nSend your key like this to unlock the tools:\n`/auth YOUR_KEY`")
            
        elif text.startswith("/auth "):
            user_key = text.split(" ", 1)[1].strip()
            if user_key in VALID_KEYS:
                send_message(chat_id, "✅ **Access Granted, Chef!** Your device is cleared for 8K 120fps lossless uploads. Go break the algorithm. 🔥")
            else:
                send_message(chat_id, "❌ **Invalid Key, blud.** That key is cooked. Check with Hsyko for a legitimate token.")
                
    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    # Cloud hosts usually supply a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)