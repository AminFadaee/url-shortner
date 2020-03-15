from url_analytics.factories import URLLogsCrudFactory
from app.celery import celery


@celery.task
def submit_url_log(url_id, user_agent):
    URLLogsCrudFactory().create(url_id, user_agent)
