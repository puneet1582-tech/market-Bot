import requests
import os
import re
import json
import time
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
    "Accept-Language": "en-US,en;q=0.9"
}

REPORT = {
    "timestamp": str(datetime.now()),
    "price_fetch": False,
    "index_fetch": False,
    "commodity_fetch": False,
    "nse_fetch": False,
    "multi_symbol_batch": False,
    "telegram_live": False,
    "intelligence_trigger": False,
    "system_status": ""
}

def fetch_price(symbol):
    try:
        url = f"https://finance.yahoo.com/quote/{symbol}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            if "QuoteSummaryStore" in r.text:
                return True
    except:
        pass
    return False

def fetch_batch(symbols):
    success = 0
    for s in symbols:
        if fetch_price(s):
            success += 1
        time.sleep(1)
    return success >= 2

def fetch_commodity():
    return fetch_price("CL=F") and fetch_price("GC=F")

def fetch_index():
    return fetch_price("%5EGSPC")

def fetch_nse():
    try:
        r = requests.get("https://www.nseindia.com", headers=HEADERS, timeout=10)
        return r.status_code == 200
    except:
        return False

def telegram_test():
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, data={"chat_id": chat_id, "text": "Institutional Live Stabilizer Test"})
        return r.status_code == 200
    except:
        return False

print("STARTING INSTITUTIONAL LIVE STABILIZER...\n")

REPORT["price_fetch"] = fetch_price("RELIANCE.NS")
REPORT["index_fetch"] = fetch_index()
REPORT["commodity_fetch"] = fetch_commodity()
REPORT["nse_fetch"] = fetch_nse()
REPORT["multi_symbol_batch"] = fetch_batch(["RELIANCE.NS","TCS.NS","INFY.NS"])
REPORT["telegram_live"] = telegram_test()

# Intelligence trigger simulation
if REPORT["price_fetch"] and REPORT["commodity_fetch"]:
    REPORT["intelligence_trigger"] = True

score = sum([1 for k,v in REPORT.items() if v == True])
if score >= 5:
    REPORT["system_status"] = "LIVE DATA ENGINE STABLE"
elif score >= 3:
    REPORT["system_status"] = "PARTIAL STABILITY - NEEDS HARDENING"
else:
    REPORT["system_status"] = "LIVE DATA ENGINE FAILED"

with open("INSTITUTIONAL_LIVE_REPORT.json", "w") as f:
    json.dump(REPORT, f, indent=4)

print("======================================")
print("INSTITUTIONAL LIVE STABILIZATION DONE")
print("======================================")
for k,v in REPORT.items():
    print(k, ":", v)
print("Report saved as INSTITUTIONAL_LIVE_REPORT.json")
print("======================================")
