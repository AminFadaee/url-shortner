from celery import Celery

from app.config import Config

celery = Celery(
    'url_app',
    backend='rpc://',
    broker=f"amqp://{Config.RABBIT_USER}:{Config.RABBIT_PASSWORD}@{Config.RABBIT_HOST}:5672"
)
