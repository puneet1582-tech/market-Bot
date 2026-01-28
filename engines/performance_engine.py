import csv
from engines.live_price_engine import get_live_price

def performance_report(filepath="data/trades.csv"):
    total = 0
    win = 0
    loss = 0
    zero = 0

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
                    pl = live_price - buy_price
                else:
                    pl = buy_price - live_price

                total += 1
                if pl > 0:
                    win += 1
                elif pl < 0:
                    loss += 1
                else:
                    zero += 1
    except FileNotFoundError:
        return None

    win_rate = round((win / total) * 100, 2) if total > 0 else 0

    return {
        "total": total,
        "win": win,
        "loss": loss,
        "zero": zero,
        "win_rate": win_rate
    }
