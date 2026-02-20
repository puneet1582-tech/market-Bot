from engines.multicycle_capital_allocation_engine import MultiCycleCapitalAllocationEngine

_engine = MultiCycleCapitalAllocationEngine()

def apply_multicycle_allocation(dashboard):
    try:
        dashboard["multicycle_capital_allocation"] = _engine.optimize(dashboard)
    except Exception as e:
        dashboard["multicycle_allocation_error"] = str(e)

    return dashboard
