from engines.sector_strength_engine import sector_strength

def sector_report():

    s = sector_strength()

    lines=[]

    for k,v in sorted(s.items(), key=lambda x:x[1], reverse=True):

        lines.append(f"{k}: {round(v*100,2)}")

    return "\n".join(lines)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
