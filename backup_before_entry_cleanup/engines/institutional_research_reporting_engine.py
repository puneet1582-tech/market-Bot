"""
Ultimate Brain — Institutional Research Reporting Engine
Generates Investor Memo, Committee Note, and Opportunity Map automatically
"""

from datetime import datetime


class InstitutionalResearchReportingEngine:

    def generate_reports(self, dashboard):
        timestamp = datetime.utcnow().isoformat()

        investor_memo = {
            "timestamp": timestamp,
            "market_mode": dashboard.get("regime_probability", {}),
            "top_opportunities": dashboard.get("probability_enriched_stocks", [])[:10]
        }

        committee_note = {
            "timestamp": timestamp,
            "sector_leaders": dashboard.get("sector_leaders", []),
            "capital_flow": dashboard.get("capital_flow", {}),
            "risk_summary": dashboard.get("portfolio_attribution", {})
        }

        opportunity_map = dashboard.get("market_mode_classification", {})

        return {
            "investor_memo": investor_memo,
            "committee_note": committee_note,
            "opportunity_map": opportunity_map
        }
