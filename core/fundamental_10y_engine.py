import csv
from pathlib import Path
import statistics
import math

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "annual_10y" / "annual_fundamentals_10y.csv"


class Fundamental10YEngine:

    def load_data(self):
        data = {}

        if not DATA_PATH.exists():
            return {}

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                symbol = row["symbol"]
                year = int(row["year"])

                revenue = float(row.get("revenue", 0) or 0)
                net_profit = float(row.get("net_profit", 0) or 0)
                debt = float(row.get("debt", 0) or 0)
                cash_flow = float(row.get("cash_flow", 0) or 0)

                if symbol not in data:
                    data[symbol] = []

                data[symbol].append({
                    "year": year,
                    "revenue": revenue,
                    "net_profit": net_profit,
                    "debt": debt,
                    "cash_flow": cash_flow
                })

        return data

    def calculate_cagr(self, values):
        if len(values) < 2:
            return 0

        start = values[0]
        end = values[-1]
        years = len(values) - 1

        if start <= 0 or years <= 0:
            return 0

        return (end / start) ** (1 / years) - 1

    def score_company(self, records):

        records = sorted(records, key=lambda x: x["year"])
        last_10 = records[-10:]   # max 10 years

        revenues = [r["revenue"] for r in last_10]
        profits = [r["net_profit"] for r in last_10]
        debts = [r["debt"] for r in last_10]
        cashflows = [r["cash_flow"] for r in last_10]

        revenue_cagr = self.calculate_cagr(revenues)
        profit_cagr = self.calculate_cagr(profits)

        # Debt trend (improving = good)
        debt_trend = debts[-1] - debts[0] if len(debts) > 1 else 0
        debt_score = 1 if debt_trend <= 0 else max(0, 1 - (debt_trend / (abs(debts[0]) + 1e-6)))

        # Cash consistency
        positive_cash_years = sum(1 for c in cashflows if c > 0)
        cash_consistency = positive_cash_years / len(cashflows) if cashflows else 0

        # Normalize CAGR (cap extreme)
        revenue_score = max(0, min(revenue_cagr, 0.30)) / 0.30
        profit_score = max(0, min(profit_cagr, 0.30)) / 0.30

        final_score = (
            40 * revenue_score +
            40 * profit_score +
            10 * debt_score +
            10 * cash_consistency
        )

        return round(final_score, 4)

    def run(self):

        data = self.load_data()
        scores = {}

        for symbol, records in data.items():
            if len(records) >= 3:   # minimum viable history
                scores[symbol] = self.score_company(records)

        return scores
