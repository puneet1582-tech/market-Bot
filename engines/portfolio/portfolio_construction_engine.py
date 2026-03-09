import pandas as pd
import os


OPPORTUNITY_FILE = "data/processed/opportunity_intelligence.csv"
FLOW_FILE = "data/processed/stock_money_flow.csv"
MARKET_FILE = "data/processed/market_mode.csv"

OUTPUT_FILE = "data/processed/portfolio_candidates.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def score_row(row):

    score = 0

    opp = str(row.get("opportunity_type",""))
    flow = row.get("money_flow",0)

    if opp == "INSTITUTIONAL_COMPOUNDER":
        score += 5

    if opp == "SECTOR_ROTATION":
        score += 3

    if opp == "MOMENTUM_OPPORTUNITY":
        score += 2

    if flow > 0:
        score += 2

    return score


def run():

    opp = safe_read(OPPORTUNITY_FILE)
    flow = safe_read(FLOW_FILE)
    market = safe_read(MARKET_FILE)

    if opp.empty:
        print("Opportunity data missing")
        return

    df = opp.copy()

    if not flow.empty and "money_flow" in flow.columns:

        df = df.merge(
            flow[["symbol","money_flow"]],
            on="symbol",
            how="left"
        )

    else:

        df["money_flow"] = 0


    df["conviction_score"] = df.apply(
        score_row,
        axis=1
    )


    market_mode = "NEUTRAL"

    if not market.empty:
        market_mode = market.iloc[0]["market_mode"]


    if market_mode == "RISK":

        df = df[df["conviction_score"] >= 5]

    else:

        df = df[df["conviction_score"] >= 3]


    df = df.sort_values(
        by="conviction_score",
        ascending=False
    )


    df["capital_weight"] = (
        df["conviction_score"] /
        df["conviction_score"].sum()
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Portfolio construction complete")
    print("Candidates:",len(df))


if __name__ == "__main__":
    run()
