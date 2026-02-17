# SECTOR LEADERSHIP ENGINE
# Detects top-performing stock within each sector

def detect_sector_leaders(opportunity_list):
    leaders = {}

    for op in opportunity_list:
        sector = op.get("sector", "UNKNOWN")

        if sector not in leaders:
            leaders[sector] = op
        else:
            if op["score"] > leaders[sector]["score"]:
                leaders[sector] = op

    return leaders
