from flask import Flask
from .config import DevelopmentConfig
from .extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes.main import bp as main_bp
    from .routes.chambres import bp as chambres_bp
    from .routes.restaurant import bp as restaurant_bp
    from .routes.salles import bp as salles_bp
    from .routes.reservations import bp as reservations_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chambres_bp, url_prefix='/chambres')
    app.register_blueprint(restaurant_bp, url_prefix='/restaurant')
    app.register_blueprint(salles_bp, url_prefix='/salles')
    app.register_blueprint(reservations_bp, url_prefix='/mes-reservations')

    with app.app_context():
        db.create_all()

    return app
