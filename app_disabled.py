from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    output = subprocess.getoutput("python3 main.py")
    return f"<pre>{output}</pre>"

    app.run(debug=True)



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
