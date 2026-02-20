"""
ULTIMATE BRAIN
STABLE FUNDAMENTAL ENGINE
NO-CRASH MODE
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
        self.errors = []

    def load_data(self):

        if not FUNDAMENTAL_PATH.exists():
            return

        files = list(FUNDAMENTAL_PATH.glob("*.csv"))
        if not files:
            return

        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)

                    if reader.fieldnames != REQUIRED_COLUMNS:
                        self.errors.append(
                            f"Schema mismatch skipped: {file.name}"
                        )
                        continue

                    for row in reader:
                        self.data[row["symbol"]].append(row)

            except Exception as e:
                self.errors.append(
                    f"File skipped due to error: {file.name} | {str(e)}"
                )

    def analyze_symbol(self, symbol_data):

        try:
            revenues = [float(x["revenue"]) for x in symbol_data]
            profits = [float(x["net_profit"]) for x in symbol_data]
            debts = [float(x["debt"]) for x in symbol_data]
        except:
            return "DATA_ERROR"

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

    def run(self):

        results = {}

        self.load_data()

        if not self.data:
            return {"status": "NO_FUNDAMENTAL_DATA"}

        for symbol, records in self.data.items():

            records_sorted = sorted(records, key=lambda x: x["quarter"])

            if len(records_sorted) < 4:
                results[symbol] = "INSUFFICIENT_DATA"
                continue

            results[symbol] = self.analyze_symbol(records_sorted)

        return results
