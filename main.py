import time
import brain_engine
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Ultimate Brain Live Engine Running"

def background_loop():
    while True:
        try:
            brain_engine.run()
        except Exception as e:
            print("ENGINE ERROR:", e)
        time.sleep(300)  # 5 minute interval

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=background_loop)
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=10000)
