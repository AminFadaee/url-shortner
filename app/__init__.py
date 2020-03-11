from flask import Flask

from app.config import Config
from app.database import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app

from users.user import User