from engines.crisis_capital_shield_engine import CrisisCapitalShieldEngine

_engine = CrisisCapitalShieldEngine()

def apply_crisis_shield(dashboard):
    try:
        dashboard["crisis_capital_shield"] = _engine.apply_shield(dashboard)
    except Exception as e:
        dashboard["crisis_shield_error"] = str(e)

    return dashboard
