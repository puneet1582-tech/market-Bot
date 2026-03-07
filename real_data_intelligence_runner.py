import pandas as pd
from real_intelligence_layer.master_intelligence_engine import MasterIntelligenceEngine

SYMBOL = "RELIANCE"   # <<< Change symbol here if needed

def load_financials(symbol):
    q = pd.read_csv("data/quarterly_fundamentals_clean.csv")
    q = q[q["symbol"] == symbol].sort_values("date")
    return q.tail(12)  # last 12 quarters

def load_ownership(symbol):
    promoter = pd.read_csv("data/promoter_holdings.csv")
    fii_dii = pd.read_csv("data/fii_dii.csv")

    p = promoter[promoter["symbol"] == symbol].sort_values("date").tail(4)
    f = fii_dii[fii_dii["symbol"] == symbol].sort_values("date").tail(4)

    return {
        "promoter": p["holding_percent"].tolist() if not p.empty else [],
        "fii": f["fii_percent"].tolist() if not f.empty else [],
        "dii": f["dii_percent"].tolist() if not f.empty else [],
        "pledge": p["pledge_percent"].iloc[-1] if not p.empty else 0
    }

def load_sector(symbol):
    sector_map = pd.read_csv("data/sector/sector_mapping.csv")
    row = sector_map[sector_map["symbol"] == symbol]
    if row.empty:
        return {}
    return {
        "policy_support": "Neutral",
        "cyclical_status": "Structural Growth",
        "commodity_exposure": "Moderate"
    }

def load_macro():
    return {
        "interest_rate_trend": "Stable",
        "dollar_index_trend": "Stable",
        "oil_price_trend": "Stable",
        "geopolitical_risk": "Moderate"
    }

def load_global_event():
    events = pd.read_csv("data/global/global_events.csv")
    if events.empty:
        return None, {}, {}

    latest = events.sort_values("date").iloc[-1]
    event_type = latest["event_type"]

    sector_profile = {
        "event_sensitivity": {
            event_type: latest.get("sector_impact_percent", 0)
        }
    }

    company_profile = {
        "exposure_weight": 0.7
    }

    return event_type, sector_profile, company_profile

def build_company_data(symbol):
    financials = load_financials(symbol)
    ownership = load_ownership(symbol)
    sector = load_sector(symbol)
    macro = load_macro()
    event_type, sector_profile, company_profile = load_global_event()

    company_data = {
        "financials": financials,
        "ownership": ownership,
        "sector": sector,
        "macro": macro,
        "liquidity": "High",
        "volatility": "Low"
    }

    if event_type:
        company_data["event_type"] = event_type
        company_data["sector_profile"] = sector_profile
        company_data["company_profile"] = company_profile

    return company_data

# disabled_entry_point
    engine = MasterIntelligenceEngine()
    data = build_company_data(SYMBOL)
    report = engine.run_full_analysis(data)

    print("\n===== REAL DATA INTELLIGENCE REPORT =====")
    print(report)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
