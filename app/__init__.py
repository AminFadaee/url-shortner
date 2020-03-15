from flask import Flask

from app.config import Config
from app.database import db
from app.views.auth_views import auth_blueprint
from app.views.analytic_views import analytics_blueprint
from app.views.shortner_views import shortner_blueprint


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(shortner_blueprint)
    app.register_blueprint(analytics_blueprint)
    return app

from users.user import User
from urls.url import URL
from url_analytics.url_logs import URLLog