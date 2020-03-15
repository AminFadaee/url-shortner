import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_MAIN_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get('JWT_SECRET')
    JWT_EXPIRY_DAYS = 3
    REDIS_HOST = '10.0.0.5'
    REDIS_CACHE_NAME = 'cache'
    RABBIT_HOST = '10.0.0.4'
    RABBIT_USER = 'url'
    RABBIT_PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS')
