from flask_testing import TestCase

from app import Config, create_app, db
from urls.crud import URLCrud
from urls.encoders import SequentialEncoder
from urls.url import URL
from users.crud import UserCRUD
from users.factories import SimpleUserFactory
from users.user import User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@10.0.0.6/url_test'
    JWT_SECRET = 'the secret'
    REDIS_CACHE_NAME = 'test_cache'


class TestAuthViews(TestCase):
    def create_app(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        URL.query.delete()
        User.query.delete()
        self.user = UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        self.crud = URLCrud(SequentialEncoder())
        return self.app

    def setUp(self) -> None:
        response = self.client.post('/auth/login', json={'email': 'foo@bar.com', 'password': '12341234'})
        self.token = response.json['data']['auth_token']

    def test_url_shortner_get_redirects_to_correct_link(self):
        url, representation = self.crud.create_url(self.user.id, 'https://foo.bar.com')
        response = self.client.get(f'/r/{representation}')
        self.assertEqual(301, response.status_code)
        self.assertEqual(response.headers['Location'], 'https://foo.bar.com')

    def test_url_shortner_get_returns_404_for_unavailable__or_invalid_url(self):
        response = self.client.get('/r/unavailable')
        self.assertEqual(404, response.status_code)
        response = self.client.get('/r/in.vali.d')
        self.assertEqual(404, response.status_code)

    def test_url_shortner_post_returns_401_for_unauthorized_users(self):
        response = self.client.post('/urls', json={'url': 'https://foo.com'})
        self.assertEqual(401, response.status_code)

    def test_url_shortner_post_returns_401_for_bad_token(self):
        response = self.client.post(
            '/urls',
            json={'url': 'bad.url'},
            headers={'Authorization': f'Bearer BADTOKEN'}
        )
        self.assertEqual(401, response.status_code)

    def test_url_shortner_post_returns_400_for_bad_urls(self):
        response = self.client.post(
            '/urls',
            json={'url': 'bad.url'},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(400, response.status_code)

    def test_url_shortner_works_correctly_given_token_and_correct_url(self):
        response = self.client.post(
            '/urls',
            json={'url': 'https://foo.bar.com?var=3&another_var=2'},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual('https://foo.bar.com?var=3&another_var=2', response.json['data']['original_url'])
        self.assertTrue('short_uri' in response.json['data'])
        short_uri = response.json['data']['short_uri']
        response = self.client.get(f'{short_uri}')
        self.assertEqual(301, response.status_code)
        self.assertEqual(response.headers['Location'], 'https://foo.bar.com?var=3&another_var=2')

    def test_url_shortner_uses_cache_if_exists(self):
        short_uri = self.client.post(
            '/urls',
            json={'url': 'https://foo.bar.com?var=3&another_var=2'},
            headers={'Authorization': f'Bearer {self.token}'}
        ).json['data']['short_uri']
        url = URL.query.one_or_none()
        url.url = 'something_different'
        db.session.commit()
        response = self.client.get(f'{short_uri}')
        self.assertEqual(301, response.status_code)
        self.assertEqual(response.headers['Location'], 'https://foo.bar.com?var=3&another_var=2')

    def tearDown(self) -> None:
        URL.query.delete()
        User.query.delete()
