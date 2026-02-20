from engines.opportunity_memory_engine import OpportunityMemoryEngine

_memory_engine = OpportunityMemoryEngine()

def apply_memory_layer(dashboard):
    try:
        stocks = dashboard.get("adaptive_enriched_stocks", [])
        dashboard["opportunity_memory"] = _memory_engine.update_memory(stocks)
    except Exception as e:
        dashboard["memory_error"] = str(e)

    return dashboard
