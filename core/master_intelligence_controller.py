from market_brain import generate_report

class MasterIntelligenceController:

    def execute(self):

        print("Running Market Brain Analysis")

        report = generate_report()

        result = {
            "MARKET_SUMMARY": {
                "mode": report["MODE"]
            },
            "STOCK_ANALYSIS": report["STOCKS"]
        }

        return result


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)


def run():
    print('Engine started:', __name__)
