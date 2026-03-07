from real_intelligence_layer.master_intelligence_engine import MasterIntelligenceEngine
import pandas as pd

company_data = {
    "financials": pd.DataFrame({
        "revenue": [100, 120, 150],
        "net_profit": [10, 15, 25],
        "total_debt": [50, 45, 40],
        "operating_cashflow": [12, 18, 28],
        "roe": [12, 14, 16],
        "roce": [15, 17, 19]
    }),
    "ownership": {
        "promoter": [50, 52, 55],
        "fii": [10, 12, 15],
        "dii": [8, 9, 11],
        "pledge": 5
    },
    "sector": {
        "policy_support": "Positive",
        "cyclical_status": "Structural Growth",
        "commodity_exposure": "Low"
    },
    "macro": {
        "interest_rate_trend": "Stable",
        "dollar_index_trend": "Weakening",
        "oil_price_trend": "Stable",
        "geopolitical_risk": "Moderate"
    },
    "liquidity": "High",
    "volatility": "Low",

    # NEW GLOBAL EVENT TEST DATA
    "event_type": "War",
    "sector_profile": {
        "event_sensitivity": {
            "War": -18,
            "Oil Spike": -12,
            "Dollar Surge": 5
        }
    },
    "company_profile": {
        "exposure_weight": 0.6
    }
}

engine = MasterIntelligenceEngine()
report = engine.run_full_analysis(company_data)

print("\n===== REAL INTELLIGENCE REPORT WITH GLOBAL IMPACT =====")
print(report)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
