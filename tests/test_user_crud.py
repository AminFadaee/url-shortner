from unittest import TestCase

from app import Config, create_app, db
from users.crud import UserCRUD
from users.factories import SimpleUserFactory
from users.user import User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@10.0.0.6/url_test'


class TestUserCRUD(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_create_user_stores_the_data_correctly_in_database(self):
        UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        user = User.query.filter(User.email == 'foo@bar.com').one_or_none()
        self.assertEqual(user.email, 'foo@bar.com')

    def test_create_user_raises_error_when_duplicate_email_is_used(self):
        crud = UserCRUD(SimpleUserFactory())
        crud.create_user('spam@bar.com', '12341234')
        self.assertRaises(ValueError, crud.create_user, 'spam@bar.com', '12341234')

    def test_retrieve_user_gets_user_given_correct_password(self):
        crud = UserCRUD(SimpleUserFactory())
        crud.create_user('eggs@bar.com', '12341234')
        user = crud.retrieve_user('eggs@bar.com', '12341234')
        self.assertEqual(user.email, 'eggs@bar.com')

    def test_retrieve_user_raises_value_error_upon_incorrect_password(self):
        crud = UserCRUD(SimpleUserFactory())
        crud.create_user('baz@bar.com', '12341234')
        self.assertRaises(ValueError, crud.retrieve_user, 'baz@bar.com', 'incorrect_password')

    def tearDown(self) -> None:
        User.query.delete()
