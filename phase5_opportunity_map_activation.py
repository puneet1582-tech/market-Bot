from engines.global_sector_stock_map_engine import GlobalSectorStockMapEngine

_map_engine = GlobalSectorStockMapEngine()

def apply_opportunity_map(dashboard):
    try:
        dashboard["global_sector_stock_map"] = _map_engine.build_map(dashboard)
    except Exception as e:
        dashboard["opportunity_map_error"] = str(e)

    return dashboard
