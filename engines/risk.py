def risk_engine(decision, category):
    """
    Returns risk level and position size
    """

    if decision == "BUY":
        return "LOW", "15%"

    if "SPECULATIVE" in decision:
        return "HIGH", "3–5%"

    return "VERY HIGH", "0%"



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
