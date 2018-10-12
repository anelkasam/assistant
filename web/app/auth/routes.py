from flask import jsonify, request, render_template, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
# from sqlalchemy import exc
#
from app import db
from app.auth import bp
from app.auth.forms import RegisterForm, LoginForm
from app.auth.models import User, Family


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    print('Register', form.validate_on_submit())
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now a registered user!')
        return redirect(url_for('auth.login'))

    print('Something went wrong.', form.validate_on_submit())
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password. Try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# @bp.route('/users', methods=['POST'])
# def add_user():
#     post_data = request.get_json()
#     response_object = {
#         'status': 'fail',
#         'message': f'Invalid json'
#     }
#     if not post_data:
#         return jsonify(response_object), 400
#
#     name = post_data.get('name')
#     email = post_data.get('email')
#     try:
#         user = User.query.filter_by(email=email).first()
#         if not user:
#             db.session.add(User(name=name, email=email))
#             db.session.commit()
#             response_object = {
#                 'status': 'success',
#                 'message': f'{email} was added!'
#             }
#             return jsonify(response_object), 201
#         response_object['message'] = 'Sorry. That email already exists.'
#         return jsonify(response_object), 400
#     except exc.IntegrityError as e:
#         db.session.rollback()
#         return jsonify(response_object), 400
#
#
# @bp.route('/users/<user_id>', methods=['GET'])
# def get_single_user(user_id):
#     """Get single user details"""
#     user = User.query.filter_by(id=user_id).first()
#     response_object = {
#         'status': 'success',
#         'data': {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'active': user.active
#         }
#     }
#     return jsonify(response_object), 200
#
#
# @bp.route('/families', methods=['POST'])
# def add_family():
#     post_data = request.get_json()
#     last_name = post_data.get('last_name')
#     db.session.add(Family(last_name=last_name))
#     db.session.commit()
#     response_object = {
#         'status': 'success',
#         'message': f'{last_name} was added!'
#     }
#     return jsonify(response_object), 201
