"""
ULTIMATE BRAIN
PRICE STRUCTURE & TREND ENGINE
10Y Trend + Quarterly Structure + Drawdown
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_FILE = PROJECT_ROOT / "data" / "prices" / "historical_prices.csv"


class PriceStructureEngine:

    def __init__(self):
        if not PRICE_FILE.exists():
            raise RuntimeError("Historical price file missing")
        self.df = pd.read_csv(PRICE_FILE)
        self.df["date"] = pd.to_datetime(self.df["date"])

    def compute_drawdown(self, series):
        rolling_max = series.cummax()
        drawdown = (series - rolling_max) / rolling_max
        return drawdown.min()

    def classify_trend(self, quarterly_prices):

        if len(quarterly_prices) < 8:
            return "INSUFFICIENT_DATA"

        last_8 = quarterly_prices[-8:]
        growth = last_8.iloc[-1] - last_8.iloc[0]

        if growth > 0 and last_8.is_monotonic_increasing:
            return "STRONG_UPTREND"

        if growth > 0:
            return "WEAK_UPTREND"

        if growth < 0:
            return "DOWNTREND"

        return "SIDEWAYS"

    def run(self):

        results = {}

        for symbol, data in self.df.groupby("symbol"):

            data = data.sort_values("date")

            # UPDATED: Use QE (Quarter End)
            quarterly = (
                data.set_index("date")
                .resample("QE")["price"]
                .last()
                .dropna()
            )

            trend = self.classify_trend(quarterly)

            cagr = None
            if len(data) > 252 * 3:
                years = (data["date"].iloc[-1] - data["date"].iloc[0]).days / 365
                if years > 0:
                    cagr = (
                        (data["price"].iloc[-1] / data["price"].iloc[0])
                        ** (1 / years)
                        - 1
                    )

            drawdown = self.compute_drawdown(data["price"])

            results[symbol] = {
                "trend": trend,
                "cagr": round(cagr, 4) if cagr else None,
                "max_drawdown": round(drawdown, 4)
            }

        return results


if __name__ == "__main__":
    engine = PriceStructureEngine()
    output = engine.run()
    print("Price Structure Engine Completed")
    print(list(output.items())[:5])
