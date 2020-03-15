from abc import ABC, abstractmethod
from typing import Tuple


class Cache(ABC):
    @abstractmethod
    def __getitem__(self, item: str):
        pass  # pragma: no cover

    @abstractmethod
    def __setitem__(self, key: str, value: Tuple[int, str]):
        pass  # pragma: no cover

    @abstractmethod
    def get(self, item: str):
        pass  # pragma: no cover
