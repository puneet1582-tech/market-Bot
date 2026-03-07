# NSE UNIVERSE LOADER
# Prepares scalable NSE stock universe ingestion

import csv

UNIVERSE_FILE = "nse_universe.csv"

def load_nse_universe():
    stocks = []

    try:
        with open(UNIVERSE_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    stocks.append(row[0].strip())
    except:
        # fallback initial universe
        stocks = [
            "RELIANCE.NS",
            "TCS.NS",
            "HDFCBANK.NS",
            "INFY.NS",
            "ICICIBANK.NS"
        ]

    return stocks


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
