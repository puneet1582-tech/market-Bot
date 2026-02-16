

import time
import brain_engine
from engines.telegram_alert_engine import send_telegram_alert

engine = brain_engine.BrainEngine()
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]

while True:
    for s in stocks:
        result = engine.analyze_stock(s)
        send_telegram_alert(str(result))
        print("TELEGRAM SENT:", result)

    time.sleep(300)

