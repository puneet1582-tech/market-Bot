import yfinance as yf
import pandas as pd
import time
import os

UNIVERSE_FILE = "data/nse_universe_full.csv"

OUT_ANNUAL = "data/annual_fundamentals_10y_full.csv"
OUT_QUARTER = "data/quarterly_fundamentals_full.csv"

RETRY = 3
DELAY = 0.5


def safe_download(symbol):

    for _ in range(RETRY):
        try:
            ticker = yf.Ticker(symbol)

            annual = ticker.financials.T
            quarterly = ticker.quarterly_financials.T

            return annual, quarterly

        except Exception:
            time.sleep(1)

    return None, None


def build_fundamental_dataset():

    if not os.path.exists(UNIVERSE_FILE):
        print("Universe file missing")
        return

    universe = pd.read_csv(UNIVERSE_FILE)

    annual_all = []
    quarter_all = []

    for sym in universe["symbol"]:

        yahoo_symbol = sym + ".NS"

        annual, quarter = safe_download(yahoo_symbol)

        if annual is not None and not annual.empty:

            annual["symbol"] = sym
            annual_all.append(annual)

        if quarter is not None and not quarter.empty:

            quarter["symbol"] = sym
            quarter_all.append(quarter)

        time.sleep(DELAY)

    if len(annual_all) > 0:

        annual_df = pd.concat(annual_all)

        annual_df.to_csv(OUT_ANNUAL)

        print("Annual fundamentals saved:", len(annual_df))

    if len(quarter_all) > 0:

        quarter_df = pd.concat(quarter_all)

        quarter_df.to_csv(OUT_QUARTER)

        print("Quarterly fundamentals saved:", len(quarter_df))



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
