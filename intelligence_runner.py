from core.master_brain import MasterBrain

class IntelligenceNarrative:

    def __init__(self):
        self.brain = MasterBrain()

    def run(self):
        raw_output = self.brain.execute()
        return self.build_readable_output(raw_output)

    def build_readable_output(self, raw):

        market_mode = raw["MARKET_SUMMARY"]["mode"]

        mode_explanation = {
            "INVEST": "बाजार लंबी अवधि के निवेश के लिए अनुकूल है।",
            "TRADE": "बाजार अभी शॉर्ट-टर्म मूवमेंट फेज में है।",
            "DEFENSIVE": "बाजार में जोखिम अधिक है, सावधानी रखें।"
        }

        report = {}
        report["MARKET_MODE"] = market_mode
        report["MARKET_MESSAGE"] = mode_explanation.get(market_mode, "स्थिति विश्लेषणाधीन है।")

        readable_stocks = []

        for stock in raw["TOP_20"]:

            readable_stocks.append({
                "symbol": stock["symbol"],
                "analysis": f"{stock['symbol']} अभी मार्केट मोमेंटम के आधार पर चयनित हुआ है।",
                "score": stock["score"]
            })

        report["TOP_STOCKS_SIMPLE_VIEW"] = readable_stocks

        return report


if __name__ == "__main__":
    runner = IntelligenceNarrative()
    result = runner.run()
    print(result)
