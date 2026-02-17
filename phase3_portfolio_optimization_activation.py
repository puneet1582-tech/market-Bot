from engines.self_improving_portfolio_engine import SelfImprovingPortfolioEngine

_optimizer = SelfImprovingPortfolioEngine()

def apply_portfolio_optimization(dashboard):
    try:
        allocation = dashboard.get("portfolio_allocation", {})
        adaptive = dashboard.get("adaptive_enriched_stocks", [])
        dashboard["optimized_portfolio_allocation"] = _optimizer.optimize(allocation, adaptive)
    except Exception as e:
        dashboard["portfolio_optimization_error"] = str(e)

    return dashboard
