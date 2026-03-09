import pandas as pd

class SectorMoneyFlowEngine:

    def __init__(self):
        self.sector_map_file = "data/sector_map.csv"
        self.price_file = "data/price_history.csv"

    def run(self):

        print("Sector Money Flow Engine Running")

        try:
            sector = pd.read_csv(self.sector_map_file)
        except:
            sector = pd.DataFrame()

        try:
            price = pd.read_csv(self.price_file)
        except:
            price = pd.DataFrame()

        if sector.empty or price.empty:
            return {}

        if "symbol" not in price.columns or "symbol" not in sector.columns:
            return {}

        merged = price.merge(sector, on="symbol", how="left")

        sector_flow = {}

        for _, row in merged.iterrows():

            sec = row.get("sector", "unknown")
            change = row.get("price_change", 0)

            if sec not in sector_flow:
                sector_flow[sec] = 0

            try:
                sector_flow[sec] += float(change)
            except:
                continue

        print("Sector Money Flow Engine Completed")

        return sector_flow


def run():
    engine = SectorMoneyFlowEngine()
    return engine.run()


if __name__ == "__main__":
    run()
