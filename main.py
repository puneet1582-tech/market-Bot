from engines.final_report_engine import FinalReportEngine

engine = FinalReportEngine()
report = engine.generate_report("RELIANCE", "Energy")

with open("daily_report.txt", "w") as f:
    for k, v in report.items():
        f.write(f"{k} : {v}\n")

print("DAILY REPORT GENERATED -> daily_report.txt")
