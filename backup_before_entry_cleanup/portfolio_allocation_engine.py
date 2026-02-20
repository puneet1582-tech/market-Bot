# PORTFOLIO ALLOCATION ENGINE
# Suggests allocation weights based on conviction scores

def generate_portfolio_allocation(conviction_ranked, top_n=10):
    try:
        selected = conviction_ranked[:top_n]

        total_score = sum([s.get("conviction_score", 0) for s in selected])

        allocation = []

        for s in selected:
            weight = 0
            if total_score > 0:
                weight = round((s.get("conviction_score", 0) / total_score) * 100, 2)

            allocation.append({
                "symbol": s["symbol"],
                "allocation_percent": weight
            })

        return allocation

    except Exception as e:
        print("Allocation error:", e)
        return []
