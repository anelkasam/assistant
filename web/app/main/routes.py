from datetime import datetime

from app import db
from app.main import bp
from app.models import Family, User

from flask import render_template
from flask_login import current_user, login_required


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='home')


@bp.route('/user/<user_id>')
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)


@bp.route('/family/<family_id>')
@login_required
def family(family_id):
    """
    Render Family page if current user has family
    """
    family = Family.query.get_or_404(family_id)
    return render_template('family.html', family=family)
