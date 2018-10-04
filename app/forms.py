from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User, Family


class RegistrationForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('User with given email address is already exist.')


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class CreateFamily(FlaskForm):
    lastname = StringField('Last name', validators=[DataRequired()])
    submit = SubmitField()

    def validate_lastname(self, name):
        family = Family.query.filter_by(lastname=name).first()
        if family is not None:
            raise ValidationError('Family with this last name is already exist.')
