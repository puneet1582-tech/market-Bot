from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data
from explanation_brain import explain_mode, explain_stock

mode = decide_mode(market_conditions)
selected_stocks = select_stocks(mode)

print("🧠 ULTIMATE BRAIN REPORT")
print("------------------------")

print(f"आज का MODE: {mode}")
print("")

print("MODE के कारण:")
if market_conditions["volatility"] == "HIGH":
    print("- Market में volatility ज्यादा है")
if market_conditions["liquidity"] == "LOW":
    print("- Liquidity कम है")
if market_conditions["global_trend"] == "NEGATIVE":
    print("- Global trend negative है")

print("")
print("आज देखने लायक stocks:")

count = 1
for stock in selected_stocks:
    data = fundamental_data.get(stock, {})
    reasons = []

    if data.get("risk") == "LOW":
        reasons.append("Low risk")
    if data.get("debt") == 0:
        reasons.append("Debt free")
    if data.get("profit", 0) > 30000:
        reasons.append("Strong profit")

    reason_text = ", ".join(reasons)
    print(f"{count}) {stock} – {reason_text}")
    count += 1
