
from mode_brain import decide_mode, market_conditions
from stock_selector import select_stocks
from fundamental_brain import fundamental_data
from explanation_brain import explain_mode, explain_stock

# 1. Decide Mode
mode = decide_mode(market_conditions)
print("ACTIVE MODE:", mode)

# 2. Select Stocks based on mode
selected_stocks = select_stocks(mode)
print("SELECTED STOCKS:", selected_stocks)

# 3. Explain Mode
mode_explanation = explain_mode(market_conditions, mode)
print(mode_explanation)

# 4. Explain each selected stock
for stock in selected_stocks:
    data = fundamental_data.get(stock, {})
    if data:
        stock_explanation = explain_stock(stock, data, mode)
        print(stock_explanation)
