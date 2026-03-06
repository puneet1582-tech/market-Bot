import pandas as pd

stocks = pd.read_csv("data/stocks.csv")

sector_rules = {

"PHARMA":["pharma","drug","labs","pharmaceutical"],
"BANK":["bank","finance","financial"],
"IT":["tech","software","infotech","technologies"],
"METAL":["steel","metal","mining"],
"POWER":["power","energy"],
"AUTO":["motors","auto","automobile"],
"INFRA":["infra","engineering","construction"],
"CHEMICAL":["chemical","chem","fertilizer"],
"FMCG":["foods","consumer","retail"],
"DEFENCE":["defence","aerospace"],
}

def detect_sector(name):

    name=name.lower()

    for sector,words in sector_rules.items():

        for w in words:

            if w in name:
                return sector

    return "OTHER"

for i,row in stocks.iterrows():

    if row["sector"]=="UNKNOWN":

        stocks.at[i,"sector"]=detect_sector(row["company"])

stocks.to_csv("data/stocks.csv",index=False)

print("Sector mapping updated")

