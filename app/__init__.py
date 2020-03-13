from flask import Flask

from app.views import auth_blueprint
from app.config import Config
from app.database import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(auth_blueprint)
    return app

from users.user import User