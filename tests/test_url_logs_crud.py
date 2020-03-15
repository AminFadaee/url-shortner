from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time

from url_analytics.crud import AnalyticsCrud
from url_analytics.factories import URLLogsCrudFactory
from app import Config, create_app, db
from app import URLLog, User, URL
from urls.crud import URLCrud
from urls.encoders import SequentialEncoder
from users.crud import UserCRUD
from users.factories import SimpleUserFactory


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@10.0.0.6/url_test'


class TestUserCRUD(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        URLLog.query.delete()
        URL.query.delete()
        User.query.delete()
        self.user = UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        self.url, _ = URLCrud(SequentialEncoder()).create_url(self.user.id, 'http://foo.bar.com')
        self.crud = URLLogsCrudFactory()

    def test_url_crud_works_correctly_given_correct_data(self):
        agent = """Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko)
         Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"""
        now = datetime.utcnow()
        with freeze_time(now) as clock:
            url_log: URLLog = self.crud.create(self.url.id, user_agent=agent)
            self.assertEqual(self.url.id, url_log.url_id)
            self.assertEqual('Linux', url_log.os)
            self.assertEqual('Android', url_log.platform)
            self.assertEqual('Chrome', url_log.browser)
            self.assertEqual(now, url_log.timestamp)

    def test_url_crud_works_correctly_given_invalid_agent(self):
        agent = 'invalid agent'
        now = datetime.utcnow()
        with freeze_time(now) as clock:
            url_log: URLLog = self.crud.create(self.url.id, user_agent=agent)
            self.assertEqual(self.url.id, url_log.url_id)
            self.assertEqual(None, url_log.os)
            self.assertEqual(None, url_log.platform)
            self.assertEqual(None, url_log.browser)
            self.assertEqual(now, url_log.timestamp)

    def test_analytics_retrieve_total_view(self):
        self.assertEqual(0, AnalyticsCrud().retrieve_total_view(self.url.id))
        for i in range(5):
            self.crud.create(self.url.id, user_agent='')
        self.assertEqual(5, AnalyticsCrud().retrieve_total_view(self.url.id))

    def tearDown(self) -> None:
        URLLog.query.delete()
        URL.query.delete()
        User.query.delete()
