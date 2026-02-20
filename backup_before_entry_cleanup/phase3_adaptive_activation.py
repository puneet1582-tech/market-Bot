from engines.adaptive_learning_engine import AdaptiveLearningEngine

_adaptive_engine = AdaptiveLearningEngine()

def apply_adaptive_learning(dashboard):
    try:
        stocks = dashboard.get("probability_enriched_stocks", [])
        performance_log = dashboard.get("performance_log", {})
        dashboard["adaptive_enriched_stocks"] = _adaptive_engine.adjust_scores(
            stocks, performance_log
        )
    except Exception as e:
        dashboard["adaptive_error"] = str(e)

    return dashboard
