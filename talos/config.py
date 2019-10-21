import secrets


class developmentConfig(object):
    DEBUG = True
    DEVELOPMENT = True

    SECRET_KEY = secrets.token_hex(32)
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'True'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class productionConfig(developmentConfig):
    DEVELOPMENT = False
    DEBUG = False
    """
    This option is resource hungry and should never be enabled in Production
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
