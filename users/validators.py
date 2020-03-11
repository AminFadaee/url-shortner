import re

from users.abstracts import UserValidator


class SimpleUserValidator(UserValidator):
    def validate_email(self, email):
        email_regex = r'''[^@]+@[^@]+\.[^@]+'''
        if not re.match(email_regex, email):
            raise ValueError

    def validate_password(self, password):
        if len(password) < 6:
            raise ValueError
