import binascii
import hashlib
import os

from users.abstracts import PasswordHasher


class SaltedPasswordHasher(PasswordHasher):
    def hash(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        hashed_password = binascii.hexlify(hashed_password)
        return (salt + hashed_password).decode('ascii')

    def verify(self, saved_hash, password):
        salt = saved_hash[:64]
        stored_password = saved_hash[64:]
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 100000)
        hashed_password = binascii.hexlify(hashed_password).decode('ascii')
        return hashed_password == stored_password
