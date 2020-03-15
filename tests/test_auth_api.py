from flask_testing import TestCase

from app import Config, create_app, db
from users.crud import UserCRUD
from users.factories import SimpleUserFactory
from users.user import User


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
        User.query.delete()
        return self.app

    def test_register_api_creates_user_correctly(self):
        response = self.client.post('/auth/register', json={'email': 'foo@bar.com', 'password': '123123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('auth_token', response.json['data'])
        user = User.query.filter(User.email == 'foo@bar.com').one_or_none()
        self.assertIsNotNone(user)

    def test_register_api_returns_400_with_invalid_data(self):
        response = self.client.post('/auth/register', json={'email': 'invalid_email', 'password': '123123'})
        self.assertEqual(response.status_code, 400)

    def test_register_api_returns_409_when_user_exists(self):
        UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        response = self.client.post('/auth/register', json={'email': 'foo@bar.com', 'password': '123123'})
        self.assertEqual(response.status_code, 409)

    def test_login_api_gives_auth_token_given_correct_email_and_password(self):
        UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        response = self.client.post('/auth/login', json={'email': 'foo@bar.com', 'password': '12341234'})
        self.assertEqual(200, response.status_code)
        self.assertIn('auth_token', response.json['data'])

    def test_login_api_gives_401_given_incorrect_password(self):
        UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        response = self.client.post('/auth/login', json={'email': 'foo@bar.com', 'password': '123123'})
        self.assertEqual(401, response.status_code)

    def test_login_api_returns_400_with_invalid_data(self):
        response = self.client.post('/auth/login', json={'email': 'invalid_email', 'password': '123123'})
        self.assertEqual(response.status_code, 400)
