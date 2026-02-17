from engines.self_improvement_trigger_engine import SelfImprovementTriggerEngine

_engine = SelfImprovementTriggerEngine()

def apply_self_improvement(dashboard):
    try:
        dashboard["self_improvement_signal"] = _engine.trigger(dashboard)
    except Exception as e:
        dashboard["self_improvement_error"] = str(e)

    return dashboard
