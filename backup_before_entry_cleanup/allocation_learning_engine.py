# ADAPTIVE ALLOCATION LEARNING ENGINE
# Adjusts allocation bias based on attribution history

def allocation_learning_adjustment(allocation_list, attribution_data):
    try:
        adjusted = []

        for item in allocation_list:
            symbol = item["symbol"]
            weight = item["allocation_percent"]

            contribution = attribution_data.get(symbol, 0)

            # Positive attribution increases allocation slightly
            if contribution > 0:
                weight = weight * 1.05
            else:
                weight = weight * 0.95

            adjusted.append({
                "symbol": symbol,
                "allocation_percent": round(weight, 2)
            })

        return adjusted

    except Exception as e:
        print("Allocation learning error:", e)
        return allocation_list
