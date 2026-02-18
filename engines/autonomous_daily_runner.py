"""
Ultimate Brain — Autonomous Daily Runner
Runs full intelligence cycle including data pipelines and Telegram delivery.
"""

import time
from datetime import datetime

from engines.daily_intelligence_pipeline_scheduler import run_daily_cycle
from engines.telegram_top20_delivery_engine import send_top20

RUN_INTERVAL = 24 * 60 * 60  # 24 hours


def autonomous_run():
    while True:
        try:
            print("=== AUTONOMOUS DAILY RUN START ===", datetime.utcnow())

            run_daily_cycle()
            send_top20()

            print("=== AUTONOMOUS DAILY RUN COMPLETED ===", datetime.utcnow())

        except Exception as e:
            print("AUTONOMOUS RUN ERROR:", e)

        time.sleep(RUN_INTERVAL)


if __name__ == "__main__":
    autonomous_run()
