# ULTIMATE BRAIN SYSTEM CHECK
# Verifies all major modules are working

print("===== SYSTEM CHECK START =====")

status = {}

# --- Brain Engine ---
try:
    import brain_engine
    status["brain_engine"] = "OK"
except Exception as e:
    status["brain_engine"] = f"ERROR: {e}"

# --- Opportunity Engine ---
try:
    from opportunity_engine import calculate_opportunity
    test = calculate_opportunity("TEST.NS", 1500)
    status["opportunity_engine"] = f"OK | TEST OUTPUT: {test}"
except Exception as e:
    status["opportunity_engine"] = f"ERROR: {e}"

# --- Telegram Engine ---
try:
    from engines.telegram_alert_engine import send_telegram_alert
    status["telegram_engine"] = "OK"
except Exception as e:
    status["telegram_engine"] = f"ERROR: {e}"

# --- Market Mode Engine ---
try:
    from engines.market_mode_engine import MarketModeEngine
    status["market_mode_engine"] = "OK"
except Exception as e:
    status["market_mode_engine"] = f"ERROR: {e}"

# --- Opportunity Trigger Engine ---
try:
    from engines.opportunity_trigger_engine import process_opportunity
    status["opportunity_trigger_engine"] = "OK"
except Exception as e:
    status["opportunity_trigger_engine"] = f"ERROR: {e}"

print("\n===== MODULE STATUS =====")
for k, v in status.items():
    print(f"{k}: {v}")

print("\n===== SYSTEM CHECK COMPLETE =====")
