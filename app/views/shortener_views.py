from http import HTTPStatus

from flask import current_app as app, Blueprint
from flask import request
from flask.views import MethodView

from url_analytics.tasks import submit_url_log
from app.cache.factories import RedisCacheFactory
from app.views.utilities import response, get_user_id
from urls.crud import URLCrud
from urls.encoders import SequentialEncoder

shortener_blueprint = Blueprint('shortener', __name__)


class URLShortenerAPI(MethodView):
    def post(self):
        cache = RedisCacheFactory().create(name=app.config.get('REDIS_CACHE_NAME'),
                                           redis_host=app.config.get('REDIS_HOST'))
        post_data = request.get_json()
        url_str = post_data.get('url')
        custom_str = post_data.get('custom')
        auth_header = request.headers.get('Authorization')
        user_id = get_user_id(auth_header)
        if user_id is None:
            return response(message='Invalid credentials!', status=HTTPStatus.UNAUTHORIZED)
        crud = URLCrud(SequentialEncoder())
        try:
            url, representation = crud.create_url(user_id, url_str, custom_str)
        except ValueError:
            return response(status=HTTPStatus.BAD_REQUEST, message='url is not formatted correctly!')
        cache[representation] = url.id, url_str
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
        url_id, url = cache[short_representation]
        if url is None:
            url_object = crud.retrieve_url(short_representation)
            if not url_object:
                return response(status=HTTPStatus.NOT_FOUND, message='URL not available')
            url_id, url = url_object.id, url_object.url
            cache[short_representation] = url
        submit_url_log.delay(url_id=url_id, user_agent=request.headers.get('User-Agent'))
        return response(status=HTTPStatus.MOVED_PERMANENTLY, headers={'Location': url})


shortener_blueprint.add_url_rule(
    '/urls',
    view_func=URLShortenerAPI.as_view('url_shortener_create'),
    methods=['POST']
)
shortener_blueprint.add_url_rule(
    '/r/<short_representation>',
    view_func=URLShortenerAPI.as_view('url_shortener_retrieve'),
    methods=['GET']
)
