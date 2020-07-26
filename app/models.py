
from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return '<User {}>'.format(self.username) 

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    platform = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return '<Games {}>'.format(self.title)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))