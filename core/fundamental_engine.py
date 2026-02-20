"""
ULTIMATE BRAIN
10-YEAR FUNDAMENTAL ENGINE
Quarter-by-Quarter Institutional Analyzer
"""

import csv
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FUNDAMENTAL_PATH = PROJECT_ROOT / "data" / "fundamentals"

REQUIRED_COLUMNS = [
    "symbol",
    "quarter",
    "revenue",
    "net_profit",
    "debt",
    "cash_flow"
]

class FundamentalEngine:

    def __init__(self):
        self.data = defaultdict(list)

    # -----------------------------------
    # LOAD FUNDAMENTAL DATA
    # -----------------------------------
    def load_data(self):

        files = list(FUNDAMENTAL_PATH.glob("*.csv"))
        if not files:
            raise RuntimeError("No fundamental CSV files found")

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                if reader.fieldnames != REQUIRED_COLUMNS:
                    raise RuntimeError(
                        f"Invalid fundamental schema in {file.name}"
                    )

                for row in reader:
                    self.data[row["symbol"]].append(row)

    # -----------------------------------
    # QUARTERLY ANALYSIS
    # -----------------------------------
    def analyze_symbol(self, symbol_data):

        revenues = [float(x["revenue"]) for x in symbol_data]
        profits = [float(x["net_profit"]) for x in symbol_data]
        debts = [float(x["debt"]) for x in symbol_data]

        revenue_growth = revenues[-1] - revenues[0]
        profit_growth = profits[-1] - profits[0]
        debt_trend = debts[-1] - debts[0]

        if revenue_growth > 0 and profit_growth > 0 and debt_trend <= 0:
            return "LONG_TERM"

        if revenue_growth > 0 and profit_growth > 0:
            return "SWING"

        if profit_growth < 0:
            return "WEAK"

        return "AVOID"

    # -----------------------------------
    # RUN FULL ENGINE
    # -----------------------------------
    def run(self):

        results = {}

        for symbol, records in self.data.items():

            # Ensure chronological order
            records_sorted = sorted(records, key=lambda x: x["quarter"])

            if len(records_sorted) < 8:
                results[symbol] = "INSUFFICIENT_DATA"
                continue

            results[symbol] = self.analyze_symbol(records_sorted)

        return results
