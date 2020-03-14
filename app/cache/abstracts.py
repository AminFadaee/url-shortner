from abc import ABC, abstractmethod


class Cache(ABC):
    @abstractmethod
    def __getitem__(self, item: str):
        pass  # pragma: no cover

    @abstractmethod
    def __setitem__(self, key: str, value: str):
        pass  # pragma: no cover

    @abstractmethod
    def get(self, item: str):
        pass  # pragma: no cover
