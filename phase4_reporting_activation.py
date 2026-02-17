from engines.institutional_research_reporting_engine import InstitutionalResearchReportingEngine

_report_engine = InstitutionalResearchReportingEngine()

def apply_reporting_layer(dashboard):
    try:
        reports = _report_engine.generate_reports(dashboard)
        dashboard["institutional_reports"] = reports
    except Exception as e:
        dashboard["reporting_error"] = str(e)

    return dashboard
