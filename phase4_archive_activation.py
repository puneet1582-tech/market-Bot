from engines.research_archive_engine import ResearchArchiveEngine

_archive_engine = ResearchArchiveEngine()

def apply_archive_layer(dashboard):
    try:
        dashboard["research_archive"] = _archive_engine.archive(dashboard)
    except Exception as e:
        dashboard["archive_error"] = str(e)

    return dashboard
