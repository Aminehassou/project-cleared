
import enum
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
class GameStatus(enum.Enum):
    PLAYING = "Playing"
    CLEARED = "Cleared"
    FULL_CLEARED = "100% Cleared"
    
    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        if not item:
            return GameStatus.PLAYING

        return item if isinstance(item, cls) else GameStatus[item]
    
    def __str__(self):
        return self.name

    def __html__(self):
        return self.value

class User_game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clear_status = db.Column(db.Enum(GameStatus), default=GameStatus.PLAYING.value, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    created_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return '<User_game {}>'.format(self.clear_status)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)
    games = db.relationship('Game', secondary="user_game", backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
    def __repr__(self):
        return '<User {}>'.format(self.username) 

game_platform = db.Table('game_platform',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'))
)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)
    platforms = db.relationship('Platform', secondary=game_platform, backref='games')

    def __repr__(self):
        return '<Games {}>'.format(self.title)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return '<Platform {}>'.format(self.title)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))