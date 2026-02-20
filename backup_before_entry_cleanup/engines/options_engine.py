import yfinance as yf

def get_options_data(stock):
    try:
        ticker = yf.Ticker(stock + ".NS")
        expiries = ticker.options
        if not expiries:
            return None

        exp = expiries[0]  # nearest expiry
        opt_chain = ticker.option_chain(exp)

        calls = opt_chain.calls
        puts = opt_chain.puts

        total_call_oi = calls["openInterest"].sum()
        total_put_oi = puts["openInterest"].sum()

        if total_call_oi == 0:
            pcr = 0
        else:
            pcr = round(total_put_oi / total_call_oi, 2)

        return {
            "call_oi": int(total_call_oi),
            "put_oi": int(total_put_oi),
            "pcr": pcr
        }
    except Exception as e:
        return None

def options_signal(stock):
    data = get_options_data(stock)
    if not data:
        return 0, ["No options data found"]

    reasons = []
    score = 0

    call_oi = data["call_oi"]
    put_oi = data["put_oi"]
    pcr = data["pcr"]

    reasons.append(f"CALL OI = {call_oi}")
    reasons.append(f"PUT OI = {put_oi}")
    reasons.append(f"PCR = {pcr}")

    if pcr < 0.8:
        score += 1
        reasons.append("Low PCR = Bullish bias")
    elif pcr > 1.2:
        score -= 1
        reasons.append("High PCR = Bearish bias")
    else:
        reasons.append("PCR neutral zone")

    return score, reasons
