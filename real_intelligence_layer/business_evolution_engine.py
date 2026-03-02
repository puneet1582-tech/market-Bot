import pandas as pd
import numpy as np

class BusinessEvolutionEngine:

    def analyze(self, df):
        result = {}

        if df is None or len(df) < 3:
            return {"error": "Insufficient financial history"}

        result["revenue_cagr"] = self._cagr(df["revenue"])
        result["profit_cagr"] = self._cagr(df["net_profit"])
        result["debt_change_percent"] = self._percent_change(df["total_debt"])
        result["cashflow_consistency"] = self._cashflow_consistency(df)
        result["roe_trend"] = self._trend(df["roe"])
        result["roce_trend"] = self._trend(df["roce"])
        result["earnings_volatility"] = self._volatility(df["net_profit"])
        result["margin_trend"] = self._margin_trend(df)

        result["structural_interpretation"] = self._interpret(result)

        return result

    def _cagr(self, series):
        start = series.iloc[0]
        end = series.iloc[-1]
        periods = len(series) - 1
        if start <= 0:
            return "Invalid Start Value"
        cagr = ((end / start) ** (1 / periods) - 1) * 100
        return round(cagr, 2)

    def _percent_change(self, series):
        return round(((series.iloc[-1] - series.iloc[0]) / abs(series.iloc[0])) * 100, 2)

    def _cashflow_consistency(self, df):
        positive_years = (df["operating_cashflow"] > 0).sum()
        total_years = len(df)
        return f"{round((positive_years/total_years)*100,2)}% Positive"

    def _trend(self, series):
        if series.iloc[-1] > series.iloc[0]:
            return "Improving"
        elif series.iloc[-1] < series.iloc[0]:
            return "Declining"
        else:
            return "Flat"

    def _volatility(self, series):
        return round(series.std(), 2)

    def _margin_trend(self, df):
        margin = df["net_profit"] / df["revenue"]
        if margin.iloc[-1] > margin.iloc[0]:
            return "Expanding"
        elif margin.iloc[-1] < margin.iloc[0]:
            return "Contracting"
        else:
            return "Stable"

    def _interpret(self, data):
        if (
            isinstance(data["revenue_cagr"], (int, float)) and
            isinstance(data["profit_cagr"], (int, float)) and
            data["revenue_cagr"] > 12 and
            data["profit_cagr"] > 15 and
            data["margin_trend"] == "Expanding" and
            "Positive" in data["cashflow_consistency"]
        ):
            return "High Probability Structural Compounder"
        elif data["earnings_volatility"] > 20:
            return "Cyclical / Volatile Business"
        else:
            return "Stable but Moderate Growth Business"
