from typing import Type

from app.database import db
from url_analytics.abstracts import UserAgentParser
from url_analytics.url_logs import URLLog


class UrlLogsCrud:
    def __init__(self, url_agent_parser_class: Type[UserAgentParser]):
        self.url_agent_parser_class = url_agent_parser_class

    def create_user_log(self, url_id, user_agent):
        agent = self.url_agent_parser_class(user_agent)
        url_log = URLLog(url_id, agent.os, agent.platform, agent.browser)
        db.session.add(url_log)
        db.session.commit()
        return url_log


class AnalyticsCrud:
    def retrieve_total_view(self, url_id: int):
        return URLLog.query.filter(URLLog.url_id == url_id).count()
