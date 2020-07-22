from flask import Flask, render_template, jsonify, request, flash, redirect
from config import Config
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import data

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Succesfully logged in", "success" )
        return redirect('/')
    return render_template("login.html", form=form)