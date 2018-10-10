from sqlalchemy.sql import func

from app import db


class Family(db.Model):
    __tablename__ = 'families'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(32), nullable=False)
    # users = db.relationship('User', backref='family', lazy='dynamic')

    def __repr__(self):
        return f'Family: {self.last_name}'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_head = db.Column(db.Boolean, default=False)
    # family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f'User: {self.name}'
