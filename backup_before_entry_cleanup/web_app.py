from flask import Flask, render_template_string
from market_brain import generate_report

app = Flask(__name__)

HTML = """
<html>
<head>
<title>Market Bot</title>
<style>
body { font-family: Arial; background:#f4f4f4; padding:20px; }
table { border-collapse: collapse; width:100%; background:white; }
th, td { border:1px solid #ccc; padding:8px; text-align:center; }
th { background:#222; color:white; }
.buy { background:#c8f7c5; }
.avoid { background:#f7c5c5; }
.wait { background:#f7f3c5; }
</style>
</head>
<body>

<h2>MARKET MODE: {{ mode }}</h2>

<table>
<tr>
<th>Symbol</th>
<th>Decision</th>
<th>Score</th>
<th>Reason</th>
</tr>

{% for s in stocks %}
<tr class="{{ s.decision|lower }}">
<td>{{ s.symbol }}</td>
<td>{{ s.decision }}</td>
<td>{{ s.score }}</td>
<td>{{ s.reason }}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

@app.route("/")
def home():
    report = generate_report()
    return render_template_string(
        HTML,
        mode=report["MODE"],
        stocks=report["STOCKS"]
    )

# DISABLED ENTRY POINT
# if __name__ == "__main__":
    app.run(debug=True)

