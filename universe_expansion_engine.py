# NSE UNIVERSE EXPANSION ENGINE
# Adds new stocks into existing universe file safely

import csv

UNIVERSE_FILE = "nse_universe.csv"

def add_stock_to_universe(stock_symbol):
    try:
        existing = set()

        try:
            with open(UNIVERSE_FILE, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        existing.add(row[0])
        except:
            pass

        if stock_symbol not in existing:
            with open(UNIVERSE_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([stock_symbol])
            print(f"{stock_symbol} added to universe")
        else:
            print(f"{stock_symbol} already exists")

    except Exception as e:
        print("Universe expansion error:", e)
