from users.abstracts import UserFactory
from users.password_hashers import SaltedPasswordHasher
from users.user import User
from users.validators import SimpleUserValidator


class SimpleUserFactory(UserFactory):
    def create(self, email, password):
        return User(SaltedPasswordHasher(), SimpleUserValidator(), email, password)

    def from_orm(self, orm_user: User):
        orm_user.hasher = SaltedPasswordHasher()
        orm_user.validator = SimpleUserValidator
        return orm_user
