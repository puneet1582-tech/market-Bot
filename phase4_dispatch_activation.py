from engines.institutional_report_dispatcher import InstitutionalReportDispatcher

_dispatcher = InstitutionalReportDispatcher()

def apply_dispatch_layer(dashboard):
    try:
        _dispatcher.dispatch(dashboard)
    except Exception as e:
        dashboard["dispatch_error"] = str(e)

    return dashboard


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
