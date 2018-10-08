import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'assistant-learning-project'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'assistant.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LANGUAGES = ['en', 'ru', 'ua']

    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '1234567890')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'elena')
    POSTGRES_DB = os.environ.get('DB', 'assistant')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['anelka.dmytriieva@gmail.com', 'test.dev.elena@gmail.com']
