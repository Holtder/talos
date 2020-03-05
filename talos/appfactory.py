import logging

from flask import Flask
from .config import productionConfig
from . import routes, tasks
from .tasks import celery


logger = logging.getLogger()

"""This script makes use of code written by Zenyui https://github.com/zenyui/celery-flask-factory
Code that allows for celery and flask to each have their own entrypoint without getting in eachothers way
when importing other parts of the app.
"""


def create_app(debug=False):
    return entrypoint(debug=debug, mode='app')


def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')


def entrypoint(debug=False, mode='app'):
    """Both create functions lead back to this function, passing different arguments based on
    which call is made"""

    assert isinstance(mode, str), 'bad mode type "{}"'.format(type(mode))
    assert mode in ('app', 'celery'), 'bad mode "{}"'.format(mode)

    app = Flask(__name__)

    app.debug = debug

    # Configure Flask, the logging file and celery
    configure_app(app)
    configure_logging(debug=debug)
    configure_celery(app, tasks.celery)

    # Register the blueprint for all the pages
    app.register_blueprint(routes.talosBP, url_prefix='')

    if mode == 'app':
        return app
    elif mode == 'celery':
        return celery


def configure_app(app):

    logger.info('configuring flask app')
    # app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL')
    # app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND')

    # in Talos.config two objects are defined, whose members represent a set of configs for Flask
    app.config.from_object(productionConfig)
    from .models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def configure_celery(app, celery):

    # set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task

    class AppContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()


def configure_logging(debug=False):

    root = logging.getLogger()
    h = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s (%(name)s) %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(fmt)

    root.addHandler(h)

    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)
