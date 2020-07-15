from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/games")
def get_games():
    cars = {'suggestions': [
        { "value": "Unite Arab Emirates", "data": "AE" },
        { "value": "United Kingdom",       "data": "UK" },
        { "value": "United States",        "data": "US" }
    ]}
    return jsonify(cars)

@app.route("/")
def home():
    return render_template("index.html")