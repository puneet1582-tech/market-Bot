# DECISION SUMMARY ENGINE
# Generates final institutional action summary

def generate_decision_summary(conviction_ranked, allocation):
    try:
        top = conviction_ranked[:5]

        summary_lines = []
        summary_lines.append("FINAL INSTITUTIONAL ACTION SUMMARY:")

        for stock in top:
            symbol = stock["symbol"]
            confidence = stock.get("confidence_percent", 0)

            alloc = next(
                (a["allocation_percent"] for a in allocation if a["symbol"] == symbol),
                0
            )

            line = f"{symbol} → Suggested Allocation: {alloc}% | Confidence: {confidence}%"
            summary_lines.append(line)

        return "\n".join(summary_lines)

    except Exception as e:
        print("Decision summary error:", e)
        return ""
