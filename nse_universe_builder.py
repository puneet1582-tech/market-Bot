# NSE UNIVERSE BUILDER
# Builds and updates NSE universe CSV

import csv

UNIVERSE_FILE = "nse_universe.csv"

INITIAL_UNIVERSE = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "LT.NS",
    "ITC.NS",
    "SBIN.NS",
    "HINDUNILVR.NS",
    "BHARTIARTL.NS"
]

def build_initial_universe():
    try:
        with open(UNIVERSE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for stock in INITIAL_UNIVERSE:
                writer.writerow([stock])
        print("Initial NSE universe created")
    except Exception as e:
        print("Universe build error:", e)
