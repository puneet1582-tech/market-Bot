import yfinance as yf
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📊 Daily Market Analysis (Daily Change Tracker)")
print("")

# ---------------- MODE SECTION ----------------
print("MODE DECISION:")
print(f"आज का Active Mode: {mode}")
print("")

# ---------------- MARKET PSYCHOLOGY ----------------
print("Market Psychology:")
if market_conditions["global_trend"] == "NEGATIVE" and market_conditions["volatility"] == "HIGH":
    market_mood = "Fear"
elif market_conditions["global_trend"] == "POSITIVE":
    market_mood = "Confidence"
else:
    market_mood = "Neutral"

print(f"- Market Mood: {market_mood}")

# ---------------- STOCK SCORING ----------------
def score_stock(data):
    score = 0
    if data.get("risk") == "LOW":
        score += 3
    if str(data.get("debt")).startswith("0"):
        score += 2
    if "Cr" in str(data.get("profit")):
        score += 1
    return score

scored = []
for stock in stocks:
    data = fundamental_data.get(stock, {})
    scored.append((stock, score_stock(data)))

scored.sort(key=lambda x: x[1], reverse=True)
top_25 = scored[:25]

# ---------------- TECHNICAL FUNCTIONS ----------------
def get_trend(symbol):
    try:
        df = yf.Ticker(symbol + ".NS").history(period="20d")
        close = df["Close"]
        if close.iloc[-1] > close.mean():
            return "Uptrend"
        elif close.iloc[-1] < close.mean():
            return "Downtrend"
        else:
            return "Sideways"
    except:
        return "Data not available"

def get_daily_change(symbol):
    try:
        df = yf.Ticker(symbol + ".NS").history(period="2d")
        today = df["Close"].iloc[-1]
        yesterday = df["Close"].iloc[-2]
        change_pct = ((today - yesterday) / yesterday) * 100
        return round(change_pct, 2)
    except:
        return "NA"

# ---------------- OUTPUT ----------------
print("")
print("TOP 25 Stocks – With Daily Change:")
print("")

i = 1
for stock, score in top_25:
    data = fundamental_data.get(stock, {})
    trend = get_trend(stock)
    change = get_daily_change(stock)

    print("====================================")
    print(f"{i}. {stock}")
    print("------------------------------------")
    print(f"Sector : {data.get('sector')}")
    print(f"Sales  : {data.get('sales')}")
    print(f"Profit : {data.get('profit')}")
    print(f"Debt   : {data.get('debt')}")
    print(f"Risk   : {data.get('risk')}")
    print(f"Trend  : {trend}")
    print(f"Daily Change : {change}%")
    print("")

    print("Observation:")
    if isinstance(change, float):
        if change > 0:
            print("- Stock आज ऊपर बंद हुआ है")
        elif change < 0:
            print("- Stock आज नीचे बंद हुआ है")
        else:
            print("- Stock में कोई खास बदलाव नहीं हुआ")
    else:
        print("- Daily data available नहीं है")

    print("")
    i += 1

print("====================================")
print("Note: Daily Change = आज का close vs कल का close")
