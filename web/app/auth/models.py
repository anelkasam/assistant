import jwt

from time import time
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(32), nullable=False)
    users = db.relationship('User', backref='family', lazy='dynamic')

    def __repr__(self):
        return f'Family: {self.last_name}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_head = db.Column(db.Boolean, default=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256']).get('reset_password')
        return user_id and User.query.get(user_id)

    def __repr__(self):
        return f'User: {self.name}'


@login.user_loader
def load_user(id):
    """
    Takes user id from the session and load corresponding user from the DataBase
    """
    return User.query.get(int(id))
