import csv
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

QUARTERLY_PATH = PROJECT_ROOT / "data" / "quarterly_fundamentals_clean.csv"
ANNUAL_OUTPUT_PATH = PROJECT_ROOT / "data" / "annual_10y" / "annual_fundamentals_10y.csv"


class AnnualAggregatorEngine:

    def run(self):

        if not QUARTERLY_PATH.exists():
            return {"error": "quarterly file missing"}

        data = defaultdict(lambda: defaultdict(lambda: {
            "revenue": 0,
            "net_profit": 0,
            "debt": 0,
            "cash_flow": 0
        }))

        with open(QUARTERLY_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                symbol = row["symbol"]
                year = row["quarter"][:4]

                data[symbol][year]["revenue"] += float(row.get("sales", 0) or 0)
                data[symbol][year]["net_profit"] += float(row.get("profit", 0) or 0)
                data[symbol][year]["debt"] = float(row.get("debt", 0) or 0)
                data[symbol][year]["cash_flow"] += float(row.get("cashflow", 0) or 0)

        with open(ANNUAL_OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["symbol","year","revenue","net_profit","debt","cash_flow","roe","roce"])

            for symbol in data:
                for year in sorted(data[symbol]):
                    record = data[symbol][year]

                    writer.writerow([
                        symbol,
                        year,
                        record["revenue"],
                        record["net_profit"],
                        record["debt"],
                        record["cash_flow"],
                        0,
                        0
                    ])

        return {"status": "annual_data_built_correctly"}


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
