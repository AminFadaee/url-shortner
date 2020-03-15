from url_analytics.crud import UrlLogsCrud
from url_analytics.user_agent_parser import HTTPUserAgentParser


class URLLogsCrudFactory:
    def create(self, url_id, user_agent):
        return UrlLogsCrud(HTTPUserAgentParser).create_user_log(url_id, user_agent)
