from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Ultimate Brain Market Bot Running"

def safe_background_start():
    try:
        from brain_engine import start_brain
        start_brain()
    except Exception as e:
        print("Background engine error:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    
    # Start background system safely
    safe_background_start()

    # Start web server
    app.run(host="0.0.0.0", port=port)
