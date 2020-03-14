from typing import Type

from analytics.abstracts import UserAgentParser
from analytics.url_logs import URLLog
from app.database import db


class UrlLogsCrud:
    def __init__(self, url_agent_parser_class: Type[UserAgentParser]):
        self.url_agent_parser_class = url_agent_parser_class

    def create_user_log(self, user_id, url_id, user_agent):
        agent = self.url_agent_parser_class(user_agent)
        url_log = URLLog(user_id, url_id, agent.os, agent.platform, agent.browser)
        db.session.add(url_log)
        db.session.commit()
        return url_log
