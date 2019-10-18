import secrets


class DevelopmentConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    """TM
    Using a random secret key on dev is fine I guess. It is used to protect user sessions which as
    long as you don't have logins does not matter all that much. I've used a config before that 
    checks the DB for a secret key and if there is nothing there it uses a random one and stores it.
    Oh, one thing: 16hex=8bytes of randomness=64bit is not enough to withstand brute-force. Make it
    32 and you are fine.
    """
    SECRET_KEY = secrets.token_hex(16)
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'True'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

"""TM
Yummy, I love inheritance. Personally I always do it the other way round but that is a preference.
Why do I do that? I always feel that the ProductionConfig has the strictest possible settings and that
you loosen them up in the development environment. By doing it that way you can never by accident leak
things from development into production. The disadvantage bein of course that if you add a new setting
to your dev environment and forget to add it for production you are in trouble. So you kinda also need
a staging environment then. Decisions decisions.
"""
class ProductionConfig(DevelopmentConfig):
    DEVELOPMENT = False
    DEBUG = False
    """
    This option is resource hungry and should never be enabled in Production
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'