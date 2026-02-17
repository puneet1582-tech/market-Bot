from engines.global_market_linkage_engine import GlobalMarketLinkageEngine

_link_engine = GlobalMarketLinkageEngine()

def apply_global_linkage(dashboard):
    try:
        global_indices = dashboard.get("global_indices", {})
        dashboard["global_market_linkage"] = _link_engine.compute_linkage(global_indices)
    except Exception as e:
        dashboard["linkage_error"] = str(e)

    return dashboard
