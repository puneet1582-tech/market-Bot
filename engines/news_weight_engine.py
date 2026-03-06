import json

NEWS_FILE="data/news/stock_impact.json"

def news_weight():

    try:
        with open(NEWS_FILE) as f:
            data=json.load(f)
    except:
        return {}

    weights={}

    for item in data:

        for s in item.get("stocks",[]):

            weights[s]=weights.get(s,0)+1

    return weights
