class GlobalMacroMappingEngine:

    def analyze(self, macro_data):
        result = {}

        result["interest_rate_impact"] = macro_data.get("interest_rate_trend", "Neutral")
        result["dollar_impact"] = macro_data.get("dollar_index_trend", "Neutral")
        result["oil_impact"] = macro_data.get("oil_price_trend", "Neutral")
        result["geopolitical_risk"] = macro_data.get("geopolitical_risk", "Moderate")

        return result
