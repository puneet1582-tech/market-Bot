import pandas as pd
import os


COMPANY_FILE = "data/processed/company_intelligence.csv"
OWNERSHIP_FILE = "data/processed/ownership_intelligence.csv"
SECTOR_FILE = "data/processed/sector_intelligence.csv"
MACRO_FILE = "data/processed/global_sector_impact.csv"
FLOW_FILE = "data/processed/stock_money_flow.csv"

OUTPUT_FILE = "data/processed/investment_committee_report.csv"


def safe_read(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def generate_thesis(row):

    business = str(row.get("business_quality",""))
    sector = str(row.get("sector_strength",""))
    inst = str(row.get("institutional_activity",""))
    macro = str(row.get("macro_signal",""))
    flow = row.get("money_flow",0)


    if business == "WORLD_CLASS" and sector == "STRONG" and inst == "ACCUMULATION":

        return (
            "COMPOUNDING BUSINESS",
            "High quality business with sector tailwinds and institutional accumulation"
        )


    if sector == "STRONG" and flow > 0:

        return (
            "CYCLICAL OPPORTUNITY",
            "Sector capital inflow with improving demand conditions"
        )


    if flow > 0:

        return (
            "TRADING CANDIDATE",
            "Short term liquidity driven opportunity"
        )


    if macro == "NEGATIVE":

        return (
            "AVOID",
            "Negative macro environment affecting sector profitability"
        )


    return (
        "WATCHLIST",
        "Requires further business or macro confirmation"
    )


def run():

    company = safe_read(COMPANY_FILE)
    ownership = safe_read(OWNERSHIP_FILE)
    sector = safe_read(SECTOR_FILE)
    macro = safe_read(MACRO_FILE)
    flow = safe_read(FLOW_FILE)

    if company.empty:
        print("Company intelligence missing")
        return

    df = company.copy()

    if not ownership.empty:
        df = df.merge(ownership,on="symbol",how="left")

    if not sector.empty:
        df = df.merge(sector,on="sector",how="left")

    if not macro.empty:
        df = df.merge(macro,on="sector",how="left")

    if not flow.empty and "money_flow" in flow.columns:
        df = df.merge(flow[["symbol","money_flow"]],on="symbol",how="left")

    df["money_flow"] = df["money_flow"].fillna(0)


    results = df.apply(
        lambda r: generate_thesis(r),
        axis=1
    )

    df["classification"] = results.apply(lambda x: x[0])
    df["investment_thesis"] = results.apply(lambda x: x[1])


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Investment committee analysis complete")
    print("Stocks analysed:",len(df))


if __name__ == "__main__":
    run()
