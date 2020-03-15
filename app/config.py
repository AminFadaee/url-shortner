import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_MAIN_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get('JWT_SECRET')
    JWT_EXPIRY_DAYS = 3
