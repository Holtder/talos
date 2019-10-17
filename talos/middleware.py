def activate_middleware(app):
    from .models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from .tasks import celery
    celery.conf.update(app.config)
    from .routes import talosBP
    app.register_blueprint(talosBP)
    return