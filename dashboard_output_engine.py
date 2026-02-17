# DASHBOARD OUTPUT ENGINE
# Creates structured intelligence dashboard output

def build_dashboard(mode_report, sector_scores, ranked, perf_summary, return_summary):
    dashboard = {
        "market_mode": mode_report,
        "sector_strength": sector_scores,
        "top_opportunities": ranked[:5],
        "performance_summary": perf_summary,
        "return_estimation": return_summary
    }

    return dashboard
