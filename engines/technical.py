def technical_signal(row):
    trend = row.get("trend", "UNKNOWN")
    rsi = row.get("rsi", 50)

    if trend == "UP" and 40 <= rsi <= 70:
        return "CONFIRMED"

    if trend == "DOWN":
        return "WEAK"

    return "WAIT"



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
