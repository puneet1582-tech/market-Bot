import pandas as pd
import os


SIGNAL_FILE = "data/processed/signal_matrix.csv"
MARKET_FILE = "data/processed/market_mode.csv"

OUTPUT_FILE = "data/processed/alpha_opportunities.csv"


def safe_read(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def compute_signal_density(signal_string):

    s = str(signal_string)

    signals = s.split("|")

    score = 0

    for sig in signals:

        if sig == "STRONG_BUSINESS":
            score += 3

        elif sig == "INSTITUTIONAL_BUYING":
            score += 3

        elif sig == "STRONG_SECTOR":
            score += 2

        elif sig == "PRICE_MOMENTUM":
            score += 2

        elif sig == "GLOBAL_TAILWIND":
            score += 1

        elif sig == "GLOBAL_HEADWIND":
            score -= 2

    return score


def classify_alpha(score):

    if score >= 7:
        return "COMPOUNDING_ALPHA"

    if score >= 5:
        return "ROTATION_ALPHA"

    if score >= 3:
        return "MOMENTUM_ALPHA"

    return "NO_ALPHA"


def run():

    signals = safe_read(SIGNAL_FILE)
    market = safe_read(MARKET_FILE)

    if signals.empty:
        print("Signal matrix missing")
        return

    df = signals.copy()

    df["signal_score"] = df["signals"].apply(
        compute_signal_density
    )

    df["alpha_type"] = df["signal_score"].apply(
        classify_alpha
    )

    market_mode = "NEUTRAL"

    if not market.empty:
        market_mode = market.iloc[0]["market_mode"]

    if market_mode == "RISK":

        df.loc[
            df["alpha_type"] == "MOMENTUM_ALPHA",
            "alpha_type"
        ] = "WEAK_ALPHA"


    alpha_df = df[
        df["alpha_type"].isin(
            [
                "COMPOUNDING_ALPHA",
                "ROTATION_ALPHA",
                "MOMENTUM_ALPHA"
            ]
        )
    ]

    alpha_df = alpha_df.sort_values(
        by="signal_score",
        ascending=False
    )

    alpha_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Alpha discovery complete")
    print("Total signals:",len(df))
    print("Alpha opportunities:",len(alpha_df))


if __name__ == "__main__":
    run()
