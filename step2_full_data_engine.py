from nsepython import nse_quote

def get_live_price(symbol):
    try:
        data = nse_quote(symbol)

        price = float(data["priceInfo"]["lastPrice"])
        volume = int(data["securityWiseDP"]["quantityTraded"])

        return price, volume

    except Exception as e:
        print(f"ERROR FETCHING {symbol}: {e}")
        return 0, 0
