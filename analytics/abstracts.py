from abc import ABC, abstractmethod


class UserAgentParser(ABC):
    def __init__(self, agent: str):
        self.user_agent = agent

    @property
    @abstractmethod
    def os(self):
        pass

    @property
    @abstractmethod
    def browser(self):
        pass

    @property
    @abstractmethod
    def platform(self):
        pass
