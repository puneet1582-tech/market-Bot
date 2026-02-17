# ==========================================
# ULTIMATE BRAIN — CORE ANALYSIS ENGINE
# Compatible with new NSE ingestion engine
# ==========================================

from datetime import datetime
from step2_full_data_engine import fetch_price


class BrainEngine:
    def __init__(self):
        """
        Core Brain Initialization
        Future layers:
        - fundamentals engine
        - sector intelligence
        - news intelligence
        """
        self.engine_name = "Ultimate Brain Core Engine"

    def analyze_stock(self, symbol):
        """
        Main stock analysis function
        Fetches live price and prepares analysis record
        """

        # Remove .NS for NSE engine
        nse_symbol = symbol.replace(".NS", "")

        price, volume = fetch_price(nse_symbol)

        record = {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "analysis_time": str(datetime.now())
        }

        return record
