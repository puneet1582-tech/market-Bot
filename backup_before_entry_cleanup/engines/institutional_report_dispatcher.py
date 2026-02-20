"""
Ultimate Brain — Institutional Report Dispatcher
Formats and dispatches institutional research reports via Telegram
"""

from engines.telegram_alert_engine import send_telegram_alert
import json


class InstitutionalReportDispatcher:

    def dispatch(self, dashboard):
        reports = dashboard.get("institutional_reports", {})
        if not reports:
            return

        formatted = json.dumps(reports, indent=2)
        send_telegram_alert(f"INSTITUTIONAL REPORT UPDATE:\n{formatted}")
