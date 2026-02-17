# FINAL REPORT FORMATTER ENGINE
# Standardizes institutional report output

def format_final_report(dashboard):
    try:
        report_lines = []

        mode = dashboard.get("mode", {}).get("mode", "TRADE")
        regime = dashboard.get("regime_probability", {})

        report_lines.append(f"MARKET MODE: {mode}")
        report_lines.append(
            f"Regime Probabilities → Bull: {regime.get('bull_probability',0)}% | "
            f"Bear: {regime.get('bear_probability',0)}% | "
            f"Sideways: {regime.get('sideways_probability',0)}%"
        )

        report_lines.append("\nHIGH CONVICTION STOCKS:")
        for stock in dashboard.get("portfolio_allocation", [])[:5]:
            report_lines.append(
                f"{stock['symbol']} → Allocation: {stock['allocation_percent']}%"
            )

        decision_summary = dashboard.get("decision_summary", "")
        if decision_summary:
            report_lines.append("\n" + decision_summary)

        return "\n".join(report_lines)

    except Exception as e:
        print("Final report format error:", e)
        return "Report formatting error"
