from flask import Flask
import os
import threading
from brain_engine import start_brain

app = Flask(__name__)

@app.route("/")
def home():
    return "Ultimate Brain Running"

def run_background():
    thread = threading.Thread(target=start_brain)
    thread.start()

if __name__ == "__main__":
    run_background()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
