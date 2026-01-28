import yfinance as yf
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📊 Daily Market Analysis (TOP 25 Stocks)")
print("")

# ---------------- MODE SECTION ----------------
print("MODE DECISION:")
print(f"आज का Active Mode: {mode}")
print("")

print("Mode चुनने का कारण:")
if mode == "DEFENSIVE MODE":
    print("- Market में volatility ज्यादा है")
    print("- Global trend कमजोर है")
    print("- इसलिए safe stocks पर focus किया गया है")
elif mode == "INVEST MODE":
    print("- Market का trend positive है")
    print("- Liquidity ठीक है")
    print("- इसलिए long-term investment के मौके देखे जा रहे हैं")
else:
    print("- Market में साफ दिशा नहीं है")
    print("- इसलिए short-term trading नजरिया रखा गया है")

# ---------------- MARKET PSYCHOLOGY ----------------
print("")
print("Market Psychology:")
if market_conditions["global_trend"] == "NEGATIVE" and market_conditions["volatility"] == "HIGH":
    market_mood = "Fear (डर का माहौल)"
elif market_conditions["global_trend"] == "POSITIVE":
    market_mood = "Confidence (भरोसे का माहौल)"
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

        rsi_value = round(rsi.iloc[-1], 2)

        if rsi_value > 70:
            return rsi_value, "Overbought"
        elif rsi_value < 30:
            return rsi_value, "Oversold"
        else:
            return rsi_value, "Neutral"
    except:
        return 0, "Not available"

# ---------------- BUY / HOLD / AVOID LOGIC ----------------
def decide_signal(mode, data, trend, rsi_status):
    if data.get("risk") == "LOW" and str(data.get("debt")).startswith("0") and trend == "Uptrend" and rsi_status == "Neutral":
        return "BUY"
    elif trend == "Downtrend" or rsi_status == "Overbought":
        return "AVOID"
    else:
        return "HOLD"

# ---------------- OUTPUT ----------------
print("")
print("TOP 25 Stocks – Final Signal:")
print("")

i = 1
for stock, score in top_25:
    data = fundamental_data.get(stock, {})

    trend = get_trend(stock)
    rsi_value, rsi_status = get_rsi(stock)

    signal = decide_signal(mode, data, trend, rsi_status)

    print("====================================")
    print(f"{i}. {stock}")
    print("------------------------------------")
    print(f"Sector : {data.get('sector')}")
    print(f"Sales  : {data.get('sales')}")
    print(f"Profit : {data.get('profit')}")
    print(f"Debt   : {data.get('debt')}")
    print(f"Risk   : {data.get('risk')}")
    print(f"Trend  : {trend}")
    print(f"RSI    : {rsi_value} ({rsi_status})")
    print("")
    print(f"FINAL SIGNAL: {signal}")
    print("")

    print("Reason:")
    if signal == "BUY":
        print("- Company fundamentals strong हैं")
        print("- Trend positive है और RSI balanced है")
    elif signal == "HOLD":
        print("- Stock stable है लेकिन clear entry नहीं है")
    else:
        print("- Trend कमजोर है या stock overbought है")

    print("")
    i += 1

print("====================================")
print("Note: Signals are based on combined Fundamental + Technical logic.")
