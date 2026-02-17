# ================================
# ULTIMATE BRAIN — MAIN ENGINE
# Production Integrated Version
# ================================

from flask import Flask
import threading
import time

import brain_engine
from opportunity_engine import calculate_opportunity
from engines.telegram_alert_engine import send_telegram_alert
from engines.opportunity_trigger_engine import process_opportunity
from engines.market_mode_engine import MarketModeEngine

app = Flask(__name__)


# ---------------- ENGINE LOOP ----------------
def run_engine():
    engine = brain_engine.BrainEngine()
    market_mode_engine = MarketModeEngine()

    stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]

    while True:
        try:
            # ---- Market Mode Detection ----
            market_data = {
                "fii_flow": 500,
                "dii_flow": 200,
                "volatility_index": 18,
                "sentiment": 60,
                "index_returns": [0.3, 0.1, -0.2]
            }

            mode_report = market_mode_engine.detect_mode(market_data)
            print("MARKET MODE:", mode_report, flush=True)

            # ---- Stock Loop ----
            for s in stocks:
                result = engine.analyze_stock(s)
                print("INGESTION:", result, flush=True)

                # ---- Opportunity Intelligence ----
                opportunity = calculate_opportunity(s, result.get("price", 0))
                print("OPPORTUNITY:", opportunity, flush=True)

                # ---- Telegram / Trigger Engine ----
                process_opportunity(s, opportunity, mode_report["mode"])

            time.sleep(300)

        except Exception as e:
            print("ENGINE ERROR:", e, flush=True)
            send_telegram_alert(f"ENGINE ERROR: {e}")
            time.sleep(60)


# ---------------- WEB ROUTES ----------------
@app.route("/")
def home():
    return "Ultimate Brain Running"


# ---------------- MAIN ----------------
if __name__ == "__main__":
    ingestion_thread = threading.Thread(target=run_engine)
    ingestion_thread.daemon = True
    ingestion_thread.start()

    try:
        send_telegram_alert("MARKET BOT STARTED — OPPORTUNITY ENGINE LIVE")
    except Exception as e:
        print("Telegram startup alert failed:", e)

    app.run(host="0.0.0.0", port=10000)
