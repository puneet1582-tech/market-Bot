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
            "TRADE": "बाजार अभी शॉर्ट-टर्म ट्रेडिंग फेज में है।",
            "DEFENSIVE": "बाजार में जोखिम अधिक है, पूंजी की सुरक्षा पर ध्यान दें।"
        }

        report = {}
        report["MARKET_MODE"] = market_mode
        report["MARKET_MESSAGE"] = mode_explanation.get(market_mode, "स्थिति विश्लेषणाधीन है।")

        report["GLOBAL_CONTEXT"] = self.global_context_explanation(market_mode)

        readable_stocks = []

        for stock in raw["TOP_20"]:

            stock_view = {
                "symbol": stock["symbol"],
                "why_selected": self.stock_reasoning(stock["symbol"], market_mode),
                "risk_view": self.global_risk_view(stock["symbol"], market_mode),
                "score": stock["score"]
            }

            readable_stocks.append(stock_view)

        report["TOP_STOCK_INTELLIGENCE"] = readable_stocks

        return report


    def global_context_explanation(self, mode):

        if mode == "TRADE":
            return "वैश्विक स्तर पर अस्थिरता मध्यम है, इसलिए तेज़ मूवमेंट वाले सेक्टर सक्रिय हैं।"
        elif mode == "INVEST":
            return "वैश्विक माहौल स्थिर है, संरचनात्मक ग्रोथ वाले सेक्टर लाभ में रह सकते हैं।"
        else:
            return "वैश्विक जोखिम अधिक है, डिफेंसिव सेक्टर बेहतर प्रदर्शन कर सकते हैं।"


    def stock_reasoning(self, symbol, mode):

        if mode == "TRADE":
            return f"{symbol} में हाल की प्राइस मोमेंटम मजबूत है।"
        elif mode == "INVEST":
            return f"{symbol} संरचनात्मक ग्रोथ के लिए उपयुक्त दिख रहा है।"
        else:
            return f"{symbol} में सीमित जोखिम के साथ सीमित अवसर है।"


    def global_risk_view(self, symbol, mode):

        if mode == "TRADE":
            return "ग्लोबल अस्थिरता का असर अल्पकालिक हो सकता है।"
        elif mode == "INVEST":
            return "ग्लोबल माहौल दीर्घकालिक निवेश के लिए अनुकूल है।"
        else:
            return "ग्लोबल जोखिम इस स्टॉक पर नकारात्मक असर डाल सकता है।"


if __name__ == "__main__":
    runner = IntelligenceNarrative()
    result = runner.run()
    print(result)
