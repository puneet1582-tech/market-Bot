import yfinance as yf
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📅 WEEKLY MARKET SUMMARY")
print("")

# ---------------- MARKET MOOD ----------------
print("Market Mood (इस हफ्ते):")
if market_conditions["global_trend"] == "NEGATIVE" and market_conditions["volatility"] == "HIGH":
    mood = "Weak / Fear"
elif market_conditions["global_trend"] == "POSITIVE":
    mood = "Positive / Confidence"
else:
    mood = "Neutral"

print(f"- Overall Mood: {mood}")
print(f"- Active Mode: {mode}")

# ---------------- WEEKLY CHANGE (NIFTY) ----------------
try:
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="7d")
    start = data["Close"].iloc[0]
    end = data["Close"].iloc[-1]
    weekly_change = round(((end - start) / start) * 100, 2)
    print("")
    print("NIFTY Weekly Performance:")
    print(f"- Weekly Change: {weekly_change}%")
except:
    print("- Weekly index data not available")

# ---------------- SECTOR SUMMARY ----------------
print("")
print("Sector Summary:")
sector_count = {}
for stock in stocks:
    data = fundamental_data.get(stock, {})
    sector = data.get("sector", "NA")
    sector_count[sector] = sector_count.get(sector, 0) + 1

for sector, count in sector_count.items():
    print(f"- {sector}: {count} stocks")

# ---------------- BUY SIGNAL COUNT ----------------
def score_stock(data):
    score = 0
    if data.get("risk") == "LOW":
        score += 3
    if str(data.get("debt")).startswith("0"):
        score += 2
    if "Cr" in str(data.get("profit")):
        score += 1
    return score

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
            return "Overbought"
        elif val < 30:
            return "Oversold"
        else:
            return "Neutral"
    except:
        return "NA"

def decide_buy(data, trend, rsi_status):
    if data.get("risk") == "LOW" and str(data.get("debt")).startswith("0") and trend == "Uptrend" and rsi_status == "Neutral":
        return True
    return False

buy_count = 0
for stock in stocks:
    data = fundamental_data.get(stock, {})
    trend = get_trend(stock)
    rsi_status = get_rsi(stock)
    if decide_buy(data, trend, rsi_status):
        buy_count += 1

print("")
print("Action Summary:")
print(f"- Total BUY signals this week: {buy_count}")

# ---------------- TOP STOCKS ----------------
print("")
print("Top Strong Stocks (Fundamental based):")
scored = []
for stock in stocks:
    data = fundamental_data.get(stock, {})
    scored.append((stock, score_stock(data)))

scored.sort(key=lambda x: x[1], reverse=True)
top_5 = scored[:5]

i = 1
for stock, score in top_5:
    print(f"{i}. {stock} (Score: {score})")
    i += 1

print("")
print("Note: यह weekly summary केवल learning और analysis के लिए है।")
