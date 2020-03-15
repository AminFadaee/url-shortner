from unittest import TestCase

from url_analytics.user_agent_parser import HTTPUserAgentParser


class TestUserAgent(TestCase):
    def test_user_agent(self):
        agent = "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) \
        Chrome/5.0.307.11 Safari/532.9"
        parser = HTTPUserAgentParser(agent)
        self.assertEqual('Linux', parser.os)
        self.assertEqual('Linux', parser.platform)
        self.assertEqual('Chrome', parser.browser)

        agent = "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"
        parser = HTTPUserAgentParser(agent)
        self.assertEqual('Linux', parser.os)
        self.assertEqual('Android', parser.platform)
        self.assertEqual('Chrome', parser.browser)

        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        parser = HTTPUserAgentParser(agent)
        self.assertEqual('Windows', parser.os)
        self.assertEqual('Windows', parser.platform)
        self.assertEqual('MSEdge', parser.browser)

        agent = 'invalid agent'
        parser = HTTPUserAgentParser(agent)
        self.assertEqual(None, parser.os)
        self.assertEqual(None, parser.platform)
        self.assertEqual(None, parser.browser)
