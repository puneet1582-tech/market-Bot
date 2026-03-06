import os

def load_env():
    path = "config/.env"
    if not os.path.exists(path):
        return

    with open(path) as f:
        for line in f:
            if "=" in line:
                k,v = line.strip().split("=",1)
                os.environ[k]=v
