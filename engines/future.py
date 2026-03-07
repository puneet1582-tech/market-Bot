def future_sector_score(row):
    score = 0

    if row["future_score"] >= 80:
        score += 30
    elif row["future_score"] >= 60:
        score += 20
    else:
        score -= 10

    return score



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
