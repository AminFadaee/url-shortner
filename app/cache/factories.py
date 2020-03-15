from redis import Redis

from app.cache.caches import RedisCache


class RedisCacheFactory:
    def create(self, name: str, redis_host: str, db=0, port=6379):
        redis = Redis(
            host=redis_host,
            port=port,
            db=db
        )
        return RedisCache(redis, name)
