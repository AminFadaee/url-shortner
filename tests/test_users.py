from unittest import TestCase

from users.factories import SimpleUserFactory


class TestSimpleUser(TestCase):
    def test_user_class_initializes_with_email_and_password_and_sets_email_correctly(self):
        user = SimpleUserFactory().create(email='foo@bar.com', password='123123')
        self.assertEqual('foo@bar.com', user.email)

    def test_create_user_rejects_invalid_emails_with_validation_error(self):
        self.assertRaises(ValueError, SimpleUserFactory().create, 'invalid_email', '123123')
        self.assertRaises(ValueError, SimpleUserFactory().create, 'invalid@email', '123123')

    def test_create_user_rejects_passwords_with_length_less_than_6_with_validation_error(self):
        self.assertRaises(ValueError, SimpleUserFactory().create, 'foo@bar.com', '1')
        self.assertRaises(ValueError, SimpleUserFactory().create, 'foo@bar.com', '12')
        self.assertRaises(ValueError, SimpleUserFactory().create, 'foo@bar.com', '123')
        self.assertRaises(ValueError, SimpleUserFactory().create, 'foo@bar.com', '1234')
        self.assertRaises(ValueError, SimpleUserFactory().create, 'foo@bar.com', '12345')

    def test_user_objects_store_hashed_passwords(self):
        user = SimpleUserFactory().create(email='foo@bar.com', password='123123')
        self.assertFalse(hasattr(user, 'password'))
        self.assertNotEqual(user.hashed_password, '123123')
