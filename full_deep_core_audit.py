import os
import re
import json
import ast
from datetime import datetime

PROJECT_ROOT = os.getcwd()

MANDATORY_FILES = [
    "run.py",
    "brain_control.py"
]

EXPECTED_KEYWORDS = {
    "price_data_schema": ["date", "symbol", "price"],
    "fundamentals": ["revenue", "profit", "net_profit", "cash_flow", "debt"],
    "quarter_analysis": ["quarter", "q1", "q2", "q3", "q4"],
    "shareholding": ["promoter", "fii", "dii", "pledge"],
    "news_engine": ["news", "headline", "reuters", "bloomberg"],
    "sector_mapping": ["sector", "industry"],
    "multibagger_logic": ["roe", "roce", "cagr"],
    "mode_engine": ["invest", "trade", "defensive"],
    "telegram": ["telegram", "bot", "send_message"],
}

report = {
    "timestamp": str(datetime.now()),
    "files_scanned": 0,
    "python_files": 0,
    "missing_mandatory_files": [],
    "detected_modules": {},
    "duplicate_entrypoints": [],
    "hardcoded_keys": [],
    "production_readiness_score": 0,
    "missing_components": [],
}

all_py_files = []

for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        report["files_scanned"] += 1
        if file.endswith(".py"):
            report["python_files"] += 1
            full_path = os.path.join(root, file)
            all_py_files.append(full_path)

# Check mandatory files
for m in MANDATORY_FILES:
    if not os.path.exists(os.path.join(PROJECT_ROOT, m)):
        report["missing_mandatory_files"].append(m)

# Analyze python files
keyword_hits = {k: False for k in EXPECTED_KEYWORDS}

for file_path in all_py_files:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()

            # Keyword detection
            for section, keywords in EXPECTED_KEYWORDS.items():
                for kw in keywords:
                    if kw in content:
                        keyword_hits[section] = True

            # Detect multiple __main__
            if 'if __name__ == "__main__"' in content:
                report["duplicate_entrypoints"].append(file_path)

            # Detect hardcoded API keys
            if re.search(r'api[_-]?key\s*=\s*["\']', content):
                report["hardcoded_keys"].append(file_path)

    except Exception:
        pass

report["detected_modules"] = keyword_hits

# Missing logic detection
for section, detected in keyword_hits.items():
    if not detected:
        report["missing_components"].append(section)

# Production score calculation
score = 100
score -= len(report["missing_mandatory_files"]) * 10
score -= len(report["missing_components"]) * 5
score -= len(report["hardcoded_keys"]) * 5

if score < 0:
    score = 0

report["production_readiness_score"] = score

# Save report
with open("deep_core_audit_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("========================================")
print("FULL DEEP CORE AUDIT COMPLETED")
print("========================================")
print("Python Files Found:", report["python_files"])
print("Missing Mandatory Files:", report["missing_mandatory_files"])
print("Missing Components:", report["missing_components"])
print("Duplicate Entry Points:", len(report["duplicate_entrypoints"]))
print("Hardcoded API Keys:", len(report["hardcoded_keys"]))
print("Production Readiness Score:", report["production_readiness_score"], "%")
print("Full JSON Report Saved: deep_core_audit_report.json")
print("========================================")
