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
    print("- इसलिए सुरक्षित (defensive) stocks पर ध्यान दिया गया है")
elif mode == "INVEST MODE":
    print("- Market का trend positive है")
    print("- Liquidity ठीक है")
    print("- इसलिए long-term investment के मौके देखे जा रहे हैं")
else:
    print("- Market में साफ दिशा नहीं है")
    print("- इसलिए trading / short-term नजरिया रखा गया है")

# ---------------- MARKET STATUS ----------------
print("")
print("Market स्थिति:")
if market_conditions["volatility"] == "HIGH":
    print("- Volatility ज्यादा है")
if market_conditions["liquidity"] == "LOW":
    print("- Liquidity कम है")
if market_conditions["global_trend"] == "NEGATIVE":
    print("- Global trend कमजोर है")

# ---------------- MARKET PSYCHOLOGY ----------------
print("")
print("Market Psychology:")
if market_conditions["global_trend"] == "NEGATIVE" and market_conditions["volatility"] == "HIGH":
    market_mood = "Fear (डर का माहौल)"
elif market_conditions["global_trend"] == "POSITIVE":
    market_mood = "Confidence (भरोसे का माहौल)"
else:
    market_mood = "Neutral (ना डर, ना ज्यादा भरोसा)"

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
            return f"{rsi_value} (Overbought)"
        elif rsi_value < 30:
            return f"{rsi_value} (Oversold)"
        else:
            return f"{rsi_value} (Neutral)"
    except:
        return "RSI not available"

# ---------------- OUTPUT ----------------
print("")
print("TOP 25 Stocks – Fundamental + Technical View:")
print("")

i = 1
for stock, score in top_25:
    data = fundamental_data.get(stock, {})

    trend = get_trend(stock)
    rsi_status = get_rsi(stock)

    print("====================================")
    print(f"{i}. {stock}")
    print("------------------------------------")
    print(f"Sector : {data.get('sector')}")
    print(f"Sales  : {data.get('sales')}")
    print(f"Profit : {data.get('profit')}")
    print(f"Debt   : {data.get('debt')}")
    print(f"Risk   : {data.get('risk')}")
    print(f"Score  : {score}")
    print("")

    print("Technical Analysis:")
    print(f"- Trend : {trend}")
    print(f"- RSI   : {rsi_status}")
    print("")

    print("Why selected:")
    if data.get("risk") == "LOW":
        print("- Business risk low")
    if str(data.get("debt")).startswith("0"):
        print("- Company is debt free")
    if "Cr" in str(data.get("profit")):
        print("- Company is profitable")

    print("")
    i += 1

print("====================================")
print("Note: Mode is auto-selected based on real market conditions.")
