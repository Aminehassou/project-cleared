import datetime
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from werkzeug.urls import url_parse
from time import strftime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc, or_
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, EditProfileForm, AddGameForm, EditGameForm
from app.data import get_games, get_game_by_id
from app.models import User, Game, Platform, User_game
from app.email import send_password_reset_email
from app import app, db

def filter_devs(query):
    developers = []
    publishers = []
    for company in query.get("involved_companies", []):
        if company["developer"]:
            developers.append(company["company"]["name"])
            #dev_info.update({"developer": company["company"]["name"] })
        if company["publisher"]:
            publishers.append(company["company"]["name"])
            #dev_info.update({"publisher": company["company"]["name"] })
    return {
        "developers": ", ".join(developers),
        "publishers": ", ".join(publishers)
    }

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route("/games")
def browse_games():

    query = request.args.get("query")

    games = get_games(query)
    for game in games:
        game["url"] = url_for("get_game", api_id = game["id"])
        game["image_url"] = Game.generate_image_url(game["image_id"])
        
    return jsonify(games)

@app.route("/")
def home():
    user_count = db.session.query(func.count(User.id)).first()[0]

    top_games = db.session.query(User_game.game_id, Game.title, Game.image_id, func.count(User_game.game_id).label("count"))\
        .filter(User_game.game_id == Game.id)\
        .group_by(User_game.game_id)\
        .order_by(desc("count"))\
        .limit(4).all()

    clear_status_info = db.session.query(User_game.clear_status.name, func.count(User_game.clear_status))\
        .group_by(User_game.clear_status).all()

    added_games_count = 0
    status_info = {}

    for status in clear_status_info:
        added_games_count += status[1]
        status_info[status[0]] = status[1]

    return render_template("index.html", top_games=top_games, Game=Game, added_games_count=added_games_count,
                                         clear_status_info=clear_status_info, user_count=user_count, status_info=status_info)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You've already registered!", "danger")
        return redirect(url_for("home"))
        
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
        flash("You're already logged in!", "danger")
        return redirect(url_for("home"))
        
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

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)
                           
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/game_data/<api_id>')
def get_game(api_id):
    game = Game.query.filter_by(api_id = api_id).first()
    if not game:
        game_info = get_game_by_id(api_id)
        dev_info = filter_devs(game_info)
        name = game_info["name"]
        date = datetime.datetime.fromtimestamp(game_info["first_release_date"]).strftime('%Y-%m-%d %H:%M:%S')

        if "similar_games" not in game_info:
            similar_games = None
        else:
            similar_games = game_info["similar_games"]

        if "cover" not in game_info:
            image_id = None
        else:
            image_id = game_info["cover"]["image_id"]

        if "summary" not in game_info:
            summary = None
        else:
            summary = game_info["summary"]

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

        game = Game(api_id = api_id, title = name, summary=summary, image_id = image_id, developer = dev_info["developers"], publisher = dev_info["publishers"], initial_release_date = date, similar_games=similar_games)
        game.platforms = platforms_list
        db.session.add(game)
        db.session.commit()
    return redirect(url_for("display_game", id = game.id))


@app.route('/game/<id>', methods=['GET', 'POST'])
def display_game(id):
    form = AddGameForm()
    game = Game.query.filter_by(id = id).first()
    recently_added_games = User_game.query.filter_by(game_id=id).order_by(User_game.modified_at).limit(3).all()
    recently_added_notes = User_game.query.filter(User_game.game_id==id, func.coalesce(User_game.note, '') != '').order_by(User_game.modified_at).limit(3).all()
    has_platforms = True

    if not game.platforms:
        has_platforms = False

    for platform in game.platforms:
        form.platform.choices.append((platform.id, platform.title))

    if current_user.is_authenticated:
        user_game = User_game.query.filter_by(game_id=id, platform_id=form.platform.data, user_id=current_user.id).first()
        if not user_game:
            if form.validate_on_submit():
                user = User_game(clear_status=form.status.data, note=form.note.data, game_id=id, platform_id=form.platform.data, user_id=current_user.id )
                db.session.add(user)    
                db.session.commit()
                flash("You have successfully added the game!", "success")
        else:
            flash("This game already exists in your list!", "danger")

    platforms = ", ".join([platform.title for platform in game.platforms])

    return render_template("game.html", game=game, 
        platforms=platforms,
        form=form,
        has_platforms = has_platforms, 
        recently_added_games = recently_added_games,
        recently_added_notes = recently_added_notes)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_game = User_game.query.filter_by(user_id = user.id).all()
    form = EditGameForm()
    return render_template("user.html", user=user, user_game=user_game, form=form)

@app.route('/edit_game_info', methods=['POST'])
@login_required
def edit_game_info():
    form = EditGameForm() 
    if form.validate_on_submit():
        edited_game = User_game.query.filter_by(id=form.user_game_id.data).first()
        form.populate_obj(edited_game)
        db.session.commit()
        flash('Your changes have been saved.', "success")
    return redirect(url_for("user", username=current_user.username))

@app.route('/game/delete', methods=['POST'])
@login_required
def delete_game():
    user_game_id = request.form['user_game_id']
    User_game.query.filter_by(id=user_game_id, user_id=current_user.id).delete()
    db.session.commit()
    flash("Game successfully removed!", "success")
    return redirect(url_for("user", username=current_user.username))



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    form = EditProfileForm(obj=current_user, original_username=current_user.username) 
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', "success")
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html',
                           form=form, user=user)
@login_required
@app.route('/insert/<id>', methods=['GET', 'POST'])
def add_game(id):
    game = Game.query.filter_by(id = id).first()
    has_platforms = True
    if not game.platforms:
        has_platforms = False

    for platform in game.platforms:
        form.platform.choices.append((platform.id, platform.title))
    user_game = User_game.query.filter_by(game_id=id, platform_id=form.platform.data, user_id=current_user.id).first()
    if not user_game:
        if form.validate_on_submit():
            user = User_game(clear_status=form.status.data, game_id=id, platform_id=form.platform.data, user_id=current_user.id )
            db.session.add(user)    
            db.session.commit()
            flash("You have successfully added the game!", "success")
    else:
        flash("This game already exists in your list!", "danger")

    return render_template("add_game.html", form=form, has_platforms=has_platforms)