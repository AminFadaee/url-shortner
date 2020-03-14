from redis import Redis

from app.cache.abstracts import Cache


class RedisCache(Cache):
    def __init__(self, redis: Redis, name: str):
        self.redis = redis
        self.name = name

    def __getitem__(self, item: str):
        return self.get(item)

    def __setitem__(self, key: str, value: str):
        self.redis.hset(self.name, str(key), str(value))

    def get(self, item: str):
        result = self.redis.hget(self.name, str(item))
        if result:
            result = result.decode()
        return result
