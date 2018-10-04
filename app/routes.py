from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateFamily
from app.models import Family, User, BudgetCategory, Transaction

from datetime import datetime

from flask import redirect, render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    If user is not logged in returns simple index page.
    If user logged in -> returns form if needed
    """
    if current_user.is_authenticated and not current_user.family:
        form = CreateFamily()
        if form.is_submitted():
            family = Family(lastname=form.lastname.data)
            db.session.add(family)
            db.session.commit()
            current_user.create_family(family)
            flash(f'Congratulation! You have just created family {family.lastname}')
            return redirect(url_for('index'))

        return render_template('index.html', title='home', form=form)

    return render_template('index.html', title='home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid name or password!')
            return redirect('login')

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<user_id>')
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)


@app.route('/family/<family_id>')
@login_required
def family(family_id):
    """
    Render Family page if current user has family
    """
    family = Family.query.get_or_404(family_id)
    return render_template('family.html', family=family)
