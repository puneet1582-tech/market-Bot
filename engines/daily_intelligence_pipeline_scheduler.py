"""
Ultimate Brain — Daily Intelligence Pipeline Scheduler
Runs full daily intelligence cycle automatically.
"""

import time
from datetime import datetime

from engines.nse_universe_master_builder import download_universe
from engines.historical_price_data_pipeline import run_pipeline as price_pipeline
from engines.quarterly_fundamentals_pipeline import run_pipeline as fundamentals_pipeline
from engines.quarterly_fundamental_comparison_engine import run_engine as comparison_engine
from engines.institutional_opportunity_scoring_engine import run_scoring
from engines.daily_top20_opportunity_engine import generate_top20


SLEEP_INTERVAL = 24 * 60 * 60  # 24 hours


def run_daily_cycle():
    print("=== DAILY INTELLIGENCE PIPELINE START ===", datetime.utcnow())

    download_universe()
    price_pipeline()
    fundamentals_pipeline()
    comparison_engine()
    run_scoring()
    generate_top20()

    print("=== DAILY INTELLIGENCE PIPELINE COMPLETED ===", datetime.utcnow())


if __name__ == "__main__":
    while True:
        try:
            run_daily_cycle()
        except Exception as e:
            print("PIPELINE ERROR:", e)

        time.sleep(SLEEP_INTERVAL)
