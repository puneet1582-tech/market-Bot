"""
Ultimate Brain — Institutional Research Archive Engine
Stores institutional reports and decision logs historically
"""

import json
import os
from datetime import datetime

ARCHIVE_FILE = "data/research_archive.json"


class ResearchArchiveEngine:

    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(ARCHIVE_FILE):
            with open(ARCHIVE_FILE, "w") as f:
                json.dump([], f)

    def archive(self, dashboard):
        with open(ARCHIVE_FILE, "r") as f:
            archive = json.load(f)

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "reports": dashboard.get("institutional_reports", {}),
            "classification": dashboard.get("market_mode_classification", {}),
            "portfolio": dashboard.get("optimized_portfolio_allocation", {})
        }

        archive.append(entry)

        with open(ARCHIVE_FILE, "w") as f:
            json.dump(archive, f, indent=2)

        return archive
