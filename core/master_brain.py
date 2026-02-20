"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR (STEP-M)
STREAMING REGIME ENGINE + DATA CONTINUITY VALIDATION
PRODUCTION HARDENED
"""

import csv
import traceback
import statistics
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque
from core.data_ingestion_engine import DataIngestionEngine
from core.fundamental_engine import FundamentalEngine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "prices"


class MasterBrain:

    def __init__(self):
        self.market_mode = "UNDEFINED"
        self.mode_score = {}
        self.symbol_snapshot = {}
        self.data_gap_flag = False

        self.ingestion = DataIngestionEngine()
        self.fundamental_engine = FundamentalEngine()

    # -------------------------
    # SAFE EXECUTION
    # -------------------------

    def safe_execute(self, func, name):
        try:
            return func()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    # -------------------------
    # ENV VALIDATION
    # -------------------------

    def validate_environment(self):
        self.ingestion.ensure_data_ready()

    # -------------------------
    # STREAMING REGIME ENGINE
    # -------------------------

    def detect_market_mode(self):

        symbol_buffers = defaultdict(lambda: deque(maxlen=21))
        latest_prices = {}
        prev_prices = {}
        all_dates = set()

        files = sorted(PRICE_DATA_PATH.glob("*.csv"))

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row["symbol"]
                    date = row["date"]
                    price = float(row["price"])

                    all_dates.add(date)
                    symbol_buffers[symbol].append((date, price))

                    if symbol not in latest_prices:
                        latest_prices[symbol] = (date, price)
                    else:
                        if date > latest_prices[symbol][0]:
                            prev_prices[symbol] = latest_prices[symbol]
                            latest_prices[symbol] = (date, price)

        # ---- DATA CONTINUITY CHECK ----
        sorted_dates = sorted(all_dates)
        if len(sorted_dates) >= 2:
            latest_date = datetime.strptime(sorted_dates[-1], "%Y-%m-%d")
            prev_date = datetime.strptime(sorted_dates[-2], "%Y-%m-%d")
            gap = (latest_date - prev_date).days

            if gap > 7:
                self.data_gap_flag = True
        else:
            self.data_gap_flag = True

        # ---- BREADTH ----
        advances = 0
        declines = 0

        for symbol in latest_prices:
            if symbol in prev_prices:
                if latest_prices[symbol][1] > prev_prices[symbol][1]:
                    advances += 1
                elif latest_prices[symbol][1] < prev_prices[symbol][1]:
                    declines += 1

        total = advances + declines
        advance_ratio = advances / total if total else 0

        # ---- MOMENTUM ----
        returns = []

        for symbol, buffer in symbol_buffers.items():
            if len(buffer) == 21:
                first_price = buffer[0][1]
                last_price = buffer[-1][1]
                if first_price > 0:
                    ret = (last_price - first_price) / first_price
                    returns.append(ret)

        avg_return = statistics.mean(returns) if returns else 0
        volatility = statistics.pstdev(returns) if len(returns) > 1 else 0

        # ---- MODE DECISION ----
        if self.data_gap_flag:
            self.market_mode = "DEFENSIVE"
        elif advance_ratio >= 0.6 and avg_return > 0:
            self.market_mode = "INVEST"
        elif advance_ratio >= 0.4:
            self.market_mode = "TRADE"
        else:
            self.market_mode = "DEFENSIVE"

        self.mode_score = {
            "advance_ratio": round(advance_ratio, 4),
            "average_20d_return": round(avg_return, 4),
            "volatility_proxy": round(volatility, 4),
            "data_gap_flag": self.data_gap_flag,
            "advances": advances,
            "declines": declines
        }

        return self.market_mode

    # -------------------------
    # PRICE SNAPSHOT
    # -------------------------

    def run_price_snapshot(self):
        files = sorted(PRICE_DATA_PATH.glob("*.csv"))

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
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
        self.safe_execute(self.detect_market_mode, "Regime Engine")
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

