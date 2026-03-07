class GlobalImpactEngine:

    def analyze_event(self, event_type, sector_profile, company_profile):
        """
        event_type: str (War, Oil Spike, Dollar Surge, Rate Hike, Recession)
        sector_profile: dict (sector sensitivity configuration)
        company_profile: dict (revenue mix, import/export exposure, fx debt etc.)
        """

        sector_impact = self._sector_impact(event_type, sector_profile)
        stock_exposure = self._stock_exposure(sector_impact, company_profile)

        return {
            "event": event_type,
            "sector_impact_percent": sector_impact,
            "stock_exposure_percent": stock_exposure,
            "risk_category": self._risk_category(stock_exposure)
        }

    def _sector_impact(self, event_type, sector_profile):
        sensitivity = sector_profile.get("event_sensitivity", {})
        return sensitivity.get(event_type, 0)

    def _stock_exposure(self, sector_impact, company_profile):
        exposure_weight = company_profile.get("exposure_weight", 1.0)
        return round(sector_impact * exposure_weight, 2)

    def _risk_category(self, exposure):
        if abs(exposure) >= 20:
            return "High Sensitivity"
        elif abs(exposure) >= 10:
            return "Moderate Sensitivity"
        else:
            return "Low Sensitivity"


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
