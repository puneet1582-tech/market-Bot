def load_quarterly_shareholding_data():
    # DEMO DATA (3 साल = 12 quarters)
    return {
        "RELIANCE": {
            "quarters": ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12"],
            "promoter": [50.5,50.6,50.7,50.8,50.9,51.0,51.1,51.2,51.3,51.4,51.5,51.6],
            "fii": [22.0,22.2,22.5,22.8,23.0,23.5,24.0,24.3,24.6,25.0,25.5,26.0],
            "dii": [10.0,10.1,10.2,10.3,10.4,10.5,10.6,10.7,10.8,10.9,11.0,11.1],
            "retail": [17.5,17.1,16.6,16.1,15.7,15.0,14.3,13.8,13.3,12.7,12.0,11.3]
        },
        "TCS": {
            "quarters": ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12"],
            "promoter": [72,72,72,72,72,72,72,72,72,72,72,72],
            "fii": [18,18.1,18.2,18.3,18.4,18.5,18.6,18.7,18.8,18.9,19.0,19.1],
            "dii": [5,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6.0,6.1],
            "retail": [5,4.8,4.6,4.4,4.2,4.0,3.8,3.6,3.4,3.2,3.0,2.8]
        }
    }

def trend(values):
    if values[-1] > values[0]:
        return "INCREASING"
    elif values[-1] < values[0]:
        return "DECREASING"
    else:
        return "FLAT"

def smart_money_report(stock, data):
    row = data.get(stock)
    if not row:
        return 0, ["No shareholding data"]

    reasons = []

    promoter_trend = trend(row["promoter"])
    fii_trend = trend(row["fii"])
    dii_trend = trend(row["dii"])
    retail_trend = trend(row["retail"])

    reasons.append(f"Promoter holding: {promoter_trend}")
    reasons.append(f"FII holding: {fii_trend}")
    reasons.append(f"DII holding: {dii_trend}")
    reasons.append(f"Retail holding: {retail_trend}")

    score = 0
    if promoter_trend == "INCREASING": score += 1
    if fii_trend == "INCREASING": score += 1
    if dii_trend == "INCREASING": score += 1
    if retail_trend == "DECREASING": score += 1  # crowd exit = smart money entry

    return score, reasons
