from app import app, db
from app.models import User, Game, Platform, User_game, game_platform

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game, 'Platform': Platform, 'User_game': User_game, 'game_platform': game_platform}