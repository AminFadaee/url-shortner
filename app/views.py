from http import HTTPStatus
from typing import Dict

import jwt
from flask import Blueprint, request, make_response, jsonify
from flask import current_app as app
from flask.views import MethodView

from app.cache.factories import RedisCacheFactory
from app.config import Config
from authorization.token import JWT
from urls.crud import URLCrud
from urls.encoders import SequentialEncoder
from users.crud import UserCRUD
from users.factories import SimpleUserFactory
from users.user import User
from users.validators import SimpleUserValidator

auth_blueprint = Blueprint('auth', __name__)


def response(status: HTTPStatus, message: str = None, data: Dict = None, headers=None):
    payload = {
        'data': data or {},
        'message': message
    }
    result = make_response(jsonify(payload))
    if headers:
        result.headers = headers
    return result, status


class RegisterAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            SimpleUserValidator().validate_email(post_data.get('email'))
            SimpleUserValidator().validate_password(post_data.get('password'))
        except ValueError:
            return response(message='Incorrect data!', status=HTTPStatus.BAD_REQUEST)
        crud = UserCRUD(SimpleUserFactory())
        user = User.query.filter(User.email == post_data.get('email')).one_or_none()
        if not user:
            user = crud.create_user(email=post_data.get('email'), password=post_data.get('password'))
            auth_token = JWT(app.config.get('JWT_SECRET')).encode(user.id, Config.JWT_EXPIRY_DAYS)
            return response(
                data={'auth_token': auth_token.decode()},
                message='Successfully registered.',
                status=HTTPStatus.CREATED
            )
        else:
            return response(message='User already exists. Please Log in.', status=HTTPStatus.CONFLICT)


class LoginAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            SimpleUserValidator().validate_email(post_data.get('email'))
            SimpleUserValidator().validate_password(post_data.get('password'))
        except ValueError:
            return response(message='Incorrect data!', status=HTTPStatus.BAD_REQUEST)

        try:
            crud = UserCRUD(SimpleUserFactory())
            user = crud.retrieve_user(email=post_data.get('email'), password=post_data.get('password'))
            token = JWT(app.config.get('JWT_SECRET')).encode(user.id, Config.JWT_EXPIRY_DAYS)
            return response(data={'auth_token': token.decode()}, message='Successfully logged in.',
                            status=HTTPStatus.OK)
        except ValueError:
            return response(message='email and/or password is not correct!', status=HTTPStatus.UNAUTHORIZED)


class URLShortnerAPI(MethodView):
    def post(self):
        cache = RedisCacheFactory().create(name=app.config.get('REDIS_CACHE_NAME'),
                                           redis_host=app.config.get('REDIS_HOST'))
        post_data = request.get_json()
        url_str = post_data.get('url')
        custom_str = post_data.get('custom')
        auth_header = request.headers.get('Authorization')
        user_id = self._get_user_id(auth_header)
        if user_id is None:
            return response(message='Invalid credentials!', status=HTTPStatus.UNAUTHORIZED)
        crud = URLCrud(SequentialEncoder())
        try:
            url, representation = crud.create_url(user_id, url_str, custom_str)
        except ValueError:
            return response(status=HTTPStatus.BAD_REQUEST, message='url is not formatted correctly!')
        cache[representation] = url_str
        return response(
            data={
                'id': url.id,
                'original_url': url_str,
                'short_uri': f'r/{representation}'
            },
            message='URL shortened successfully!',
            status=HTTPStatus.CREATED
        )

    def get(self, short_representation):
        cache = RedisCacheFactory().create(name=app.config.get('REDIS_CACHE_NAME'),
                                           redis_host=app.config.get('REDIS_HOST'))
        crud = URLCrud(SequentialEncoder())
        url = cache[short_representation]
        if url is None:
            url_object = crud.retrieve_url(short_representation)
            if not url_object:
                return response(status=HTTPStatus.NOT_FOUND, message='URL not available')
            url = url_object.url
            cache[short_representation] = url
        return response(status=HTTPStatus.MOVED_PERMANENTLY, headers={'Location': url})

    def _get_user_id(self, auth_header):
        if not auth_header:
            return None
        try:
            auth_token = auth_header.split(" ")[1]
            user_id = int(JWT(app.config.get('JWT_SECRET')).decode(auth_token))
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        return user_id


auth_blueprint.add_url_rule('/auth/register', view_func=RegisterAPI.as_view('register_api'), methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=LoginAPI.as_view('login_api'), methods=['POST'])
auth_blueprint.add_url_rule('/urls', view_func=URLShortnerAPI.as_view('url_shortner_create'), methods=['POST'])
auth_blueprint.add_url_rule(
    '/r/<short_representation>',
    view_func=URLShortnerAPI.as_view('url_shortner_retrieve'),
    methods=['GET']
)
