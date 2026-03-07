from engines.meta_intelligence_feedback_engine import MetaIntelligenceFeedbackEngine

_engine = MetaIntelligenceFeedbackEngine()

def apply_meta_feedback(dashboard):
    try:
        dashboard["meta_intelligence_feedback"] = _engine.analyze(dashboard)
    except Exception as e:
        dashboard["meta_feedback_error"] = str(e)

    return dashboard


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
