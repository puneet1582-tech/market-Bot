from engines.strategic_decision_engine import StrategicDecisionEngine

_strategy_engine = StrategicDecisionEngine()

def apply_strategy_layer(dashboard):
    try:
        dashboard["strategic_decision"] = _strategy_engine.generate_strategy(dashboard)
    except Exception as e:
        dashboard["strategy_error"] = str(e)

    return dashboard


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
