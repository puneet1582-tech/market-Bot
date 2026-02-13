from engines.final_report_engine import FinalReportEngine
import time
import threading
from flask import Flask

# ---------- Web Server ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Market Bot Running"

# ---------- Bot Engine ----------
def run_bot():
    engine = FinalReportEngine()
    report = engine.generate_report("RELIANCE", "Energy")

    with open("daily_report.txt", "w") as f:
        for k, v in report.items():
            f.write(f"{k} : {v}\n")

    print("DAILY REPORT GENERATED -> daily_report.txt")

    # keep running continuously
    while True:
        time.sleep(60)

# start bot in background thread
threading.Thread(target=run_bot).start()

# start web server (required for Render free web service)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
