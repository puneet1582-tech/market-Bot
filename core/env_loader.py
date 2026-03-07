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


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
