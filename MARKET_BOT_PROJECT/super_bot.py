import pandas as pd
from flask import Flask, render_template_string, request

df = pd.read_csv("data/fundamentals.csv")

# safety columns
if "symbol" not in df.columns: df["symbol"] = "NA"
if "promoter_holding" not in df.columns: df["promoter_holding"] = 0
if "pledge" not in df.columns: df["pledge"] = 0
if "cash_flow_years" not in df.columns: df["cash_flow_years"] = 0
if "debt_trend" not in df.columns: df["debt_trend"] = "unknown"
if "revenue_growth" not in df.columns: df["revenue_growth"] = 0

# Auto sector from revenue_growth (simple logic)
def auto_sector(row):
    if row["revenue_growth"] >= 15:
        return "High Growth"
    elif row["revenue_growth"] >= 8:
        return "Stable Growth"
    else:
        return "Weak Growth"

df["sector"] = df.apply(auto_sector, axis=1)

# -------- GLOBAL + MODE --------
def global_view():
    return {"US": "UP", "Dollar": "STABLE", "Crude": "DOWN"}

def decide_mode():
    g = global_view()
    score = 0
    if g["US"] == "UP": score += 1
    if g["Crude"] == "DOWN": score += 1
    if g["Dollar"] == "STABLE": score += 1
    if score >= 2:
        return "INVEST"
    elif score == 1:
        return "TRADE"
    else:
        return "DEFENSIVE"

# -------- SECTOR ENGINE --------
def sector_strength(sector):
    s = df[df["sector"] == sector]
    return s["revenue_growth"].mean()

# -------- STOCK ENGINE --------
def stock_score(row):
    score = 0
    reason = []

    if row["revenue_growth"] >= 10:
        score += 1; reason.append("Revenue growing")
    if row["promoter_holding"] >= 50:
        score += 1; reason.append("Strong promoter holding")
    if row["pledge"] == 0:
        score += 1; reason.append("No pledge")
    if row["cash_flow_years"] >= 3:
        score += 1; reason.append("Stable cash flow")
    if row["debt_trend"] in ["stable", "reducing", "zero"]:
        score += 1; reason.append("Debt under control")

    return score, ", ".join(reason)

# -------- BRAIN --------
def generate_brain(capital):
    mode = decide_mode()

    sectors = {}
    for sec in df["sector"].unique():
        sectors[sec] = sector_strength(sec)

    best_sectors = sorted(sectors, key=sectors.get, reverse=True)

    stocks = []
    total_score = 0

    for _, row in df.iterrows():
        sc, rs = stock_score(row)
        if sc >= 4:
            decision = "BUY"
        elif sc == 3:
            decision = "WATCH"
        else:
            decision = "AVOID"

        if decision == "BUY":
            total_score += sc

        stocks.append({
            "symbol": row["symbol"],
            "sector": row["sector"],
            "decision": decision,
            "score": sc,
            "reason": rs
        })

    # Capital allocation
    for s in stocks:
        if s["decision"] == "BUY" and total_score > 0:
            s["allocation"] = round(capital * (s["score"] / total_score), 2)
        else:
            s["allocation"] = 0

    return {
        "mode": mode,
        "sectors": best_sectors,
        "stocks": stocks,
        "global_data": global_view()
    }

# -------- APP --------
app = Flask(__name__)

HTML = """
<h2>GLOBAL VIEW</h2>
<p>{{ global_data }}</p>

<h2>MARKET MODE: {{ mode }}</h2>

<h3>TOP SECTORS</h3>
<ul>
{% for s in sectors %}
<li>{{ s }}</li>
{% endfor %}
</ul>

<table border="1" cellpadding="5">
<tr>
<th>Stock</th><th>Sector</th><th>Decision</th>
<th>Score</th><th>Reason</th><th>Capital Allocation</th>
</tr>
{% for s in stocks %}
<tr>
<td>{{ s.symbol }}</td>
<td>{{ s.sector }}</td>
<td>{{ s.decision }}</td>
<td>{{ s.score }}</td>
<td>{{ s.reason }}</td>
<td>{{ s.allocation }}</td>
</tr>
{% endfor %}
</table>
"""

@app.route("/")
def home():
    capital = float(request.args.get("capital", 100000))
    brain = generate_brain(capital)
    return render_template_string(
        HTML,
        mode=brain["mode"],
        sectors=brain["sectors"],
        stocks=brain["stocks"],
        global_data=brain["global_data"]
    )

if __name__ == "__main__":
    app.run(debug=True)
