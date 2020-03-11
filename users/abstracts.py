from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password):
        pass  # pragma: no cover

    @abstractmethod
    def verify(self, saved_hash, password):
        pass  # pragma: no cover


class UserValidator(ABC):
    @abstractmethod
    def validate_email(self, email):
        pass  # pragma: no cover

    @abstractmethod
    def validate_password(self, password):
        pass  # pragma: no cover


class UserFactory(ABC):
    @abstractmethod
    def create(self, email: str, password: str):
        pass  # pragma: no cover

    @abstractmethod
    def from_orm(self, orm_user):
        pass  # pragma: no cover
