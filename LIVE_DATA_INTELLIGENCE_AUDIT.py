import os
import json
import requests
import socket
import csv
import time
from datetime import datetime

REPORT = {
    "timestamp": str(datetime.now()),
    "internet_connectivity": False,
    "yahoo_price_test": False,
    "global_index_test": False,
    "commodity_test": False,
    "news_sources_reachable": False,
    "nse_reachable": False,
    "telegram_test": False,
    "price_schema_valid": False,
    "data_files_found": False,
    "system_health_score": 0,
    "missing_capabilities": [],
    "next_action_required": ""
}

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except:
        return False

def test_yahoo_price():
    try:
        r = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=RELIANCE.NS")
        return r.status_code == 200
    except:
        return False

def test_global_index():
    try:
        r = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5EGSPC")
        return r.status_code == 200
    except:
        return False

def test_commodity():
    try:
        r = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=CL=F,GC=F")
        return r.status_code == 200
    except:
        return False

def test_news_sources():
    sources = [
        "https://www.reuters.com",
        "https://www.bloomberg.com",
        "https://www.marketwatch.com"
    ]
    success = 0
    for url in sources:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                success += 1
        except:
            pass
    return success >= 2

def test_nse():
    try:
        r = requests.get("https://www.nseindia.com", timeout=5)
        return r.status_code == 200
    except:
        return False

def validate_price_schema():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".csv"):
                try:
                    with open(os.path.join(root, file), "r") as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        if set(["date","symbol","price"]).issubset(set([h.lower() for h in headers])):
                            return True
                except:
                    pass
    return False

def check_data_files():
    count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".csv") or file.endswith(".json"):
                count += 1
    return count > 5

def test_telegram():
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, data={"chat_id": chat_id, "text": "LIVE AUDIT TEST"})
        return r.status_code == 200
    except:
        return False

print("STARTING LIVE DATA INTELLIGENCE AUDIT...\n")

REPORT["internet_connectivity"] = check_internet()
REPORT["yahoo_price_test"] = test_yahoo_price()
REPORT["global_index_test"] = test_global_index()
REPORT["commodity_test"] = test_commodity()
REPORT["news_sources_reachable"] = test_news_sources()
REPORT["nse_reachable"] = test_nse()
REPORT["price_schema_valid"] = validate_price_schema()
REPORT["data_files_found"] = check_data_files()
REPORT["telegram_test"] = test_telegram()

score = 100
for key in REPORT:
    if isinstance(REPORT[key], bool) and REPORT[key] == False:
        score -= 8

if score < 0:
    score = 0

REPORT["system_health_score"] = score

missing = []
for key, val in REPORT.items():
    if isinstance(val, bool) and val == False:
        missing.append(key)

REPORT["missing_capabilities"] = missing

if score >= 85:
    REPORT["next_action_required"] = "SYSTEM READY FOR MASTER ORCHESTRATION HARDENING"
elif score >= 60:
    REPORT["next_action_required"] = "LIVE DATA LAYER NEEDS FIXING"
else:
    REPORT["next_action_required"] = "CORE LIVE INFRASTRUCTURE BROKEN"

with open("LIVE_DATA_AUDIT_REPORT.json", "w") as f:
    json.dump(REPORT, f, indent=4)

print("========================================")
print("LIVE DATA INTELLIGENCE AUDIT COMPLETE")
print("========================================")
print("System Health Score:", score, "%")
print("Missing Capabilities:", missing)
print("Next Action:", REPORT["next_action_required"])
print("Full Report Saved: LIVE_DATA_AUDIT_REPORT.json")
print("========================================")


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
