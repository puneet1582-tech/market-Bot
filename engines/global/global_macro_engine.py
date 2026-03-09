import pandas as pd
import os


NEWS_INPUT = "data/global/global_news_raw.csv"

SECTOR_OUTPUT = "data/processed/global_sector_impact.csv"
STOCK_OUTPUT = "data/processed/global_stock_impact.csv"


COMMODITY_MAP = {
    "oil":"Energy",
    "crude":"Energy",
    "gas":"Energy",
    "steel":"Metals",
    "copper":"Metals",
    "lithium":"EV",
    "semiconductor":"Technology",
    "chip":"Technology"
}


POLICY_MAP = {
    "defence":"Defence",
    "infrastructure":"CapitalGoods",
    "railway":"Railways",
    "renewable":"Energy",
    "solar":"Energy"
}


def classify_sector(text):

    text = str(text).lower()

    for key,sector in COMMODITY_MAP.items():
        if key in text:
            return sector

    for key,sector in POLICY_MAP.items():
        if key in text:
            return sector

    return "Neutral"


def compute_impact(text):

    text = str(text).lower()

    positive = ["increase","growth","support","boost","record"]
    negative = ["ban","fall","crisis","war","cut","decline"]

    for w in positive:
        if w in text:
            return "POSITIVE"

    for w in negative:
        if w in text:
            return "NEGATIVE"

    return "NEUTRAL"


def run():

    if not os.path.exists(NEWS_INPUT):
        print("No global news input")
        return

    df = pd.read_csv(NEWS_INPUT)

    df["sector"] = df["headline"].apply(classify_sector)

    df["impact"] = df["headline"].apply(compute_impact)

    sector = df.groupby(["sector","impact"]).size().reset_index(name="signals")

    sector.to_csv(SECTOR_OUTPUT,index=False)

    stock = sector.copy()

    stock.rename(columns={"sector":"affected_sector"},inplace=True)

    stock.to_csv(STOCK_OUTPUT,index=False)

    print("GLOBAL MACRO INTELLIGENCE COMPLETE")


if __name__ == "__main__":
    run()
