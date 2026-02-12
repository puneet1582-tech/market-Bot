import pandas as pd
import json
import asyncio
from telegram import Bot
from flask import Flask

app = Flask(__name__)

# Load data
df = pd.read_csv("data/fundamentals.csv")

# Load config
cfg = json.load(open("config.json"))

async def send_telegram():
    bot = Bot(token=cfg["telegram_token"])
    await bot.send_message(
        chat_id=cfg["chat_id"],
        text="MARKET BOT RUNNING SUCCESSFULLY"
    )

@app.route("/")
def home():
    asyncio.run(send_telegram())
    return "BOT ACTIVE"

if __name__ == "__main__":
    app.run()
