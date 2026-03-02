import pandas as pd

class BusinessEvolutionEngine:

    def analyze(self, df):
        result = {}

        result["revenue_trend"] = self._trend(df.get("revenue"))
        result["profit_trend"] = self._trend(df.get("net_profit"))
        result["debt_trend"] = self._trend(df.get("total_debt"))
        result["cashflow_quality"] = self._trend(df.get("operating_cashflow"))
        result["roe_stability"] = self._stability(df.get("roe"))
        result["roce_stability"] = self._stability(df.get("roce"))

        return result

    def _trend(self, series):
        if series is None or len(series) < 2:
            return "Insufficient Data"
        if series.iloc[-1] > series.iloc[0]:
            return "Uptrend"
        elif series.iloc[-1] < series.iloc[0]:
            return "Downtrend"
        else:
            return "Flat"

    def _stability(self, series):
        if series is None:
            return "Insufficient Data"
        return "Stable" if series.std() < 5 else "Volatile"
