import csv
from engines.live_price_engine import get_live_price

def calculate_pl(filepath="data/trades.csv"):
    results = []

    try:
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stock = row["stock"]
                action = row["action"]
                buy_price = float(row["price"])
                live_price = get_live_price(stock)

                if live_price is None:
                    continue

                if action == "BUY":
                    pl = round(live_price - buy_price, 2)
                else:
                    pl = round(buy_price - live_price, 2)

                results.append({
                    "stock": stock,
                    "action": action,
                    "buy_price": buy_price,
                    "live_price": live_price,
                    "pl": pl
                })
    except FileNotFoundError:
        return []

    return results
