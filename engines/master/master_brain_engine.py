import pandas as pd

MARKET_FILE = "data/processed/market_mode.csv"
COMPANY_FILE = "data/processed/company_intelligence.csv"
OWNERSHIP_FILE = "data/processed/ownership_intelligence.csv"
MOMENTUM_FILE = "data/processed/momentum_stocks.csv"
SECTOR_FLOW_FILE = "data/processed/sector_money_flow.csv"
SECTOR_MAP_FILE = "data/processed/stock_sector_map.csv"
UNIVERSE_FILE = "data/processed/tradable_universe.csv"

OUT_DECISIONS = "data/processed/final_decisions.csv"
OUT_TOP = "data/processed/top_opportunities.csv"


def safe_read(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()


def run():

    universe = safe_read(UNIVERSE_FILE)
    company = safe_read(COMPANY_FILE)
    ownership = safe_read(OWNERSHIP_FILE)
    momentum = safe_read(MOMENTUM_FILE)
    sector_flow = safe_read(SECTOR_FLOW_FILE)
    sector_map = safe_read(SECTOR_MAP_FILE)
    market = safe_read(MARKET_FILE)

    if universe.empty:
        print("Universe missing")
        return

    df = universe.copy()

    df = df.merge(company, on="symbol", how="left")
    df = df.merge(ownership, on="symbol", how="left")
    df = df.merge(sector_map, on="symbol", how="left")

    if not sector_flow.empty:
        df = df.merge(sector_flow, on="sector", how="left")

    df["momentum_flag"] = df["symbol"].isin(momentum["symbol"]) if not momentum.empty else False

    market_mode = "NEUTRAL"

    if not market.empty:
        market_mode = market.iloc[0]["market_mode"]


    def decision(row):

        sector_strength = row.get("avg_return_20d",0)
        momentum = row.get("momentum_flag",False)
        inst = str(row.get("institutional_activity",""))
        business = str(row.get("business_quality",""))

        if business == "WORLD_CLASS" and sector_strength > 0.05:
            return "INVEST"

        if momentum and sector_strength > 0:
            return "TRADE"

        if sector_strength < -0.02:
            return "DEFENSIVE"

        return "WATCH"


    df["decision"] = df.apply(decision,axis=1)

    df.to_csv(OUT_DECISIONS,index=False)

    top = df[df["decision"].isin(["INVEST","TRADE"])]

    top = top.sort_values("decision")

    top.head(20).to_csv(OUT_TOP,index=False)

    print("MASTER BRAIN COMPLETED")


if __name__=="__main__":
    run()
