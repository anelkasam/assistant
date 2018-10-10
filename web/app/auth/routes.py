from flask import jsonify, request
from sqlalchemy import exc

from app import db
from app.auth import bp
from app.auth.models import User, Family


@bp.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@bp.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': f'Invalid json'
    }
    if not post_data:
        return jsonify(response_object), 400

    name = post_data.get('name')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(name=name, email=email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        response_object['message'] = 'Sorry. That email already exists.'
        return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@bp.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    user = User.query.filter_by(id=user_id).first()
    response_object = {
        'status': 'success',
        'data': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'active': user.active
        }
    }
    return jsonify(response_object), 200


@bp.route('/families', methods=['POST'])
def add_family():
    post_data = request.get_json()
    last_name = post_data.get('last_name')
    db.session.add(Family(last_name=last_name))
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': f'{last_name} was added!'
    }
    return jsonify(response_object), 201
