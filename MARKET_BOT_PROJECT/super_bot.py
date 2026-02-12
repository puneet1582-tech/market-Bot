import os
import json
import asyncio
import pandas as pd
from flask import Flask
from telegram import Bot

app = Flask(__name__)

# Load config
CONFIG_PATH = "config.json"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

@app.route("/")
def home():
    return "MARKET BOT RUNNING"

@app.route("/send-test")
def send_test():
    cfg = load_config()
    asyncio.run(send_message(cfg["telegram_token"], cfg["chat_id"]))
    return "Message Sent"

async def send_message(token, chat_id):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text="MARKET BOT ACTIVE")

# Optional: load sample fundamentals
DATA_PATH = "data/fundamentals.csv"
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
