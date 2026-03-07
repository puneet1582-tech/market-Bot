import pandas as pd
import numpy as np

class BusinessEvolutionEngine:

    def analyze(self, df):
        result = {}

        if df is None or len(df) < 3:
            return {"error": "Insufficient financial history"}

        result["revenue_cagr"] = float(self._cagr(df["revenue"]))
        result["profit_cagr"] = float(self._cagr(df["net_profit"]))
        result["debt_change_percent"] = float(self._percent_change(df["total_debt"]))
        result["cashflow_consistency"] = self._cashflow_consistency(df)
        result["roe_trend"] = self._trend(df["roe"])
        result["roce_trend"] = self._trend(df["roce"])
        result["earnings_volatility"] = float(self._volatility(df["net_profit"]))
        result["margin_trend"] = self._margin_trend(df)

        result["structural_interpretation"] = self._interpret(result)

        return result

    def _cagr(self, series):
        start = float(series.iloc[0])
        end = float(series.iloc[-1])
        periods = len(series) - 1
        if start <= 0:
            return 0.0
        return round(((end / start) ** (1 / periods) - 1) * 100, 2)

    def _percent_change(self, series):
        start = float(series.iloc[0])
        end = float(series.iloc[-1])
        if start == 0:
            return 0.0
        return round(((end - start) / abs(start)) * 100, 2)

    def _cashflow_consistency(self, df):
        positive_years = int((df["operating_cashflow"] > 0).sum())
        total_years = len(df)
        percent = round((positive_years / total_years) * 100, 2)
        return f"{percent}% Positive"

    def _trend(self, series):
        if float(series.iloc[-1]) > float(series.iloc[0]):
            return "Improving"
        elif float(series.iloc[-1]) < float(series.iloc[0]):
            return "Declining"
        else:
            return "Flat"

    def _volatility(self, series):
        return round(float(series.std()), 2)

    def _margin_trend(self, df):
        margin_start = float(df["net_profit"].iloc[0] / df["revenue"].iloc[0])
        margin_end = float(df["net_profit"].iloc[-1] / df["revenue"].iloc[-1])
        if margin_end > margin_start:
            return "Expanding"
        elif margin_end < margin_start:
            return "Contracting"
        else:
            return "Stable"

    def _interpret(self, data):
        if (
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


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
