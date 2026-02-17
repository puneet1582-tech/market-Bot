from engines.risk_governance_engine import RiskGovernanceEngine

_engine = RiskGovernanceEngine()

def apply_risk_governance(dashboard):
    try:
        dashboard["risk_governed_portfolio"] = _engine.apply_risk_controls(dashboard)
    except Exception as e:
        dashboard["risk_governance_error"] = str(e)

    return dashboard
