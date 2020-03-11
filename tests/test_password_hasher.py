from unittest import TestCase

from users.password_hashers import SaltedPasswordHasher


class TestSaltedHashedPasswords(TestCase):
    def test_salted_hashed_password_generates_different_password_hash_each_time(self):
        password = 'this is a password'
        hasher = SaltedPasswordHasher()
        hash_1 = hasher.hash(password)
        hash_2 = hasher.hash(password)
        self.assertNotEqual(hash_1, hash_2)

    def test_salted_hash_verifys_password_correctly(self):
        password = 'this is a password'
        hasher = SaltedPasswordHasher()
        hash = hasher.hash(password)
        self.assertTrue(hasher.verify(hash, password))
