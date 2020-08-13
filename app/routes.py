import datetime
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from werkzeug.urls import url_parse
from sqlalchemy.exc import IntegrityError
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddGameForm
from app.data import get_games, get_game_by_id
from app.models import User, Game, Platform, User_game
from app import app, db

def filter_query(item_list, query):
    filtered_list = {"suggestions": []}
    for item in item_list["suggestions"]:
        if query.lower() in item["value"].lower():
            filtered_list["suggestions"].append({"value": item["value"]})
    return filtered_list

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route("/games")
def browse_games():

    query = request.args.get("query")
    games = get_games(query)
    for game in games["suggestions"]:
        game["url"] = url_for("get_game", api_id = game["data"])
    return jsonify(games)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', "danger")
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template("login.html", form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/game_data/<api_id>')
@login_required
def get_game(api_id):
    game = Game.query.filter_by(api_id = api_id).first()
    if not game:
        game_info = get_game_by_id(api_id)
        name = game_info["name"]
        platforms_list = []
        if "platforms" in game_info:
            for platform in game_info["platforms"]:
                try:
                    p = Platform(api_id = platform["id"], title = platform["name"])
                    db.session.add(p)
                    db.session.commit()

                except IntegrityError as e:
                    db.session.rollback()
                    p = Platform.query.filter_by(api_id = platform["id"]).first()
                    print("You can't add this platform (it already exists)")
                platforms_list.append(p)

        game = Game(api_id = api_id, title = name)
        game.platforms = platforms_list
        db.session.add(game)
        db.session.commit()
    return redirect(url_for("display_game", id = game.id))


@app.route('/game/<id>')
@login_required
def display_game(id):
    game = Game.query.filter_by(id = id).first()
    return render_template("game.html", game=game)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    info = {"name": username, "games": 5, "cleared": 2, "clearing": 3}
    return render_template("user.html", user=user, info=info)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user, original_username=current_user.username) 
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', "success")
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html',
                           form=form)
@login_required
@app.route('/insert/<id>', methods=['GET', 'POST'])
def add_game(id):
    form = AddGameForm()
    game = Game.query.filter_by(id = id).first()
    has_platforms = True
    if not game.platforms:
        has_platforms = False

    for platform in game.platforms:
        form.platform.choices.append((platform.id, platform.title))
    if form.validate_on_submit():
        print("PLATFORM DATA:", form.platform.data, current_user.id)
        user = User_game(clear_status=form.status.data, game_id=id, platform_id=form.platform.data, user_id=current_user.id )
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered!", "success")

    return render_template("add_game.html", form=form, has_platforms=has_platforms)