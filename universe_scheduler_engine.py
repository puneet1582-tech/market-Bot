# UNIVERSE SCHEDULER ENGINE
# Schedules automatic universe growth

import time
from universe_expansion_engine import add_stock_to_universe

# Example placeholder list (future: NSE API / list ingestion)
NEW_STOCKS_POOL = [
    "ASIANPAINT.NS",
    "MARUTI.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "ULTRACEMCO.NS"
]

def run_universe_scheduler():
    while True:
        try:
            for stock in NEW_STOCKS_POOL:
                add_stock_to_universe(stock)

            # run once every 24 hours
            time.sleep(86400)

        except Exception as e:
            print("Universe scheduler error:", e)
            time.sleep(3600)
