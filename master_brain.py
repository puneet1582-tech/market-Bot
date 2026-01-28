from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("🧠 ULTIMATE BRAIN DAILY REPORT")
print("================================")
print(f"आज का MODE: {mode}")
print("")

print("Market की स्थिति:")
count = 1
if market_conditions["volatility"] == "HIGH":
    print(f"{count}) Volatility ज्यादा है")
    count += 1
if market_conditions["liquidity"] == "LOW":
    print(f"{count}) Liquidity कम है")
    count += 1
if market_conditions["global_trend"] == "NEGATIVE":
    print(f"{count}) Global trend negative है")
    count += 1

print("")
print("चुनी गई कंपनियाँ (Fundamental + कारण):")
print("")

num = 1
for stock in stocks:
    data = fundamental_data.get(stock, {})

    print(f"{num}. कंपनी का नाम: {stock}")
    print(f"   1) Sector: {data.get('sector')}")
    print(f"   2) Sales: {data.get('sales')}")
    print(f"   3) Profit: {data.get('profit')}")

    debt = data.get("debt", 0)
    if debt == 0:
        print("   4) Debt: 0 (Debt free)")
    else:
        print(f"   4) Debt: {debt}")

    print(f"   5) Promoter Holding: {data.get('promoter_holding')}%")
    print(f"   6) FII Holding: {data.get('fii_holding')}%")
    print(f"   7) Risk Level: {data.get('risk')}")

    # WHY LOGIC
    reasons = []
    if data.get("risk") == "LOW":
        reasons.append("Low risk business")
    if data.get("debt") == 0:
        reasons.append("Debt free company")
    if data.get("profit", 0) > 30000:
        reasons.append("Strong profit")

    reason_text = ", ".join(reasons)
    print(f"   8) क्यों चुनी गई: {reason_text}")

    print("")
    num += 1
