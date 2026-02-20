from engines.capital_deployment_decision_engine import CapitalDeploymentDecisionEngine

_engine = CapitalDeploymentDecisionEngine()

def apply_capital_deployment(dashboard):
    try:
        dashboard["capital_deployment_plan"] = _engine.generate_execution_plan(dashboard)
    except Exception as e:
        dashboard["capital_deployment_error"] = str(e)

    return dashboard
