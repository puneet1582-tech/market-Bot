"""
Ultimate Brain — Phase-2 Pipeline Integration
Safely integrates orchestration output into dashboard pipeline
"""

from engines.intelligence_orchestrator_engine import IntelligenceOrchestrator

orchestrator = IntelligenceOrchestrator()


def apply_phase2_intelligence(dashboard, conviction_ranked,
                             regime_score, sector_scores, volatility):
    try:
        result = orchestrator.run(
            conviction_ranked,
            regime_score,
            sector_scores,
            volatility
        )

        dashboard["global_snapshot"] = result["snapshot"]
        dashboard["probability_enriched_stocks"] = result["stocks"]

    except Exception as e:
        dashboard["phase2_error"] = str(e)

    return dashboard
