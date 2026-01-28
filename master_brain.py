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

