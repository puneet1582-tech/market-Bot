import pandas as pd

from engines.classifier import classify_stock
from engines.fundamentals import fundamental_score
from engines.decision import final_decision
from engines.news import news_score
from engines.future import future_sector_score
from engines.risk import risk_engine
from engines.why import why_engine

# Load data
stocks = pd.read_csv("data/stocks.csv")
fund = pd.read_csv("data/fundamentals.csv")
news = pd.read_csv("data/news.csv")
future = pd.read_csv("data/future_sectors.csv")

# Merge data
df = stocks.merge(fund, on="symbol")
df = df.merge(news, on=["symbol", "sector"], how="left")
df = df.merge(future, on="sector", how="left")

print("\n=== COMPLETE TRADING BOT OUTPUT ===\n")

# Dashboard buckets
buy_list = []
speculative_list = []
wait_list = []
avoid_list = []

for _, row in df.iterrows():
    category = classify_stock(row)

    f_score = fundamental_score(row)
    n_score = news_score(row) if pd.notna(row["news_type"]) else 0
    fut_score = future_sector_score(row)

    total_score = f_score + n_score + fut_score
    decision = final_decision(total_score, category)

    risk, position = risk_engine(row, category)
    why = why_engine(row, decision, risk)

    print(f"STOCK: {row['symbol']}")
    print(f"ACTION: {decision}")
    print(f"WHY: {why}")
    print("-" * 45)

    # ✅ FIXED LOGIC
    if "SPECULATIVE" in decision:
        speculative_list.append(row["symbol"])
    elif decision == "BUY":
        buy_list.append(row["symbol"])
    elif decision == "WAIT":
        wait_list.append(row["symbol"])
    else:
        avoid_list.append(row["symbol"])

print("\n=== DAILY DASHBOARD ===")
print("🟢 BUY :", buy_list)
print("🟠 SPECULATIVE :", speculative_list)
print("🟡 WAIT :", wait_list)
print("🔴 AVOID :", avoid_list)

