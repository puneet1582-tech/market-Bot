"""
PHASE-2 REAL CORE
10 YEAR FUNDAMENTAL INGESTION ENGINE (PILOT 200 STOCKS)

Institutional-grade architecture
Streaming write
No memory overload
Clean numeric enforcement
"""

import os
import logging
import pandas as pd
import yfinance as yf
from datetime import datetime

logging.basicConfig(level=logging.INFO)

UNIVERSE_FILE = "data/nse_universe_pilot.csv"
OUTPUT_FILE = "data/fundamentals_10y_pilot.csv"


def load_symbols():
    df = pd.read_csv(UNIVERSE_FILE)
    return df["symbol"].tolist()


def fetch_10y_fundamentals(symbol):
    try:
        ticker = yf.Ticker(symbol + ".NS")
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow

        if financials.empty:
            return None

        years = financials.columns[:10]

        records = []

        for year in years:
            revenue = financials.loc["Total Revenue", year] if "Total Revenue" in financials.index else 0
            net_profit = financials.loc["Net Income", year] if "Net Income" in financials.index else 0
            debt = balance_sheet.loc["Total Debt", year] if "Total Debt" in balance_sheet.index else 0
            cash_flow = cashflow.loc["Operating Cash Flow", year] if "Operating Cash Flow" in cashflow.index else 0

            roe = 0
            if "Total Stockholder Equity" in balance_sheet.index and net_profit != 0:
                equity = balance_sheet.loc["Total Stockholder Equity", year]
                if equity != 0:
                    roe = net_profit / equity * 100

            records.append({
                "symbol": symbol,
                "year": year.year,
                "revenue": float(revenue) if pd.notna(revenue) else 0,
                "net_profit": float(net_profit) if pd.notna(net_profit) else 0,
                "debt": float(debt) if pd.notna(debt) else 0,
                "cash_flow": float(cash_flow) if pd.notna(cash_flow) else 0,
                "roe": float(roe),
                "computed_time": datetime.utcnow()
            })

        return records

    except Exception as e:
        logging.warning(f"{symbol} failed: {e}")
        return None


def run_fundamental_10y_pilot():

    logging.info("10Y FUNDAMENTAL PILOT ENGINE STARTED")

    symbols = load_symbols()
    logging.info(f"Total symbols: {len(symbols)}")

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    header_written = False

    for i, symbol in enumerate(symbols):
        logging.info(f"Processing {i+1}/{len(symbols)} : {symbol}")

        records = fetch_10y_fundamentals(symbol)

        if records:
            df = pd.DataFrame(records)

            df.to_csv(
                OUTPUT_FILE,
                mode='a',
                index=False,
                header=not header_written
            )

            header_written = True

    logging.info("10Y FUNDAMENTAL PILOT COMPLETED")


# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    run_fundamental_10y_pilot()
