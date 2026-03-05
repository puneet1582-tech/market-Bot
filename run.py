from core.master_intelligence_controller import MasterIntelligenceController

def main():

    brain = MasterIntelligenceController()

    result = brain.execute()

    print(result)

    try:
        from engines.alert_engine.telegram_alert import send_market_report
        send_market_report(result)
    except Exception as e:
        print("telegram error:", e)


if __name__ == "__main__":
    main()
