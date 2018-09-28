import enum

from app import db


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(32), nullable=False, unique=True)
    users = db.relationship('User', backref='family', lazy='dynamic')

    def __repr__(self):
        return f'Family {self.lastname}'


class User(db.Model):
    # __table_args__ = ()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))

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
    user = db.relationship('User', backref=db.backref('user', uselist=False))

    def __repr__(self):
        return f'Transaction: {self.amount} грн на {self.description}'
