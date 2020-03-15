from flask_testing import TestCase

from app.views.shortener_views import submit_url_log
from app import Config, create_app
from app import URLLog, URL, User
from app.database import db
from urls.crud import URLCrud
from urls.encoders import SequentialEncoder
from users.crud import UserCRUD
from users.factories import SimpleUserFactory


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
        URLLog.query.delete()
        URL.query.delete()
        User.query.delete()
        db.create_all()
        self.user = UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        self.crud = URLCrud(SequentialEncoder())
        submit_url_log.delay = submit_url_log
        return self.app

    def setUp(self) -> None:
        response = self.client.post('/auth/login', json={'email': 'foo@bar.com', 'password': '12341234'})
        self.token = response.json['data']['auth_token']

    def test_url_shortener_get_redirects_to_correct_link(self):
        url, representation = self.crud.create_url(self.user.id, 'https://foo.bar.com')
        response = self.client.get(f'/r/{representation}')
        self.assertEqual(301, response.status_code)
        self.assertEqual(response.headers['Location'], 'https://foo.bar.com')

    def test_url_shortener_create_url_log_correctly(self):
        url, representation = self.crud.create_url(self.user.id, 'https://foo.bar.com')
        response = self.client.get(
            f'/r/{representation}',
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv)'
                                   'AppleWebKit/537.36 (KHTML, like Gecko)'
                                   'Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'}
        )
        url_log: URLLog = URLLog.query.filter(URLLog.url_id == url.id).one_or_none()
        self.assertEqual(url.id, url_log.url_id)
        self.assertEqual('Chrome', url_log.browser)
        self.assertEqual('Linux', url_log.os)
        self.assertEqual('Android', url_log.platform)

    def test_url_shortener_get_returns_404_for_unavailable__or_invalid_url(self):
        response = self.client.get('/r/unavailable')
        self.assertEqual(404, response.status_code)
        response = self.client.get('/r/in.vali.d')
        self.assertEqual(404, response.status_code)

    def test_url_shortener_post_returns_401_for_unauthorized_users(self):
        response = self.client.post('/urls', json={'url': 'https://foo.com'})
        self.assertEqual(401, response.status_code)

    def test_url_shortener_post_returns_401_for_bad_token(self):
        response = self.client.post(
            '/urls',
            json={'url': 'bad.url'},
            headers={'Authorization': f'Bearer BADTOKEN'}
        )
        self.assertEqual(401, response.status_code)

    def test_url_shortener_post_returns_400_for_bad_urls(self):
        response = self.client.post(
            '/urls',
            json={'url': 'bad.url'},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(400, response.status_code)

    def test_url_shortener_works_correctly_given_token_and_correct_url(self):
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

    def test_url_shortener_uses_cache_if_exists(self):
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
