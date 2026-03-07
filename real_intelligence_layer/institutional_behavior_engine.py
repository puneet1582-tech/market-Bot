class InstitutionalBehaviorEngine:

    def analyze(self, data):
        result = {}

        result["promoter_trend"] = self._trend(data.get("promoter"))
        result["fii_trend"] = self._trend(data.get("fii"))
        result["dii_trend"] = self._trend(data.get("dii"))
        result["pledge_status"] = "High Risk" if data.get("pledge", 0) > 20 else "Safe"

        return result

    def _trend(self, series):
        if not series or len(series) < 2:
            return "Insufficient Data"
        return "Accumulating" if series[-1] > series[0] else "Distributing"


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
