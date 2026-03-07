# STOCK UNIVERSE ENGINE
# Provides scalable stock universe list

def get_stock_universe():
    """
    Initial scalable universe (expand later to NIFTY 500)
    """

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "HDFCBANK.NS",
        "INFY.NS",
        "ICICIBANK.NS",
        "HINDUNILVR.NS",
        "LT.NS",
        "ITC.NS",
        "SBIN.NS",
        "BHARTIARTL.NS"
    ]

    return stocks


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
