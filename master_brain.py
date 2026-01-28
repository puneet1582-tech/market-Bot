from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📊 Daily Market Analysis (TOP 25 Stocks)")
print("")
print(f"Market Mode: {mode}")
print("")

# ---------------- MARKET STATUS ----------------
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
    market_mood = "Negative"
elif market_conditions["global_trend"] == "POSITIVE":
    market_mood = "Positive"
else:
    market_mood = "Neutral"

print(f"- Overall Market Mood: {market_mood}")

# ---------------- SECTOR SENSITIVITY ----------------
sector_news_sensitivity = {
    "IT": "High",
    "BANKING": "High",
    "FINANCIAL SERVICES": "High",
    "FMCG": "Low",
    "PHARMA": "Medium",
    "ENERGY": "Medium",
    "METALS": "High",
    "AUTO": "Medium",
    "INFRASTRUCTURE": "Medium"
}

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

# ---------------- NEWS IMPACT LOGIC ----------------
def news_impact(sector):
    sensitivity = sector_news_sensitivity.get(sector, "Medium")

    if market_mood == "Negative" and sensitivity == "High":
        return "Negative impact expected (news sensitive sector)"
    elif market_mood == "Positive" and sensitivity == "High":
        return "Positive impact possible (news sensitive sector)"
    elif market_mood == "Negative":
        return "Limited impact (defensive sector)"
    else:
        return "Neutral impact"

# ---------------- OUTPUT ----------------
print("")
print("TOP 25 Stocks – Detailed View:")
print("")

i = 1
for stock, score in top_25:
    data = fundamental_data.get(stock, {})
    sector = data.get("sector", "NA")

    print("====================================")
    print(f"{i}. {stock}")
    print("------------------------------------")
    print(f"Sector   : {sector}")
    print(f"Sales    : {data.get('sales')}")
    print(f"Profit   : {data.get('profit')}")
    print(f"Debt     : {data.get('debt')}")
    print(f"Risk     : {data.get('risk')}")
    print(f"Score    : {score}")

    print("News Impact:")
    print(f"- {news_impact(sector)}")

    print("Why selected:")
    if data.get("risk") == "LOW":
        print("- Business risk comparatively low")
    if str(data.get("debt")).startswith("0"):
        print("- Company is debt free")
    if "Cr" in str(data.get("profit")):
        print("- Company is consistently profitable")

    print("")
    i += 1

print("====================================")
print("Note: News impact is derived from market mood and sector sensitivity.")
