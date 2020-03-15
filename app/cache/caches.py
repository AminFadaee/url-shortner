from typing import Tuple

from redis import Redis

from app.cache.abstracts import Cache


class RedisCache(Cache):
    def __init__(self, redis: Redis, name: str):
        self.redis = redis
        self.name = name

    def __getitem__(self, item: str):
        return self.get(item)

    def __setitem__(self, key: str, value: Tuple[int, str]):
        self.redis.hset(self.name, str(key), f'{value[0]}:{value[1]}')

    def get(self, item: str):
        result = self.redis.hget(self.name, str(item))
        if result:
            result = result.decode()
            id, url = result.split(':', maxsplit=1)
            return int(id), url
        return None, None
