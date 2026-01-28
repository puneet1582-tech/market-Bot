import pandas as pd
import math

DATA_PATH = "data/quarterly_fundamentals.csv"

class FundamentalEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def get_stock_data(self, symbol):
        df = self.df[self.df["symbol"] == symbol]

        if df.empty:
            return None, False
        is_complete = len(df) >= 12
        return df.tail(12), is_complete

    def is_invalid(self, series):
        return series.isnull().any() or series.apply(lambda x: isinstance(x, float) and math.isnan(x)).any()

    def trend(self, series):
        if self.is_invalid(series) or len(series) < 2:
            return "INVALID"
        mid = len(series) // 2
        old = series.iloc[:mid].mean()
        new = series.iloc[mid:].mean()
        if new > old:
            return "UP"
        elif new < old:
            return "DOWN"
        else:
            return "FLAT"

    def debt_trend(self, series):
        if self.is_invalid(series) or len(series) < 2:
            return "INVALID"
        mid = len(series) // 2
        old = series.iloc[:mid].mean()
        new = series.iloc[mid:].mean()
        if new < old:
            return "FALLING"
        else:
            return "RISING"

    def cashflow_strength(self, cashflow, profit):
        if self.is_invalid(cashflow) or self.is_invalid(profit):
            return "INVALID"
        return "STRONG" if cashflow.mean() > profit.mean() else "WEAK"

    def analyze(self, symbol):
        df, is_complete = self.get_stock_data(symbol)

        if df is None:
            return {
                "symbol": symbol,
                "decision": "NO DECISION",
                "reason": "NO DATA"
            }

        sales_trend = self.trend(df["sales"])
        profit_trend = self.trend(df["profit"])
        debt_trend = self.debt_trend(df["debt"])
        cashflow_status = self.cashflow_strength(df["cashflow"], df["profit"])

        # अगर कुछ भी INVALID है → no decision
        if "INVALID" in [sales_trend, profit_trend, debt_trend, cashflow_status]:
            return {
                "symbol": symbol,
                "decision": "NO DECISION",
                "reason": "DATA INVALID (nan or missing)"
            }

        result = {
            "symbol": symbol,
            "quarters_used": len(df),
            "sales_trend": sales_trend,
            "profit_trend": profit_trend,
            "debt_trend": debt_trend,
            "cashflow": cashflow_status
        }

        if not is_complete:
            result["decision"] = "NO DECISION"
            result["reason"] = "INSUFFICIENT HISTORY (< 3 YEARS)"

        return result
