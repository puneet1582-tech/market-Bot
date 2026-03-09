import pandas as pd
import os

MARKET_FILE = "data/processed/market_mode.csv"
COMPANY_FILE = "data/processed/company_intelligence.csv"
OWNERSHIP_FILE = "data/processed/ownership_intelligence.csv"
SECTOR_FILE = "data/processed/sector_intelligence.csv"
MOMENTUM_FILE = "data/processed/momentum_stocks.csv"
UNIVERSE_FILE = "data/processed/tradable_universe.csv"
MAP_FILE = "data/processed/stock_sector_map.csv"

OUTPUT_DECISIONS = "data/processed/final_decisions.csv"
OUTPUT_TOP = "data/processed/top_opportunities.csv"

def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def run():

    market = safe_read(MARKET_FILE)
    company = safe_read(COMPANY_FILE)
    ownership = safe_read(OWNERSHIP_FILE)
    sector = safe_read(SECTOR_FILE)
    momentum = safe_read(MOMENTUM_FILE)
    universe = safe_read(UNIVERSE_FILE)
    sector_map = safe_read(MAP_FILE)

    if universe.empty:
        print("Universe empty")
        return

    df = universe.copy()

    if not company.empty:
        df = df.merge(company, on="symbol", how="left")

    if not ownership.empty:
        df = df.merge(ownership, on="symbol", how="left")

    if not sector_map.empty:
        df = df.merge(sector_map, on="symbol", how="left")

    if not sector.empty:
        df = df.merge(sector, on="sector", how="left")

    df["momentum_flag"] = df["symbol"].isin(momentum["symbol"]) if not momentum.empty else False

    market_mode = "NEUTRAL"
    if not market.empty:
        market_mode = market.iloc[0]["market_mode"]

    def decision(row):

        business = str(row.get("business_quality",""))
        sector_strength = str(row.get("sector_strength",""))
        inst = str(row.get("institutional_activity",""))
        momentum_flag = row.get("momentum_flag",False)

        if business == "WORLD_CLASS" and sector_strength == "STRONG" and inst == "ACCUMULATION":
            return "INVEST"

        if momentum_flag and sector_strength != "WEAK":
            return "TRADE"

        if sector_strength == "WEAK":
            return "DEFENSIVE"

        return "WATCH"

    df["decision"] = df.apply(decision,axis=1)

    df.to_csv(OUTPUT_DECISIONS,index=False)

    top = df[df["decision"].isin(["INVEST","TRADE"])]
    top = top.sort_values(by="decision")

    top.head(20).to_csv(OUTPUT_TOP,index=False)

    print("MASTER BRAIN COMPLETE")
    print("Final decisions:",len(df))
    print("Top opportunities:",len(top))

if __name__ == "__main__":
    run()
