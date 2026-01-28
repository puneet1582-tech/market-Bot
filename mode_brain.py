import yfinance as yf

# NIFTY data fetch
nifty = yf.Ticker("^NSEI")
data = nifty.history(period="2d")

today_close = data["Close"][-1]
yesterday_close = data["Close"][-2]

change_percent = ((today_close - yesterday_close) / yesterday_close) * 100

# Simple real market conditions from price movement
if abs(change_percent) > 1.5:
    volatility = "HIGH"
elif abs(change_percent) > 0.5:
    volatility = "MEDIUM"
else:
    volatility = "LOW"

if change_percent > 0:
    global_trend = "POSITIVE"
elif change_percent < 0:
    global_trend = "NEGATIVE"
else:
    global_trend = "NEUTRAL"

# Liquidity dummy proxy (still structure based)
liquidity = "MEDIUM"

market_conditions = {
    "volatility": volatility,
    "liquidity": liquidity,
    "global_trend": global_trend
}

def decide_mode(conditions):
    if conditions["volatility"] == "HIGH" and conditions["global_trend"] == "NEGATIVE":
        return "DEFENSIVE MODE"
    elif conditions["liquidity"] == "HIGH" and conditions["global_trend"] == "POSITIVE":
        return "INVEST MODE"
    else:
        return "TRADE MODE"
