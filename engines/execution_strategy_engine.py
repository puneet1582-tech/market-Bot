"""
Ultimate Brain — Institutional Execution Strategy Engine
Generates final execution strategy including staggered buying plan.
"""

from datetime import datetime


def generate_execution_plan(opportunity_list, timing_decision):
    """
    opportunity_list:
    list of symbols selected for deployment

    timing_decision:
    DEPLOY / STAGGER / WAIT
    """

    plan = []

    for sym in opportunity_list:
        if timing_decision == "DEPLOY":
            steps = 1
        elif timing_decision == "STAGGER":
            steps = 3
        else:
            steps = 0

        plan.append({
            "symbol": sym,
            "execution_steps": steps,
            "execution_mode": timing_decision
        })

    return {
        "timestamp": str(datetime.utcnow()),
        "execution_plan": plan
    }
