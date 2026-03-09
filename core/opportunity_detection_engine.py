import pandas as pd

class OpportunityDetectionEngine:

    def __init__(self):

        self.price_file = "data/price_history.csv"
        self.fundamental_file = "data/fundamentals.csv"
        self.sector_file = "data/sector_map.csv"

    def run(self):

        print("Opportunity Detection Engine Running")

        try:
            price = pd.read_csv(self.price_file)
        except:
            price = pd.DataFrame()

        try:
            fundamentals = pd.read_csv(self.fundamental_file)
        except:
            fundamentals = pd.DataFrame()

        try:
            sector = pd.read_csv(self.sector_file)
        except:
            sector = pd.DataFrame()

        if price.empty or fundamentals.empty:
            return []

        merged = price.merge(fundamentals, on="symbol", how="inner")

        if not sector.empty and "symbol" in sector.columns:
            merged = merged.merge(sector, on="symbol", how="left")

        candidates = []

        for _, row in merged.iterrows():

            roe = row.get("roe", 0)
            growth = row.get("revenue_growth", 0)
            debt = row.get("debt_to_equity", 0)

            try:
                if roe > 15 and growth > 10 and debt < 1:
                    candidates.append({
                        "symbol": row.get("symbol"),
                        "sector": row.get("sector", "unknown"),
                        "roe": roe,
                        "growth": growth
                    })
            except:
                continue

        result = candidates[:20]

        print("Opportunity Detection Engine Completed")

        return result


def run():

    engine = OpportunityDetectionEngine()

    return engine.run()


if __name__ == "__main__":
    run()
