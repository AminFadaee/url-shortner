from datetime import datetime, timedelta

import jwt


class JWT:
    def __init__(self, secret):
        self.secret = secret

    def encode(self, user_id: int, expiration: int):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=expiration),
            'iat': datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode(self, auth_token):
        payload = jwt.decode(auth_token, self.secret)
        return payload['sub']
