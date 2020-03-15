from flask_testing import TestCase

from app import Config, create_app, db
from app import URLLog, URL, User
from url_analytics.factories import URLLogsCrudFactory
from urls.crud import URLCrud
from urls.encoders import SequentialEncoder
from users.crud import UserCRUD
from users.factories import SimpleUserFactory


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@10.0.0.6/url_test'
    JWT_SECRET = 'the secret'


class TestAuthViews(TestCase):
    def create_app(self):
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
        return self.app

    def setUp(self) -> None:
        response = self.client.post('/auth/login', json={'email': 'foo@bar.com', 'password': '12341234'})
        self.token = response.json['data']['auth_token']

    def test_analytics_total_api_works_correctly(self):
        response = self.client.get(f'/analytics/{self.url.id}', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.json['data']['total_view'])
        for i in range(5):
            self.crud.create(self.url.id, user_agent='')
        response = self.client.get(f'/analytics/{self.url.id}', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, response.json['data']['total_view'])

    def test_analytics_total_gives_401_given_no_or_bad_token(self):
        response = self.client.get(f'/analytics/{self.url.id}', headers={'Authorization': 'bad token'})
        self.assertEqual(401, response.status_code)
        response = self.client.get(f'/analytics/{self.url.id}')
        self.assertEqual(401, response.status_code)
