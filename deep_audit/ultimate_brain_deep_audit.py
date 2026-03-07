import os
import json
from pathlib import Path

ROOT = Path(".")

folders=[]
files=[]
py_files=[]

for r,d,f in os.walk(ROOT):
    for fd in d:
        folders.append(os.path.join(r,fd))
    for fl in f:
        path=os.path.join(r,fl)
        files.append(path)
        if fl.endswith(".py"):
            py_files.append(path)

engine_groups={
"master_control":[
"run.py","main.py","super_bot.py","orchestrator.py",
"brain_engine.py","brain_control.py","master_brain.py"
],

"fundamental_layer":[
"fundamental_engine","fundamentals","fundamental_10y",
"quarterly","financial"
],

"institutional_layer":[
"fii","dii","promoter","institutional"
],

"buffett_business_layer":[
"business_evolution","moat","wealth","multibagger"
],

"sector_intelligence":[
"sector_engine","sector_rotation","sector_rank",
"sector_mapper","sector_classifier"
],

"global_macro":[
"global","macro","policy","news"
],

"price_pipeline":[
"price_engine","price_ingestion","bhavcopy",
"live_price","historical_price"
],

"opportunity_detection":[
"opportunity","top20","ranking","trigger"
],

"automation":[
"autorun","runner","scheduler","supervisor"
],

"telegram":[
"telegram","alert"
],

"deployment":[
"render.yaml","Procfile","Dockerfile","requirements.txt"
]
}

engine_map={}
dead_code=[]
duplicates={}

names_seen={}

for f in py_files:
    name=os.path.basename(f)
    if name not in names_seen:
        names_seen[name]=[f]
    else:
        names_seen[name].append(f)

for k,v in names_seen.items():
    if len(v)>1:
        duplicates[k]=v

for group,keys in engine_groups.items():

    engine_map[group]=[]

    for f in files:
        for k in keys:
            if k.lower() in f.lower():
                engine_map[group].append(f)
                break

imported=set()

for f in py_files:
    try:
        with open(f,"r",errors="ignore") as file:
            text=file.read()
            lines=text.split("\n")
            for l in lines:
                if "import " in l or "from " in l:
                    imported.add(l.strip())
    except:
        pass

for f in py_files:
    used=False
    name=os.path.basename(f).replace(".py","")
    for imp in imported:
        if name in imp:
            used=True
            break
    if not used:
        dead_code.append(f)

detected=0
for e in engine_map:
    if len(engine_map[e])>0:
        detected+=1

completion=(detected/len(engine_groups))*100

print("\n===== ULTIMATE BRAIN DEEP AUDIT =====\n")

print("TOTAL FOLDERS:",len(folders))
print("TOTAL FILES:",len(files))
print("PYTHON MODULES:",len(py_files))

print("\nENGINE MAP\n")

for e in engine_map:
    print(e,"->",len(engine_map[e]))

print("\nDUPLICATE MODULES:",len(duplicates))
print("DEAD/UNUSED MODULES:",len(dead_code))

print("\nSYSTEM COMPLETION:",round(completion,2),"%")

report={
"folders":len(folders),
"files":len(files),
"python_modules":len(py_files),
"engine_map":engine_map,
"duplicates":duplicates,
"dead_code":dead_code,
"completion_percent":completion
}

os.makedirs("deep_audit_report",exist_ok=True)

with open("deep_audit_report/ultimate_brain_audit.json","w") as f:
    json.dump(report,f,indent=4)

print("\nREPORT SAVED -> deep_audit_report/ultimate_brain_audit.json\n")



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
