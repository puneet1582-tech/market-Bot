import yfinance as yf
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("🚨 ONLY BUY ALERT BOT")
print("")

print(f"Market Mode: {mode}")
print("")

# -------- STOCK SCORING --------
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

# -------- TECHNICAL --------
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
        return "NA"

def get_rsi(symbol):
    try:
        df = yf.Ticker(symbol + ".NS").history(period="20d")
        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        val = round(rsi.iloc[-1], 2)
        if val > 70:
            return val, "Overbought"
        elif val < 30:
            return val, "Oversold"
        else:
            return val, "Neutral"
    except:
        return 0, "NA"

# -------- BUY LOGIC --------
def decide_buy(data, trend, rsi_status):
    if data.get("risk") == "LOW" and str(data.get("debt")).startswith("0") and trend == "Uptrend" and rsi_status == "Neutral":
        return True
    return False

# -------- OUTPUT --------
print("Stocks with BUY Signal:")
print("")

count = 1
for stock, score in top_25:
    data = fundamental_data.get(stock, {})
    trend = get_trend(stock)
    rsi_value, rsi_status = get_rsi(stock)

    if decide_buy(data, trend, rsi_status):
        print("====================================")
        print(f"{count}. {stock}")
        print("------------------------------------")
        print(f"Sector : {data.get('sector')}")
        print(f"Sales  : {data.get('sales')}")
        print(f"Profit : {data.get('profit')}")
        print(f"Debt   : {data.get('debt')}")
        print(f"Trend  : {trend}")
        print(f"RSI    : {rsi_value} ({rsi_status})")
        print("")
        print("BUY SIGNAL क्योंकि:")
        print("- Fundamentals strong हैं")
        print("- Debt नहीं है")
        print("- Trend ऊपर की तरफ है")
        print("- RSI balanced है")
        print("")
        count += 1

if count == 1:
    print("आज कोई भी stock BUY criteria पूरा नहीं कर रहा।")

print("====================================")
print("Note: यह केवल study और learning के लिए है, निवेश की सलाह नहीं।")
