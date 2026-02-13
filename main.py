from engines.final_report_engine import FinalReportEngine
import time

engine = FinalReportEngine()
report = engine.generate_report("RELIANCE", "Energy")

with open("daily_report.txt", "w") as f:
    for k, v in report.items():
        f.write(f"{k} : {v}\n")

print("DAILY REPORT GENERATED -> daily_report.txt")

# keep program running (required for Render Web Service)
while True:
    time.sleep(60)
