import enum
from datetime import datetime
from time import time
import jwt

from app import db, login
from flask import current_app
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(32), nullable=False)
    users = db.relationship('User', backref='family', lazy='dynamic')

    def __repr__(self):
        return f'Family {self.lastname}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    is_head = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def create_family(self, family):
        self.family_id = family.id
        self.is_head = True
        db.session.commit()

    def __repr__(self):
        return f'User {self.name}'


class BudgetCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=True)
    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.title}'


class TransactionTypes(enum.Enum):
    expenses = -1
    income = 1


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TransactionTypes), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120))
    category_id = db.Column(db.Integer, db.ForeignKey('budget_category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    family = db.relationship('Family', backref=db.backref('family', uselist=False))
    user = db.relationship('User', backref=db.backref('user', uselist=False))

    def __repr__(self):
        return f'Transaction: {self.amount} грн на {self.description}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
