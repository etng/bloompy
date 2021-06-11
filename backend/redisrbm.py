import logging
from ..redis_roaring import RedisRoaring
__all__=['BackendRedisRoaring']
logger = logging.getLogger(__name__)

class BackendRedisRoaring:
    def __init__(self, redis_url, key_prefix):
        """
        redis://[[username]:[password]]@localhost:6379/0
        """
        self.conn = RedisRoaring.from_url(redis_url)
        self.key_prefix = key_prefix

    def name(self):
        return "redis-roaring"

    def init(self, size):
        pass

    def show(self):
        memory = self.conn.info("memory")
        logger.debug(
            f'used: {memory["used_memory"]} {memory["used_memory_human"]}  rss: {memory["used_memory_rss"]} {memory["used_memory_rss_human"]}'
        )

    def sets(self, key, postions):
        rk = f"{self.key_prefix}:{key}"
        with self.conn.pipeline() as pipe:
            [pipe.rsetbit(rk, postion, 1) for postion in postions]
            pipe.execute()

    def gets(self, key, postions):
        rk = f"{self.key_prefix}:{key}"
        with self.conn.pipeline() as pipe:
            [pipe.rgetbit(rk, postion) for postion in postions]
            return pipe.execute()

