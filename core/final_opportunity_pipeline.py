import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

REPORT_FILE = "data/master_brain_report.json"
OUTPUT_FILE = "data/top20_final_opportunities.json"


class FinalOpportunityPipeline:

    def run(self):

        print("FINAL OPPORTUNITY PIPELINE RUNNING")

        try:
            with open(REPORT_FILE, "r") as f:
                report = json.load(f)
        except:
            report = {}

        opportunities = report.get("top_opportunities", [])
        multibaggers = report.get("multibagger_candidates", [])
        institutional = report.get("institutional_flow", [])

        final_list = []

        inst_symbols = set()

        for item in institutional:
            symbol = item.get("symbol")
            if symbol:
                inst_symbols.add(symbol)

        for item in opportunities:

            symbol = item.get("symbol")

            if symbol in inst_symbols:
                final_list.append(item)

        for item in multibaggers:

            symbol = item.get("symbol")

            if symbol not in [x.get("symbol") for x in final_list]:
                final_list.append(item)

        final_list = final_list[:20]

        try:
            with open(OUTPUT_FILE, "w") as f:
                json.dump(final_list, f, indent=2)
        except:
            pass

        print("FINAL OPPORTUNITY PIPELINE COMPLETED")

        return final_list


def run():

    engine = FinalOpportunityPipeline()

    return engine.run()


if __name__ == "__main__":
    run()
