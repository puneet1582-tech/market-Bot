import pandas as pd
import os


OPPORTUNITY_FILE = "data/processed/opportunity_intelligence.csv"
FLOW_FILE = "data/processed/stock_money_flow.csv"
SECTOR_FLOW = "data/processed/sector_money_flow.csv"
MARKET_MODE = "data/processed/market_mode.csv"

OUTPUT_FILE = "data/processed/portfolio_allocation.csv"


def safe_read(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def conviction_score(row):

    score = 0

    opp = str(row.get("opportunity_type",""))
    flow = row.get("money_flow",0)

    if opp == "INSTITUTIONAL_COMPOUNDER":
        score += 5

    if opp == "SECTOR_ROTATION":
        score += 4

    if opp == "MOMENTUM_OPPORTUNITY":
        score += 3

    if flow > 0:
        score += 2

    if flow > 1000000:
        score += 3

    return score


def normalize_allocation(df):

    total = df["conviction"].sum()

    if total == 0:
        df["weight"] = 0
        return df

    df["weight"] = df["conviction"] / total

    return df


def run():

    opp = safe_read(OPPORTUNITY_FILE)
    flow = safe_read(FLOW_FILE)
    sector_flow = safe_read(SECTOR_FLOW)
    market = safe_read(MARKET_MODE)

    if opp.empty:
        print("Opportunity intelligence missing")
        return

    df = opp.copy()

    if not flow.empty:

        if "money_flow" in flow.columns:

            df = df.merge(
                flow[["symbol","money_flow"]],
                on="symbol",
                how="left"
            )

    df["money_flow"] = df["money_flow"].fillna(0)

    df["conviction"] = df.apply(
        conviction_score,
        axis=1
    )

    df = df.sort_values(
        by="conviction",
        ascending=False
    )

    df = normalize_allocation(df)

    df["capital_percent"] = (df["weight"] * 100).round(2)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Portfolio construction complete")
    print("Positions:",len(df))


if __name__ == "__main__":
    run()
