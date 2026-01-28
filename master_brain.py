from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data

mode = decide_mode(market_conditions)
stocks = select_stocks(mode)

print("🧠 ULTIMATE BRAIN DAILY REPORT")
print("--------------------------------")
print(f"आज का MODE: {mode}")
print("")

print("Market की स्थिति:")
if market_conditions["volatility"] == "HIGH":
    print("1) Volatility ज्यादा है")
if market_conditions["liquidity"] == "LOW":
    print("2) Liquidity कम है")
if market_conditions["global_trend"] == "NEGATIVE":
    print("3) Global trend negative है")

print("")
print("चुनी गई कंपनियाँ और कारण:")
print("")

num = 1
for stock in stocks:
    data = fundamental_data.get(stock, {})

    print(f"{num}. कंपनी का नाम: {stock}")

    # Risk
    print(f"   1) Risk Level: {data.get('risk')}")

    # Debt
    debt = data.get("debt", 0)
    if debt == 0:
        print("   2) Debt: 0 (Debt free)")
    else:
        print(f"   2) Debt: {debt}")

    # Profit
    profit = data.get("profit", 0)
    if profit > 30000:
        print(f"   3) Profit: Strong ({profit})")
    else:
        print(f"   3) Profit: Normal ({profit})")

    print("")  # खाली लाइन हर कंपनी के बाद
    num += 1
