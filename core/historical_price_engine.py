"""
ULTIMATE BRAIN
STABLE HISTORICAL PRICE ENGINE
Yahoo Finance via yfinance
10-Year Daily Data
"""

import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIVERSE_FILE = PROJECT_ROOT / "data" / "universe" / "nse_universe.csv"
PRICE_PATH = PROJECT_ROOT / "data" / "prices"

START_DATE = "2014-01-01"
END_DATE = datetime.utcnow().strftime("%Y-%m-%d")


class HistoricalPriceEngine:

    def __init__(self):
        PRICE_PATH.mkdir(parents=True, exist_ok=True)
        self.output_file = PRICE_PATH / "historical_prices.csv"

    def load_universe(self):
        if not UNIVERSE_FILE.exists():
            raise RuntimeError("Universe file missing")

        df = pd.read_csv(UNIVERSE_FILE)

        if "symbol" not in df.columns:
            raise RuntimeError("Universe schema invalid")

        symbols = df["symbol"].dropna().unique().tolist()

        if not symbols:
            raise RuntimeError("Universe empty")

        return symbols[:50]  # initial controlled batch

    def run(self):

        symbols = self.load_universe()
        all_data = []

        for symbol in symbols:
            ticker = f"{symbol}.NS"

            try:
                df = yf.download(
                    ticker,
                    start=START_DATE,
                    end=END_DATE,
                    progress=False,
                    auto_adjust=True
                )

                if df.empty:
                    continue

                df = df.reset_index()

                for _, row in df.iterrows():
                    all_data.append({
                        "date": row["Date"].strftime("%Y-%m-%d"),
                        "symbol": symbol,
                        "price": float(row["Close"])
                    })

            except:
                continue

        if not all_data:
            raise RuntimeError("No historical data fetched")

        out_df = pd.DataFrame(all_data)
        out_df.to_csv(self.output_file, index=False)

        return len(all_data)


if __name__ == "__main__":
    engine = HistoricalPriceEngine()
    count = engine.run()
    print(f"Historical Data Stored | Rows: {count}")
