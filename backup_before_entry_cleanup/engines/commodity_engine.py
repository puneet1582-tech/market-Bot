import pandas as pd

DATA_PATH = "data/commodities.csv"

COMMODITY_SECTOR_MAP = {
    "GOLD": ["Finance", "Defensive"],
    "SILVER": ["Metal"],
    "CRUDE": ["Energy"],
    "GAS": ["Energy"]
}

class CommodityEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def analyze(self):
        results = []

        for _, row in self.df.iterrows():
            commodity = row["commodity"]
            change = row["change_percent"]

            if commodity in COMMODITY_SECTOR_MAP:
                sectors = COMMODITY_SECTOR_MAP[commodity]
            else:
                sectors = []

            results.append({
                "commodity": commodity,
                "change_percent": change,
                "beneficiary_sectors": sectors
            })

        return results
