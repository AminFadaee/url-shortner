from unittest import TestCase

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


class TestUserCRUD(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        URL.query.delete()
        User.query.delete()
        self.user = UserCRUD(SimpleUserFactory()).create_user('foo@bar.com', '12341234')
        self.crud = URLCrud(SequentialEncoder())

    def test_create_url_raises_error_for_incorrectly_formatted_url(self):
        self.assertRaises(ValueError, self.crud.create_url, self.user.id, 'foobar')
        self.assertRaises(ValueError, self.crud.create_url, self.user.id, 'foo.bar.com')

    def test_create_url_generates_different_representation_for_the_same_url_each_time(self):
        _, representation_1 = self.crud.create_url(self.user.id, 'http://foo.bar.com')
        _, representation_2 = self.crud.create_url(self.user.id, 'http://foo.bar.com')
        self.assertNotEqual(representation_1, representation_2)

    def test_create_url_uses_custom_representation_if_not_already_used(self):
        _, representation = self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom')
        self.assertEqual('custom', representation)

    def test_create_url_uses_similar_custom_representation_in_case_of_conflict_in_order(self):
        _, representation_1 = self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom')
        for i in range(10):
            _, representation_i = self.crud.create_url(self.user.id, 'http://foo.bar.com',
                                                       custom_representation='custom')
            self.assertEqual(representation_i, f'custom{i}')
        _, representation_00 = self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom')
        self.assertEqual('custom00', representation_00)

    def test_create_url_uses_similar_custom_representation_in_case_of_conflict_without_order(self):
        self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom')
        self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom0')
        self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom2')
        _, representation = self.crud.create_url(self.user.id, 'http://foo.bar.com', custom_representation='custom')
        self.assertEqual('custom1', representation)

    def test_create_url_raises_value_error_given_invalid_custom_string(self):
        self.assertRaises(ValueError, self.crud.create_url, self.user.id, 'http://foo.bar.com', '!nv^l!d')

    def test_retrieve_url_finds_the_correct_url_given_short_representation(self):
        url_normal, representation_normal = self.crud.create_url(self.user.id, 'http://foo.bar.com')
        url_custom, representation_custom = self.crud.create_url(self.user.id, 'http://foo.bar.com',
                                                                 custom_representation='custom')
        retrieved_url_normal = self.crud.retrieve_url(representation_normal)
        retrieved_url_custom = self.crud.retrieve_url(representation_custom)

        self.assertEqual(url_normal, retrieved_url_normal)
        self.assertEqual(url_custom, retrieved_url_custom)

    def test_retrieve_url_returns_none_given_unavailable_representation(self):
        retrieved_url_unavailable = self.crud.retrieve_url('unavailable')
        self.assertIsNone(retrieved_url_unavailable)

    def test_retrieve_url_returns_none_given_invalid_representation(self):
        retrieved_url_invalid = self.crud.retrieve_url('!nv^lID')
        self.assertIsNone(retrieved_url_invalid)

    def tearDown(self) -> None:
        URL.query.delete()
        User.query.delete()
