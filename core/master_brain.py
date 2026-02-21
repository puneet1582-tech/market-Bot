"""
ULTIMATE BRAIN v2
INSTITUTIONAL PROBABILISTIC ENGINE
STABLE ARCHITECTURE — ENHANCED INTELLIGENCE CORE
"""

import csv
import math
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
        self.mode_probabilities = {}
        self.regime_confidence = 0
        self.signal_agreement = 0
        self.mode_score = {}
        self.top_opportunities = []

        self.ingestion = DataIngestionEngine()
        self.fundamental_engine = FundamentalEngine()

    def safe_execute(self, func, name):
        try:
            return func()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    def validate_environment(self):
        self.ingestion.ensure_data_ready()

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
        dispersion = std_ret

        regime_strength = (mean_ret / (std_ret + 1e-6))

        invest_prob = max(0, min(1, (advance_ratio * 0.6) + (regime_strength * 0.2)))
        trade_prob = max(0, 1 - abs(invest_prob - 0.5) * 2)
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

        breadth_strength = abs(advance_ratio - 0.5) * 2
        dispersion_factor = 1 - min(1, dispersion)
        confidence = (breadth_strength * 0.6 + dispersion_factor * 0.4) * 100

        self.regime_confidence = round(confidence, 2)

        self.mode_score = {
            "advance_ratio": round(advance_ratio, 4),
            "mean_return": round(mean_ret, 4),
            "dispersion": round(dispersion, 4)
        }

        return returns

    def compute_composite_scores(self, returns, fundamental_results):

        if not returns:
            return []

        mean_ret = statistics.mean(returns.values())
        std_ret = statistics.stdev(returns.values()) if len(returns) > 1 else 0.0001

        weight_map = {
            "LONG_TERM": 1.0,
            "SWING": 0.7,
            "WEAK": -0.3,
            "AVOID": -0.7
        }

        scored = []

        for symbol, ret in returns.items():

            z_momentum = (ret - mean_ret) / (std_ret + 1e-6)

            fundamental_label = fundamental_results.get(symbol, "AVOID")
            fundamental_score = weight_map.get(fundamental_label, -0.7)

            regime_alignment = 1 if (
                self.market_mode == "INVEST" and fundamental_label in ["LONG_TERM", "SWING"]
            ) else 0.5

            composite = (
                0.40 * z_momentum +
                0.30 * fundamental_score +
                0.15 * regime_alignment +
                0.15 * self.mode_probabilities.get(self.market_mode, 0)
            )

            scored.append((symbol, composite))

        return sorted(scored, key=lambda x: x[1], reverse=True)

    def compute_signal_agreement(self, scored):

        if not scored:
            return 0

        top_scores = [s[1] for s in scored[:20]]
        if len(top_scores) < 2:
            return 50

        std_top = statistics.stdev(top_scores)
        agreement = max(0, 100 - std_top * 50)
        return round(min(100, agreement), 2)

    def execute(self):

        self.safe_execute(self.validate_environment, "Environment Validation")

        returns = self.safe_execute(
            self.detect_market_mode,
            "Regime Engine v2"
        )

        fundamental_results = self.safe_execute(
            self.fundamental_engine.run,
            "Fundamental Engine"
        )

        scored = self.compute_composite_scores(returns, fundamental_results)

        self.signal_agreement = self.compute_signal_agreement(scored)

        if self.market_mode != "DEFENSIVE":
            self.top_opportunities = scored[:20]
        else:
            self.top_opportunities = []

        return self.build_output()

    def build_output(self):

        return {
            "MARKET_SUMMARY": {
                "mode": self.market_mode,
                "probabilities": self.mode_probabilities,
                "confidence": self.regime_confidence,
                "signal_agreement": self.signal_agreement,
                "metrics": self.mode_score
            },
            "TOP_20": [
                {
                    "rank": i + 1,
                    "symbol": sym,
                    "composite_score": round(score, 4)
                }
                for i, (sym, score) in enumerate(self.top_opportunities)
            ],
            "generated_at": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    brain = MasterBrain()
    print(brain.execute())
