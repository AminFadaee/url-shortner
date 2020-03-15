from http import HTTPStatus
from typing import Dict

from flask import Blueprint, request, make_response, jsonify
from flask import current_app as app
from flask.views import MethodView

from app.config import Config
from authorization.token import JWT
from users.crud import UserCRUD
from users.factories import SimpleUserFactory
from users.user import User
from users.validators import SimpleUserValidator

auth_blueprint = Blueprint('auth', __name__)


def response(message: str, status: HTTPStatus, data: Dict = None):
    payload = {
        'data': data or {},
        'message': message
    }
    return make_response(jsonify(payload)), status


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


auth_blueprint.add_url_rule('/auth/register', view_func=RegisterAPI.as_view('register_api'), methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=LoginAPI.as_view('login_api'), methods=['POST'])
