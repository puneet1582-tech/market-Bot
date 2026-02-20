"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR (STEP-M)
REAL PRICE BREADTH MODE ENGINE ACTIVE
STRICT PIPELINE CONTROL
"""

import csv
import traceback
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from core.data_ingestion_engine import DataIngestionEngine
from core.fundamental_engine import FundamentalEngine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "prices"


class MasterBrain:

    def __init__(self):
        self.market_data = []
        self.symbol_snapshot = {}
        self.market_mode = "UNDEFINED"
        self.mode_score = {}

        self.ingestion = DataIngestionEngine()
        self.fundamental_engine = FundamentalEngine()

    # -------------------------
    # ENV VALIDATION
    # -------------------------

    def validate_environment(self):
        self.ingestion.ensure_data_ready()

    def safe_execute(self, func, name):
        try:
            return func()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    # -------------------------
    # LOAD DATA
    # -------------------------

    def load_market_data(self):
        files = list(PRICE_DATA_PATH.glob("*.csv"))
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.market_data.append(row)

    # -------------------------
    # PRICE SNAPSHOT
    # -------------------------

    def run_price_snapshot(self):
        for row in self.market_data:
            symbol = row["symbol"]
            date = row["date"]
            price = float(row["price"])

            if symbol not in self.symbol_snapshot:
                self.symbol_snapshot[symbol] = (date, price)
            else:
                if date > self.symbol_snapshot[symbol][0]:
                    self.symbol_snapshot[symbol] = (date, price)

        self.symbol_snapshot = {
            k: v[1] for k, v in self.symbol_snapshot.items()
        }

    # -------------------------
    # REAL BREADTH ENGINE
    # -------------------------

    def detect_market_mode(self):

        price_by_date = defaultdict(dict)

        for row in self.market_data:
            date = row["date"]
            symbol = row["symbol"]
            price = float(row["price"])
            price_by_date[date][symbol] = price

        sorted_dates = sorted(price_by_date.keys())

        if len(sorted_dates) < 2:
            self.market_mode = "DEFENSIVE"
            return self.market_mode

        latest_date = sorted_dates[-1]
        prev_date = sorted_dates[-2]

        latest_prices = price_by_date[latest_date]
        prev_prices = price_by_date[prev_date]

        advances = 0
        declines = 0

        for symbol in latest_prices:
            if symbol in prev_prices:
                if latest_prices[symbol] > prev_prices[symbol]:
                    advances += 1
                elif latest_prices[symbol] < prev_prices[symbol]:
                    declines += 1

        total = advances + declines

        if total == 0:
            self.market_mode = "DEFENSIVE"
            return self.market_mode

        advance_ratio = advances / total

        self.mode_score = {
            "advance_ratio": round(advance_ratio, 4),
            "advances": advances,
            "declines": declines
        }

        if advance_ratio >= 0.65:
            self.market_mode = "INVEST"
        elif advance_ratio >= 0.45:
            self.market_mode = "TRADE"
        else:
            self.market_mode = "DEFENSIVE"

        return self.market_mode

    # -------------------------
    # FUNDAMENTAL ENGINE
    # -------------------------

    def run_fundamental_engine(self):
        self.fundamental_engine.load_data()
        return self.fundamental_engine.run()

    # -------------------------
    # MASTER EXECUTION
    # -------------------------

    def execute(self):

        self.safe_execute(self.validate_environment, "Environment Validation")
        self.safe_execute(self.load_market_data, "Load Market Data")
        self.safe_execute(self.detect_market_mode, "Market Breadth Mode Detection")
        self.safe_execute(self.run_price_snapshot, "Price Snapshot Engine")

        fundamental_results = self.safe_execute(
            self.run_fundamental_engine,
            "Fundamental Engine"
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "market_mode": self.market_mode,
            "mode_score": self.mode_score,
            "symbols_processed": len(self.symbol_snapshot),
            "fundamental_analysis": fundamental_results
        }


if __name__ == "__main__":
    brain = MasterBrain()
    result = brain.execute()
    print(result)

