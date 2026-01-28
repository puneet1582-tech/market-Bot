import yfinance as yf
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📊 Daily Market Analysis (Sector Rotation System)")
print("")

# ---------------- MODE ----------------
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

# ---------------- SECTOR ROTATION LOGIC ----------------
sector_score = {}
sector_count = {}

for stock, score in top_25:
    data = fundamental_data.get(stock, {})
    sector = data.get("sector", "NA")

    sector_score[sector] = sector_score.get(sector, 0) + score
    sector_count[sector] = sector_count.get(sector, 0) + 1

# average score per sector
sector_avg = {}
for sector in sector_score:
    sector_avg[sector] = round(sector_score[sector] / sector_count[sector], 2)

# classify sectors
strong_sectors = []
weak_sectors = []

for sector, avg in sector_avg.items():
    if avg >= 5:
        strong_sectors.append(sector)
    else:
        weak_sectors.append(sector)

# ---------------- OUTPUT ----------------
print("")
print("SECTOR ROTATION SUMMARY:")
print("")

print("Strong Sectors Today:")
if strong_sectors:
    for s in strong_sectors:
        print(f"- {s}")
else:
    print("- कोई sector खास strong नहीं दिख रहा")

print("")
print("Weak / Neutral Sectors Today:")
if weak_sectors:
    for s in weak_sectors:
        print(f"- {s}")
else:
    print("- सभी sectors balanced हैं")

# ---------------- COMPANY DETAILS ----------------
print("")
print("TOP 25 Stocks (Sector Wise View):")
print("")

i = 1
for stock, score in top_25:
    data = fundamental_data.get(stock, {})
    sector = data.get("sector")

    print("====================================")
    print(f"{i}. {stock}")
    print("------------------------------------")
    print(f"Sector : {sector}")
    print(f"Sales  : {data.get('sales')}")
    print(f"Profit : {data.get('profit')}")
    print(f"Debt   : {data.get('debt')}")
    print(f"Risk   : {data.get('risk')}")
    print(f"Score  : {score}")
    print("")
    i += 1

print("====================================")
print("Note: Sector strength is based on average stock score in Top 25.")
