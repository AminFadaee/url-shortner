import string
from typing import Tuple

from urls.abstracts import Encoder


class SequentialEncoder(Encoder):
    def __init__(self, characters: str = None, starting_point: int = None):
        self.characters = characters or (string.ascii_letters + string.digits)
        self.starting_point = starting_point or len(self.characters) ** 2

    def encode(self, seed: int) -> str:
        seed += self.starting_point
        result = ''
        while seed:
            result = self.characters[seed % len(self.characters)] + result
            seed //= len(self.characters)
        return result

    def decode(self, encoded_representation: str) -> int:
        result = 0
        base = 1
        for index in range(len(encoded_representation) - 1, -1, -1):
            character = encoded_representation[index]
            location = self.characters.find(character)
            if location == -1:
                raise ValueError
            result += base * location
            base *= len(self.characters)
        return result - self.starting_point

    def generate_similar_seeds_range(self, seed: int) -> Tuple[int, int]:
        min_ = self.decode(self.encode(seed) + '0')
        max_ = self.decode(self.encode(seed) + '9')
        return min_, max_
