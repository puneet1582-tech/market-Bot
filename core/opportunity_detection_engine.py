import pandas as pd

class OpportunityDetectionEngine:

    def __init__(self):
        self.price_file = "data/price_history.csv"
        self.fundamental_file = "data/fundamentals.csv"

    def run(self):

        print("Opportunity Detection Engine Running")

        try:
            price = pd.read_csv(self.price_file)
            fundamentals = pd.read_csv(self.fundamental_file)
        except Exception as e:
            print("Data load error:", e)
            return []

        # simple filter logic
        if "symbol" not in price.columns:
            return []

        merged = price.merge(fundamentals, on="symbol", how="inner")

        candidates = []

        for _, row in merged.iterrows():

            try:
                if row.get("roe", 0) > 15 and row.get("revenue_growth", 0) > 10:
                    candidates.append(row["symbol"])
            except:
                continue

        print("Opportunity Detection Engine Completed")

        return candidates[:20]


def run():

    engine = OpportunityDetectionEngine()

    return engine.run()


if __name__ == "__main__":
    run()
