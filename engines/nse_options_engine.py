import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_option_chain(symbol):
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=HEADERS)
    r = session.get(url, headers=HEADERS)
    data = r.json()
    return data["records"]["data"]

def options_signal(symbol):
    try:
        chain = get_option_chain(symbol)
    except:
        return 0, ["No NSE option data"]

    total_call_oi = 0
    total_put_oi = 0

    for row in chain:
        if "CE" in row:
            total_call_oi += row["CE"]["openInterest"]
        if "PE" in row:
            total_put_oi += row["PE"]["openInterest"]

    if total_call_oi == 0:
        return 0, ["No OI data"]

    pcr = round(total_put_oi / total_call_oi, 2)

    reasons = [
        f"CALL OI = {total_call_oi}",
        f"PUT OI = {total_put_oi}",
        f"PCR = {pcr}"
    ]

    score = 0
    if pcr < 0.8:
        score = 1
        reasons.append("Low PCR = Bullish")
    elif pcr > 1.2:
        score = -1
        reasons.append("High PCR = Bearish")
    else:
        reasons.append("PCR neutral")

    return score, reasons
