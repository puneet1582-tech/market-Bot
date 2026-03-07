import json

def news_stock_signals():

    try:
        with open("data/news/stock_impact.json") as f:
            data = json.load(f)
    except:
        return {}

    signals = {}

    for item in data:
        stocks = item.get("stocks", [])
        for s in stocks:
            signals[s] = signals.get(s,0) + 1

    return signals


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)


def run():
    print('Engine started:', __name__)
