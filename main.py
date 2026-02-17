# ================================
# ULTIMATE BRAIN — MAIN ENGINE
# Full Integrated Intelligence + Memory
# ================================

from flask import Flask
import threading
import time

import brain_engine
from opportunity_engine import calculate_opportunity
from opportunity_ranking_engine import rank_opportunities
from sector_intelligence_engine import sector_strength
from opportunity_report_engine import generate_report
from decision_memory_engine import save_decision

from engines.telegram_alert_engine import send_telegram_alert
from engines.opportunity_trigger_engine import process_opportunity
from engines.market_mode_engine import MarketModeEngine

app = Flask(__name__)


def run_engine():
    engine = brain_engine.BrainEngine()
    market_mode_engine = MarketModeEngine()

    stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]

    while True:
        try:
            market_data = {
                "fii_flow": 500,
                "dii_flow": 200,
                "volatility_index": 18,
                "sentiment": 60,
                "index_returns": [0.3, 0.1, -0.2]
            }

            mode_report = market_mode_engine.detect_mode(market_data)
            print("MARKET MODE:", mode_report, flush=True)

            opportunity_list = []

            for s in stocks:
                result = engine.analyze_stock(s)
                print("INGESTION:", result, flush=True)

                opportunity = calculate_opportunity(s, result.get("price", 0))
                opportunity_list.append(opportunity)

            sector_scores = sector_strength(opportunity_list)
            print("SECTOR STRENGTH:", sector_scores, flush=True)

            ranked = rank_opportunities(opportunity_list)
            print("TOP OPPORTUNITIES:", ranked[:5], flush=True)

            report = generate_report(ranked, sector_scores)
            print("OPPORTUNITY REPORT:", report, flush=True)

            # ---- MEMORY SAVE ----
            save_decision(report)

            for op in ranked[:5]:
                process_opportunity(op["symbol"], op, mode_report["mode"])

            time.sleep(300)

        except Exception as e:
            print("ENGINE ERROR:", e, flush=True)
            send_telegram_alert(f"ENGINE ERROR: {e}")
            time.sleep(60)


@app.route("/")
def home():
    return "Ultimate Brain Running"


if __name__ == "__main__":
    ingestion_thread = threading.Thread(target=run_engine)
    ingestion_thread.daemon = True
    ingestion_thread.start()

    try:
        send_telegram_alert("MARKET BOT STARTED — MEMORY LAYER ACTIVE")
    except Exception as e:
        print("Telegram startup alert failed:", e)

    app.run(host="0.0.0.0", port=10000)
