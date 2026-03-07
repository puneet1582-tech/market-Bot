"""
ULTIMATE BRAIN v3.0
INSTITUTIONAL ENGINE — 10Y FUNDAMENTAL INTEGRATED
"""

import csv
import traceback
import statistics
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque

from core.data_ingestion_engine import DataIngestionEngine
from core.fundamental_engine import FundamentalEngine
from core.fundamental_10y_engine import Fundamental10YEngine


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "prices"


class MasterBrain:

    def __init__(self):

        self.market_mode = "UNDEFINED"
        self.mode_probabilities = {}
        self.regime_confidence = 0
        self.mode_score = {}
        self.top_opportunities = []

        self.ingestion = DataIngestionEngine()
        self.fundamental_engine = FundamentalEngine()
        self.fundamental_10y_engine = Fundamental10YEngine()

    # ---------------- SAFETY ---------------- #

    def safe_execute(self, func, name):
        try:
            return func()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    def validate_environment(self):
        self.ingestion.ensure_data_ready()

    # ---------------- PRICE ENGINE ---------------- #

    def load_price_data(self):

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

        return symbol_buffers, latest_prices, prev_prices

    # ---------------- MARKET MODE ---------------- #

    def detect_market_mode(self):

        buffers, latest, prev = self.load_price_data()

        advances, declines = 0, 0
        returns = {}

        for symbol in latest:
            if symbol in prev:
                if latest[symbol][1] > prev[symbol][1]:
                    advances += 1
                elif latest[symbol][1] < prev[symbol][1]:
                    declines += 1

        total = advances + declines
        advance_ratio = advances / total if total else 0

        for symbol, buffer in buffers.items():
            if len(buffer) == 21:
                first = buffer[0][1]
                last = buffer[-1][1]
                if first > 0:
                    returns[symbol] = (last - first) / first

        if not returns:
            self.market_mode = "DEFENSIVE"
            return {}

        mean_ret = statistics.mean(returns.values())
        std_ret = statistics.stdev(returns.values()) if len(returns) > 1 else 0.0001

        invest_prob = max(0, min(1, advance_ratio))
        trade_prob = 1 - abs(invest_prob - 0.5) * 2
        defensive_prob = max(0, 1 - invest_prob - trade_prob)

        total_prob = invest_prob + trade_prob + defensive_prob
        invest_prob /= total_prob
        trade_prob /= total_prob
        defensive_prob /= total_prob

        probs = {
            "INVEST": round(invest_prob, 4),
            "TRADE": round(trade_prob, 4),
            "DEFENSIVE": round(defensive_prob, 4)
        }

        self.mode_probabilities = probs
        self.market_mode = max(probs, key=probs.get)

        confidence = abs(advance_ratio - 0.5) * 200
        self.regime_confidence = round(confidence, 2)

        self.mode_score = {
            "advance_ratio": round(advance_ratio, 4),
            "mean_return": round(mean_ret, 4),
            "dispersion": round(std_ret, 4)
        }

        return returns

    # ---------------- COMPOSITE ENGINE ---------------- #

    def compute_composite_scores(self, returns, fundamental_labels, fundamental_10y_scores):

        if not returns:
            return []

        mean_ret = statistics.mean(returns.values())
        std_ret = statistics.stdev(returns.values()) if len(returns) > 1 else 0.0001

        label_weight_map = {
            "LONG_TERM": 1.0,
            "SWING": 0.7,
            "WEAK": -0.3,
            "AVOID": -0.7
        }

        scored = []

        for symbol, ret in returns.items():

            z = (ret - mean_ret) / (std_ret + 1e-6)
            z = max(-3, min(3, z))

            label_score = label_weight_map.get(fundamental_labels.get(symbol, "AVOID"), -0.7)
            ten_y_score = fundamental_10y_scores.get(symbol, 0)

            composite = (
                0.4 * z +
                0.2 * label_score +
                0.2 * self.mode_probabilities.get(self.market_mode, 0) +
                0.2 * ten_y_score
            )

            scored.append((symbol, composite))

        return sorted(scored, key=lambda x: x[1], reverse=True)

    # ---------------- EXECUTION ---------------- #

    def execute(self):

        self.safe_execute(self.validate_environment, "Environment Validation")

        returns = self.safe_execute(
            self.detect_market_mode,
            "Regime Engine"
        )

        fundamental_labels = self.safe_execute(
            self.fundamental_engine.run,
            "Fundamental Label Engine"
        )

        fundamental_10y_scores = self.safe_execute(
            self.fundamental_10y_engine.run,
            "10Y Fundamental Engine"
        )

        scored = self.compute_composite_scores(
            returns,
            fundamental_labels,
            fundamental_10y_scores
        )

        if self.market_mode != "DEFENSIVE":
            self.top_opportunities = scored[:20]
        else:
            self.top_opportunities = []

        return self.build_output()

    # ---------------- OUTPUT ---------------- #

    def build_output(self):

        return {
            "MARKET_SUMMARY": {
                "mode": self.market_mode,
                "probabilities": self.mode_probabilities,
                "confidence": self.regime_confidence,
                "metrics": self.mode_score
            },
            "TOP_20": [
                {
                    "rank": i + 1,
                    "symbol": sym,
                    "score": round(score, 4),
                    "composite_score": round(score, 4)
                }
                for i, (sym, score) in enumerate(self.top_opportunities)
            ],
            "generated_at": datetime.utcnow().isoformat()
        }


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
