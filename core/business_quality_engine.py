import pandas as pd

class BusinessQualityEngine:

    def __init__(self):

        self.fundamental_file = "data/fundamentals.csv"

    def run(self):

        print("Business Quality Engine Running")

        try:
            fundamentals = pd.read_csv(self.fundamental_file)
        except:
            fundamentals = pd.DataFrame()

        if fundamentals.empty:
            return []

        strong_business = []

        for _, row in fundamentals.iterrows():

            try:

                revenue_growth = row.get("revenue_growth",0)
                roe = row.get("roe",0)
                debt = row.get("debt_to_equity",0)

                if revenue_growth > 12 and roe > 18 and debt < 1:

                    strong_business.append({
                        "symbol": row.get("symbol"),
                        "revenue_growth": revenue_growth,
                        "roe": roe
                    })

            except:
                continue

        print("Business Quality Engine Completed")

        return strong_business


def run():

    engine = BusinessQualityEngine()

    return engine.run()


if __name__ == "__main__":
    run()
