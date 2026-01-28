import csv
import os

def record_trade(stock, action, price, filepath="data/trades.csv"):
    exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["stock", "action", "price"])
        writer.writerow([stock, action, price])

def paper_trade_decision(stock, signal, live_price):
    if signal in ["STRONG BUY", "BUY"]:
        return "BUY"
    elif signal in ["STRONG AVOID", "WEAK AVOID"]:
        return "SELL"
    else:
        return "HOLD"

