import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))

    db.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
