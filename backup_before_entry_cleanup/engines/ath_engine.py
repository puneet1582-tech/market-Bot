import csv

def load_price_data(filepath="data/price_data.csv"):
    prices = {}
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row["symbol"]
            price = float(row["price"])
            if symbol not in prices:
                prices[symbol] = []
            prices[symbol].append(price)
    return prices


def calculate_ath_drop(prices):
    results = {}

    for symbol, price_list in prices.items():
        ath = max(price_list)
        current = price_list[-1]
        drop_pct = round((ath - current) / ath * 100, 2)

        results[symbol] = {
            "ath": ath,
            "current": current,
            "drop_pct": drop_pct
        }

    return results


def bucket_stocks(ath_data):
    buckets = {
        "30%": [],
        "40%": [],
        "50%": [],
        "70%": [],
        "90%": []
    }

    for symbol, data in ath_data.items():
        d = data["drop_pct"]
        if d >= 90:
            buckets["90%"].append(symbol)
        elif d >= 70:
            buckets["70%"].append(symbol)
        elif d >= 50:
            buckets["50%"].append(symbol)
        elif d >= 40:
            buckets["40%"].append(symbol)
        elif d >= 30:
            buckets["30%"].append(symbol)

    return buckets

