from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    output = subprocess.getoutput("python3 main.py")
    return f"<pre>{output}</pre>"

# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    app.run(debug=True)

