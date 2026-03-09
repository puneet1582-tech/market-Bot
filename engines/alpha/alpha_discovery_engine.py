import pandas as pd
import os


SIGNAL_FILE = "data/processed/signal_matrix.csv"
MARKET_FILE = "data/processed/market_mode.csv"

OUTPUT_FILE = "data/processed/alpha_opportunities.csv"


def safe_read(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def classify_alpha(signal_string):

    s = str(signal_string)

    signals = [

        "STRONG_BUSINESS" in s,
        "STRONG_SECTOR" in s,
        "INSTITUTIONAL_BUYING" in s,
        "PRICE_MOMENTUM" in s,
        "GLOBAL_TAILWIND" in s

    ]

    score = sum(signals)

    if score >= 4:
        return "COMPOUNDING_ALPHA"

    if score >= 3:
        return "ROTATION_ALPHA"

    if score >= 2:
        return "MOMENTUM_ALPHA"

    return "WATCH"



def run():

    signals = safe_read(SIGNAL_FILE)
    market = safe_read(MARKET_FILE)

    if signals.empty:
        print("Signal matrix missing")
        return

    df = signals.copy()

    df["alpha_type"] = df["signals"].apply(
        classify_alpha
    )

    market_mode = "NEUTRAL"

    if not market.empty:
        market_mode = market.iloc[0]["market_mode"]


    def adjust_for_market(row):

        alpha = row["alpha_type"]

        if market_mode == "RISK":

            if alpha == "MOMENTUM_ALPHA":
                return "WEAK_ALPHA"

        return alpha


    df["alpha_adjusted"] = df.apply(
        adjust_for_market,
        axis=1
    )


    alpha_df = df[
        df["alpha_adjusted"].isin([
            "COMPOUNDING_ALPHA",
            "ROTATION_ALPHA",
            "MOMENTUM_ALPHA"
        ])
    ]


    alpha_df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("Alpha discovery complete")
    print("Total signals:",len(df))
    print("Alpha opportunities:",len(alpha_df))


if __name__ == "__main__":
    run()
