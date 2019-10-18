from flask import Flask
from .middleware import activate_middleware


def make_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    activate_middleware(app)
    return app
