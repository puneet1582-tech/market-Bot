# OPPORTUNITY RANKING ENGINE
# Generates ranked opportunity list

def rank_opportunities(opportunity_list):
    """
    Sort opportunities by score (descending)
    Returns ranked list
    """
    try:
        ranked = sorted(
            opportunity_list,
            key=lambda x: x.get("score", 0),
            reverse=True
        )
        return ranked
    except Exception as e:
        print("Ranking error:", e)
        return opportunity_list


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
