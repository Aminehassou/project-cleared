from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

def filter_query(item_list, query):
    filtered_list = {"suggestions": []}
    for item in item_list["suggestions"]:
        if query.lower() in item["value"].lower():
            filtered_list["suggestions"].append({"value": item["value"]})
    return filtered_list

@app.route("/games")
def get_games():
    cars = {"suggestions": [
        { "value": "United Arab Emirates", "data": "AE" },
        { "value": "United Kingdom",       "data": "UK" },
        { "value": "United States",        "data": "US" }
    ]}
    
    query = request.args.get("query")
    filtered_cars = filter_query(cars, query)
    return jsonify(filtered_cars)

@app.route("/")
def home():
    return render_template("index.html")