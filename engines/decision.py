def final_decision(score, category):
    if category == "Large":
        if score >= 60:
            return "BUY"
        elif score >= 45:
            return "WAIT"
        else:
            return "AVOID"

    if category in ["Small", "Penny"]:
        if score >= 70:
            return "SPECULATIVE BUY (MAX 3–5%)"
        elif score >= 50:
            return "WAIT"
        else:
            return "AVOID"



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
