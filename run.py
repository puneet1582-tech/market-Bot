"""
ULTIMATE BRAIN
PRIMARY ENTRY POINT
INSTITUTIONAL SINGLE EXECUTION MODEL
"""

from core.master_brain import MasterBrain


def main():
    brain = MasterBrain()
    brain.validate_environment()
    result = brain.execute()
    return result



# --- GLOBAL NEWS ENGINE ---

import subprocess

subprocess.run(["python","engines/news_engine/global_news_collector.py"])

subprocess.run(["python","engines/news_engine/news_validator.py"])

subprocess.run(["python","engines/news_engine/macro_classifier.py"])

subprocess.run(["python","engines/news_engine/sector_mapper.py"])

subprocess.run(["python","engines/news_engine/stock_mapper.py"])

subprocess.run(["python","engines/news_engine/impact_engine.py"])

# --- END GLOBAL NEWS ENGINE ---

if __name__ == "__main__":
    output = main()
    print(output)


# ===============================
# OPTIONAL REAL INTELLIGENCE LAYER
# ===============================

try:
    from real_intelligence_layer.master_intelligence_engine import MasterIntelligenceEngine

    def run_real_intelligence_layer(company_data):
        engine = MasterIntelligenceEngine()
        return engine.run_full_analysis(company_data)

except Exception as e:
    print("Real Intelligence Layer not activated:", e)

# ===============================


# ----- TELEGRAM REPORT -----
try:
    from engines.alert_engine.telegram_alert import send_market_report
    send_market_report(result)
except Exception as e:
    print("telegram alert error:", e)

