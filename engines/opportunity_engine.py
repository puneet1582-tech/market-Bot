import random

NSE_SAMPLE = [
"RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK",
"LT","SBIN","ITC","HINDUNILVR","BHARTIARTL",
"KOTAKBANK","ASIANPAINT","BAJFINANCE","MARUTI",
"TITAN","ULTRACEMCO","WIPRO","HCLTECH","NTPC","POWERGRID"
]

def generate_top_opportunities():

    result=[]

    for s in NSE_SAMPLE:

        score=round(random.uniform(0.5,1.5),3)

        result.append({
            "symbol":s,
            "score":score
        })

    result=sorted(result,key=lambda x:x["score"],reverse=True)

    return result[:20]
