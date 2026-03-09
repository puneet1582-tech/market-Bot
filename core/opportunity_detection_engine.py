import pandas as pd

class OpportunityDetectionEngine:

    def __init__(self):

        self.business_file = "data/fundamentals.csv"
        self.price_file = "data/price_history.csv"
        self.sector_file = "data/sector_map.csv"
        self.institutional_file = "data/fii_dii.csv"

    def run(self):

        print("Opportunity Detection Engine Running")

        try:
            fundamentals = pd.read_csv(self.business_file)
        except:
            fundamentals = pd.DataFrame()

        try:
            price = pd.read_csv(self.price_file)
        except:
            price = pd.DataFrame()

        try:
            sector = pd.read_csv(self.sector_file)
        except:
            sector = pd.DataFrame()

        try:
            institutional = pd.read_csv(self.institutional_file)
        except:
            institutional = pd.DataFrame()

        if fundamentals.empty:
            return []

        merged = fundamentals.copy()

        if not price.empty and "symbol" in price.columns:
            merged = merged.merge(price, on="symbol", how="left")

        if not sector.empty and "symbol" in sector.columns:
            merged = merged.merge(sector, on="symbol", how="left")

        if not institutional.empty and "symbol" in institutional.columns:
            merged = merged.merge(institutional, on="symbol", how="left")

        opportunities = []

        for _, row in merged.iterrows():

            try:

                symbol = row.get("symbol")

                revenue_growth = row.get("revenue_growth",0)
                roe = row.get("roe",0)
                debt = row.get("debt_to_equity",0)
                fii_change = row.get("fii_change",0)

                if revenue_growth > 12 and roe > 18 and debt < 1 and fii_change >= 0:

                    opportunities.append({
                        "symbol": symbol,
                        "roe": roe,
                        "revenue_growth": revenue_growth,
                        "sector": row.get("sector","unknown")
                    })

            except:
                continue

        print("Opportunity Detection Engine Completed")

        return opportunities[:20]


def run():

    engine = OpportunityDetectionEngine()

    return engine.run()


if __name__ == "__main__":
    run()
