import httpagentparser

from analytics.abstracts import UserAgentParser


class HTTPUserAgentParser(UserAgentParser):
    @property
    def platform(self):
        platform_dict = httpagentparser.detect(self.user_agent).get('platform') or {}
        return platform_dict.get('name')

    @property
    def browser(self):
        browser_dict = httpagentparser.detect(self.user_agent).get('browser') or {}
        return browser_dict.get('name')

    @property
    def os(self):
        os_dict = httpagentparser.detect(self.user_agent).get('os') or {}
        return os_dict.get('name')
