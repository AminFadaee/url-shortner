from sqlalchemy.exc import IntegrityError

from app.database import db
from users.abstracts import UserFactory
from users.user import User


class UserCRUD:
    def __init__(self, user_factory: UserFactory):
        self.user_factory = user_factory

    def create_user(self, email, password):
        try:
            user = self.user_factory.create(email, password)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError

    def retrieve_user(self, email, password):
        user = self.retrieve_user_without_password(email)
        if not user:
            return None
        if user.verify_password(password):
            return user
        else:
            raise ValueError

    def retrieve_user_without_password(self, email):
        orm_user = User.query.filter(User.email == email).one_or_none()
        if orm_user:
            return self.user_factory.from_orm(orm_user)
        return None
