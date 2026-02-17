# ================================
# ULTIMATE BRAIN — MAIN ENGINE
# Batch Scanner Integrated
# ================================

from flask import Flask
import threading
import time

import brain_engine
from opportunity_engine import calculate_opportunity
from risk_weighted_ranking_engine import risk_weighted_rank
from sector_intelligence_engine import sector_strength
from opportunity_report_engine import generate_report
from decision_memory_engine import save_decision
from performance_tracker_engine import log_performance
from performance_evaluation_engine import evaluate_performance
from return_estimation_engine import estimate_returns
from dashboard_output_engine import build_dashboard
from daily_report_engine import generate_daily_report
from schedule_controller_engine import get_cycle_interval
from sector_universe_mapper import map_sector_universe
from sector_rotation_engine import update_sector_rotation
from sector_leadership_engine import detect_sector_leaders
from capital_flow_engine import detect_capital_flow
from nse_universe_loader import load_nse_universe
from scanner_batch_engine import create_batches

from engines.telegram_alert_engine import send_telegram_alert
from engines.opportunity_trigger_engine import process_opportunity
from engines.market_mode_engine import MarketModeEngine

app = Flask(__name__)


def run_engine():
    engine = brain_engine.BrainEngine()
    market_mode_engine = MarketModeEngine()

    while True:
        try:
            stocks = load_nse_universe()
            sector_map = map_sector_universe(stocks)

            market_data = {
                "fii_flow": 500,
                "dii_flow": 200,
                "volatility_index": 18,
                "sentiment": 60,
                "index_returns": [0.3, 0.1, -0.2]
            }

            mode_report = market_mode_engine.detect_mode(market_data)

            opportunity_list = []
            capital_flow = detect_capital_flow()

            # ---- Batch Processing ----
            for batch in create_batches(stocks, batch_size=25):
                for s in batch:
                    result = engine.analyze_stock(s)

                    opportunity = calculate_opportunity(
                        s,
                        result.get("price", 0),
                        mode_report["mode"]
                    )

                    opportunity_list.append(opportunity)

            sector_scores = sector_strength(opportunity_list)
            update_sector_rotation(sector_scores)

            sector_leaders = detect_sector_leaders(opportunity_list)

            ranked = risk_weighted_rank(opportunity_list)
            report = generate_report(ranked, sector_scores)

            save_decision(report)

            for op in ranked[:5]:
                process_opportunity(op["symbol"], op, mode_report["mode"])
                log_performance(op["symbol"], op["mode"], op["price"])

            perf_summary = evaluate_performance()
            return_summary = estimate_returns()

            dashboard = build_dashboard(
                mode_report,
                sector_scores,
                ranked,
                perf_summary,
                return_summary
            )

            dashboard["sector_leaders"] = sector_leaders
            dashboard["capital_flow"] = capital_flow

            daily_report = generate_daily_report(dashboard)
            send_telegram_alert(daily_report)

            print("BATCH NSE SCANNER CYCLE COMPLETE", flush=True)

            interval = get_cycle_interval()
            time.sleep(interval)

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
        send_telegram_alert("MARKET BOT STARTED — FULL NSE SCANNER ACTIVE")
    except Exception as e:
        print("Telegram startup alert failed:", e)

    app.run(host="0.0.0.0", port=10000)
