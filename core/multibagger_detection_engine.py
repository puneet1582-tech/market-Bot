import pandas as pd

class MultibaggerDetectionEngine:

    def __init__(self):

        self.fundamental_file = "data/fundamentals.csv"
        self.price_file = "data/price_history.csv"

    def run(self):

        print("Multibagger Detection Engine Running")

        try:
            fundamentals = pd.read_csv(self.fundamental_file)
        except:
            fundamentals = pd.DataFrame()

        try:
            price = pd.read_csv(self.price_file)
        except:
            price = pd.DataFrame()

        if fundamentals.empty:
            return []

        candidates = []

        for _, row in fundamentals.iterrows():

            try:
                roe = row.get("roe",0)
                growth = row.get("revenue_growth",0)
                debt = row.get("debt_to_equity",0)

                if roe > 18 and growth > 15 and debt < 0.8:

                    candidates.append({
                        "symbol": row.get("symbol"),
                        "roe": roe,
                        "growth": growth
                    })

            except:
                continue

        print("Multibagger Detection Engine Completed")

        return candidates[:10]


def run():

    engine = MultibaggerDetectionEngine()

    return engine.run()


if __name__ == "__main__":
    run()
