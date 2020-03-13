from app.database import db
from users.abstracts import PasswordHasher, UserValidator


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    email = db.Column(db.String(length=50), index=True, unique=True)
    hashed_password = db.Column(db.String(length=200))

    def __init__(self, hasher: PasswordHasher, validator: UserValidator, email: str, password: str):
        self.validator = validator
        self.validator.validate_email(email)
        self.validator.validate_password(password)
        self.hasher = hasher
        self.email = email
        self.hashed_password = self.hasher.hash(password)

    def verify_password(self, password):
        return self.hasher.verify(self.hashed_password, password)
