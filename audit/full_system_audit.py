import os
import json
from pathlib import Path

ROOT = Path(".")

print("\n==============================")
print("ULTIMATE BRAIN FULL SYSTEM AUDIT")
print("==============================\n")

folders = []
files = []

for root, dirs, fs in os.walk(ROOT):
    for d in dirs:
        folders.append(os.path.join(root, d))
    for f in fs:
        files.append(os.path.join(root, f))

print("TOTAL FOLDERS:", len(folders))
print("TOTAL FILES:", len(files))
print("\n")

engines = {
"master_brain":[
"brain_engine.py",
"brain_control.py",
"run.py",
"main.py"
],

"fundamental_engines":[
"fundamental_engine.py",
"quarterly_engine.py",
"financial_engine.py"
],

"institutional_engines":[
"fii_dii_engine.py",
"ownership_engine.py",
"promoter_engine.py"
],

"buffett_analysis":[
"moat_engine.py",
"business_quality_engine.py",
"management_engine.py",
"compounding_engine.py"
],

"market_intelligence":[
"sector_engine.py",
"sector_money_flow.py",
"mode_engine.py"
],

"global_macro":[
"global_news_engine.py",
"macro_engine.py",
"policy_engine.py"
],

"opportunity_detection":[
"top20_engine.py",
"multibagger_engine.py",
"trade_engine.py"
],

"data_pipeline":[
"price_data_engine.py",
"universe_engine.py",
"data_ingestion.py"
],

"automation":[
"production_autorun.py",
"scheduler_engine.py"
],

"telegram":[
"telegram_engine.py",
"alert_engine.py"
],

"deployment":[
"render.yaml",
"Dockerfile",
"requirements.txt"
]
}

engine_report = {}

for engine, flist in engines.items():

    found = []
    missing = []

    for f in flist:

        exists = False

        for file in files:
            if file.endswith(f):
                exists = True
                found.append(f)
                break

        if not exists:
            missing.append(f)

    engine_report[engine] = {
        "found":found,
        "missing":missing
    }

print("\n==============================")
print("ENGINE STATUS REPORT")
print("==============================\n")

total_engines = 0
completed = 0

for k,v in engine_report.items():

    total_engines += 1

    print("ENGINE:",k)
    print("FOUND:",len(v["found"]))
    print("MISSING:",len(v["missing"]))

    if len(v["missing"]) == 0:
        completed += 1

    if v["missing"]:
        print("MISSING FILES:")
        for m in v["missing"]:
            print("   ",m)

    print("\n")

completion = (completed/total_engines)*100

print("\n==============================")
print("CORE IDEA COVERAGE")
print("==============================\n")

print("TOTAL ENGINES:",total_engines)
print("FULLY COMPLETE:",completed)

print("\nSYSTEM COMPLETION:",round(completion,2),"%")

report = {
"total_files":len(files),
"total_folders":len(folders),
"engine_report":engine_report,
"completion_percent":completion
}

os.makedirs("audit_report",exist_ok=True)

with open("audit_report/system_audit.json","w") as f:
    json.dump(report,f,indent=4)

print("\nAudit report saved → audit_report/system_audit.json")
print("\nAUDIT COMPLETE\n")
