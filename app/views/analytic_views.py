from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask.views import MethodView

from url_analytics.crud import AnalyticsCrud
from app.views.utilities import response, get_user_id

analytics_blueprint = Blueprint('url_analytics', __name__)


class TotalAnalyticsAPI(MethodView):
    def get(self, url_id):
        auth_header = request.headers.get('Authorization')
        user_id = get_user_id(auth_header)
        if user_id is None:
            return response(message='Invalid credentials!', status=HTTPStatus.UNAUTHORIZED)
        total_view = AnalyticsCrud().retrieve_total_view(url_id)
        return response(
            status=HTTPStatus.OK,
            data={
                'url_id': url_id,
                'total_view': total_view
            }
        )


analytics_blueprint.add_url_rule(
    '/analytics/<url_id>',
    view_func=TotalAnalyticsAPI.as_view('total_analytics'),
    methods=['GET']
)
