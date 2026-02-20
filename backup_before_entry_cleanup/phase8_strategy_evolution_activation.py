from engines.strategy_evolution_engine import StrategyEvolutionEngine

_engine = StrategyEvolutionEngine()

def apply_strategy_evolution(dashboard):
    try:
        dashboard["strategy_evolution_signal"] = _engine.evolve(dashboard)
    except Exception as e:
        dashboard["strategy_evolution_error"] = str(e)

    return dashboard
