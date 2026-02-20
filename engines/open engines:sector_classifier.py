import pandas as pd

STOCKS_PATH = "data/stocks.csv"
MAP_PATH = "data/sector_map.csv"

class SectorClassifier:
    def __init__(self):
        self.stocks = pd.read_csv(STOCKS_PATH)
        self.map = pd.read_csv(MAP_PATH)

    def classify(self):
        for i, row in self.stocks.iterrows():
            name = row["company"].upper()
            sector_found = False

            for _, m in self.map.iterrows():
                if m["keyword"] in name:
                    self.stocks.at[i, "sector"] = m["sector"]
                    sector_found = True
                    break

            if not sector_found:
                self.stocks.at[i, "sector"] = "Smallcap"

        self.stocks.to_csv(STOCKS_PATH, index=False)
        print("SECTOR CLASSIFICATION DONE")

# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    sc = SectorClassifier()
    sc.classify()
