
# ----- NEWS IMPACT INTEGRATION -----
try:
    from core.news_signal_engine import news_stock_signals
    news_signals = news_stock_signals()
except:
    news_signals = {}

def apply_news_boost(top_list):

    boosted = []

    for item in top_list:

        symbol = item.get("symbol")

        boost = news_signals.get(symbol,0)

        item["score"] = item.get("score",0) + (boost * 0.05)

        boosted.append(item)

    boosted = sorted(boosted, key=lambda x:x["score"], reverse=True)

    return boosted
