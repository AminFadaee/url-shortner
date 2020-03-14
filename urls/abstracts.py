from abc import ABC, abstractmethod

from typing import Tuple


class Encoder(ABC):
    @abstractmethod
    def encode(self, seed: int) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def decode(self, encoded_representation: str) -> int:
        pass  # pragma: no cover

    @abstractmethod
    def generate_similar_seeds_range(self, seed: int) -> Tuple[int, int]:
        pass  # pragma: no cover
