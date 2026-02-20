"""
Ultimate Brain — Phase-2 Classification Activation
Adds INVEST / TRADE / DEFENSIVE classification to dashboard
"""

from engines.institutional_classification_engine import InstitutionalClassificationEngine

_classifier = InstitutionalClassificationEngine()

def apply_classification(dashboard):
    try:
        enriched = dashboard.get("probability_enriched_stocks", [])
        dashboard["market_mode_classification"] = _classifier.classify(enriched)
    except Exception as e:
        dashboard["classification_error"] = str(e)

    return dashboard
