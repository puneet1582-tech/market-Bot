import subprocess
from core.master_intelligence_controller import MasterIntelligenceController

def main():

    # --- GLOBAL NEWS PIPELINE ---
    subprocess.run(["python","engines/news_engine/global_news_collector.py"])
    subprocess.run(["python","engines/news_engine/news_validator.py"])
    subprocess.run(["python","engines/news_engine/macro_classifier.py"])
    subprocess.run(["python","engines/news_engine/sector_mapper.py"])
    subprocess.run(["python","engines/news_engine/stock_mapper.py"])
    subprocess.run(["python","engines/news_engine/impact_engine.py"])

    # --- MASTER BRAIN ---
    brain = MasterIntelligenceController()
    result = brain.execute()

    print(result)

    # --- TELEGRAM ALERT ---
    try:
        from engines.alert_engine.telegram_alert import send_market_report
        send_market_report(result)
    except Exception as e:
        print("telegram error:", e)

    return result


if __name__ == "__main__":
    main()
