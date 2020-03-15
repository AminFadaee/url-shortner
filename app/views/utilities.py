from http import HTTPStatus
from typing import Dict

import jwt
from flask import current_app as app
from flask import make_response, jsonify

from authorization.token import JWT


def response(status: HTTPStatus, message: str = None, data: Dict = None, headers=None):
    payload = {
        'data': data or {},
        'message': message
    }
    result = make_response(jsonify(payload))
    if headers:
        result.headers = headers
    return result, status


def get_user_id(auth_header):
    if not auth_header:
        return None
    try:
        auth_token = auth_header.split(" ")[1]
        user_id = int(JWT(app.config.get('JWT_SECRET')).decode(auth_token))
    except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    return user_id
