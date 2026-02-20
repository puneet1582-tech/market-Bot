def check_exit(buy_price, live_price, sl_pct=5, target_pct=10):
    if buy_price is None or live_price is None:
        return "NO LIVE PRICE"

    sl_price = buy_price * (1 - sl_pct/100)
    target_price = buy_price * (1 + target_pct/100)

    if live_price <= sl_price:
        return "STOPLOSS HIT"
    elif live_price >= target_price:
        return "TARGET HIT"
    else:
        return "HOLD"
