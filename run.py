import sys, os
sys.path.append(os.getcwd())

from core.env_loader import load_env
load_env()

from core.master_intelligence_controller import MasterIntelligenceController
from engines.alert_engine.telegram_alert import send_market_report
from core.system_logger import log

def main():

    brain = MasterIntelligenceController()

    result = brain.execute()

    print(result)

    log("Brain execution completed")

    try:
        send_market_report(result)
    except Exception as e:
        print("telegram error:", e)


if __name__ == "__main__":
    main()
