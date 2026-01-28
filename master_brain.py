import yfinance as yf
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📊 Daily Market Analysis (Portfolio Builder)")
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
portfolio_10 = top_25[:10]

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

# ---------------- PORTFOLIO SECTION ----------------
print("")
print("📌 LONG TERM PORTFOLIO (TOP 10 STOCKS)")
print("")

i = 1
for stock, score in portfolio_10:
    data = fundamental_data.get(stock, {})
    trend = get_trend(stock)

    print("====================================")
    print(f"{i}. {stock}")
    print("------------------------------------")
    print(f"Sector : {data.get('sector')}")
    print(f"Sales  : {data.get('sales')}")
    print(f"Profit : {data.get('profit')}")
    print(f"Debt   : {data.get('debt')}")
    print(f"Risk   : {data.get('risk')}")
    print(f"Trend  : {trend}")
    print("")

    print("Why in Portfolio:")
    if data.get("risk") == "LOW":
        print("- Business risk कम है")
    if str(data.get("debt")).startswith("0"):
        print("- Company debt free है")
    if "Cr" in str(data.get("profit")):
        print("- Company लगातार profit में है")
    if trend == "Uptrend":
        print("- Price trend positive है")

    print("")
    print("Portfolio Allocation Idea:")
    print("- Total capital का लगभग 8–10%")

    print("")
    i += 1

print("====================================")
print("Portfolio Note:")
print("- ये Top 10 stocks long-term नजरिए से चुने गए हैं")
print("- हर stock में बराबर weight रखना बेहतर रहेगा")
print("- हर महीने review करना जरूरी है")
print("")
print("⚠️ यह portfolio केवल study और learning के लिए है, निवेश की सलाह नहीं।")
