"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR (STEP-M)
REGIME-AWARE TOP-20 OPPORTUNITY ENGINE
CAPITAL DISCIPLINE ENABLED
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
        self.top_opportunities = []

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

    def validate_environment(self):
        self.ingestion.ensure_data_ready()

    # -------------------------
    # REGIME + RETURN COLLECTION
    # -------------------------

    def detect_market_mode(self):

        symbol_buffers = defaultdict(lambda: deque(maxlen=21))
        latest_prices = {}
        prev_prices = {}

        files = sorted(PRICE_DATA_PATH.glob("*.csv"))

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row["symbol"]
                    date = row["date"]
                    price = float(row["price"])

                    symbol_buffers[symbol].append((date, price))

                    if symbol not in latest_prices:
                        latest_prices[symbol] = (date, price)
                    else:
                        if date > latest_prices[symbol][0]:
                            prev_prices[symbol] = latest_prices[symbol]
                            latest_prices[symbol] = (date, price)

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

        # ---- MOMENTUM RETURNS ----
        returns = {}
        for symbol, buffer in symbol_buffers.items():
            if len(buffer) == 21:
                first_price = buffer[0][1]
                last_price = buffer[-1][1]
                if first_price > 0:
                    ret = (last_price - first_price) / first_price
                    returns[symbol] = ret

        avg_return = statistics.mean(returns.values()) if returns else 0

        # ---- MODE DECISION ----
        if advance_ratio >= 0.6 and avg_return > 0:
            self.market_mode = "INVEST"
        elif advance_ratio >= 0.4:
            self.market_mode = "TRADE"
        else:
            self.market_mode = "DEFENSIVE"

        self.mode_score = {
            "advance_ratio": round(advance_ratio, 4),
            "average_20d_return": round(avg_return, 4),
            "advances": advances,
            "declines": declines
        }

        return returns

    # -------------------------
    # OPPORTUNITY ENGINE
    # -------------------------

    def build_top_opportunities(self, returns, fundamental_results):

        if self.market_mode == "DEFENSIVE":
            self.top_opportunities = []
            return

        weight_map = {
            "LONG_TERM": 3,
            "SWING": 2,
            "WEAK": -1,
            "AVOID": -2
        }

        scored = []

        sorted_returns = sorted(
            returns.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for rank, (symbol, ret) in enumerate(sorted_returns, start=1):

            fundamental_label = fundamental_results.get(symbol, "AVOID")
            fundamental_weight = weight_map.get(fundamental_label, -2)

            # INVEST mode filter
            if self.market_mode == "INVEST":
                if fundamental_label not in ["LONG_TERM", "SWING"]:
                    continue

            composite_score = (len(sorted_returns) - rank) + fundamental_weight
            scored.append((symbol, composite_score))

        scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
        self.top_opportunities = scored_sorted[:20]

    # -------------------------
    # MASTER EXECUTION
    # -------------------------

    def execute(self):

        self.safe_execute(self.validate_environment, "Environment Validation")

        returns = self.safe_execute(
            self.detect_market_mode,
            "Regime Engine"
        )

        fundamental_results = self.safe_execute(
            self.fundamental_engine.run,
            "Fundamental Engine"
        )

        self.build_top_opportunities(returns, fundamental_results)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "market_mode": self.market_mode,
            "mode_score": self.mode_score,
            "top_20_opportunities": self.top_opportunities
        }


if __name__ == "__main__":
    brain = MasterBrain()
    result = brain.execute()
    print(result)

