from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("📊 Daily Market Analysis")
print("")
print(f"Market Mode: {mode}")
print("")

print("Market स्थिति:")
if market_conditions["volatility"] == "HIGH":
    print("- Volatility ज्यादा है")
if market_conditions["liquidity"] == "LOW":
    print("- Liquidity कम है")
if market_conditions["global_trend"] == "NEGATIVE":
    print("- Global trend कमजोर है")

# -------- MARKET PSYCHOLOGY --------
print("")
print("Market Psychology:")

if market_conditions["global_trend"] == "NEGATIVE" and market_conditions["volatility"] == "HIGH":
    market_mood = "Fear (डर का माहौल)"
    trend_strength = "Weak Trend"
elif market_conditions["global_trend"] == "POSITIVE" and market_conditions["volatility"] == "LOW":
    market_mood = "Confidence (भरोसे का माहौल)"
    trend_strength = "Strong Trend"
else:
    market_mood = "Neutral (ना डर, ना ज्यादा भरोसा)"
    trend_strength = "Sideways / Mixed Trend"

print(f"- Market Mood: {market_mood}")
print(f"- Trend Strength: {trend_strength}")

# -------- SECTOR SUMMARY --------
print("")
print("Sector-wise Summary:")
sector_count = {}

for stock in stocks:
    data = fundamental_data.get(stock, {})
    sector = data.get("sector", "NA")
    sector_count[sector] = sector_count.get(sector, 0) + 1

for sector, count in sector_count.items():
    print(f"- {sector} sector से {count} कंपनी चुनी गई")

# -------- COMPANY DETAILS --------
print("")
print("नीचे चुनी गई कंपनियों का विवरण दिया गया है:")
print("")

company_no = 1
for stock in stocks:
    data = fundamental_data.get(stock, {})

    print("====================================")
    print(f"Company {company_no}: {stock}")
    print("------------------------------------")
    print(f"Sector          : {data.get('sector')}")
    print(f"Sales           : {data.get('sales')}")
    print(f"Profit          : {data.get('profit')}")
    print(f"Debt            : {data.get('debt')}")
    print(f"Promoter Holding: {data.get('promoter_holding')}%")
    print(f"FII Holding     : {data.get('fii_holding')}%")
    print(f"Risk Level      : {data.get('risk')}")
    print("")

    print("चुनने का कारण:")
    if data.get("risk") == "LOW":
        print("- कंपनी का बिज़नेस कम जोखिम वाला है")
    else:
        print("- कंपनी का जोखिम मध्यम स्तर का है")

    if str(data.get("debt")).startswith("0"):
        print("- कंपनी पर कर्ज नहीं है")
    else:
        print("- कंपनी पर कर्ज मौजूद है")

    if "Cr" in str(data.get("profit")):
        print("- कंपनी मुनाफे में चल रही है")
    else:
        print("- कंपनी का मुनाफा कमजोर है")

    print("")
    company_no += 1

print("====================================")
print("नोट: यह रिपोर्ट केवल जानकारी के लिए है।")
