from talos.appfactory import make_app
from talos.config import DevelopmentConfig

"""TM
Construct the app here and not in __init__.py, this makes it explicit as to which config is used.

In layout.html: I would always download your bootstrap dependencies and serve them yourself. No need
to make your app depend on some unknown CDN somewhere.
"""
app = make_app(DevelopmentConfig())

if __name__ == '__main__':
    # Turn debug off when used on server!
    app.run()
