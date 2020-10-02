from flask import Flask, render_template

app = Flask(__name__)
data = [
    {"description": "Todo 01"},
    {"description": "Todo 02"},
    {"description": "Todo 03"},
    {"description": "Todo 04"},
]


@app.route("/")
def index():
    print(data)
    return render_template("index.html", context=data)
