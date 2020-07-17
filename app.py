from flask import Flask, render_template, jsonify, request
import data
app = Flask(__name__)

def filter_query(item_list, query):
    filtered_list = {"suggestions": []}
    for item in item_list["suggestions"]:
        if query.lower() in item["value"].lower():
            filtered_list["suggestions"].append({"value": item["value"]})
    return filtered_list

@app.route("/games")
def get_games():

    query = request.args.get("query")
    games = data.get_games(query)
    return jsonify(games)

@app.route("/")
def home():
    return render_template("index.html")