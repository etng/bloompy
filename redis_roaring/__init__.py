from redis.client import Pipeline
from redis import StrictRedis
import logging

logger = logging.getLogger(__name__)


class RedisRoaring(StrictRedis):
    def __init__(self, *args, **kwargs):
        super(RedisRoaring, self).__init__(*args, **kwargs)
        self.set_response_callback("R.SETBIT", int)
        self.set_response_callback("R.GETBIT", int)

    @classmethod
    def from_url(cls, url, db=None, **kwargs):
        from redis import ConnectionPool

        connection_pool = ConnectionPool.from_url(url, db=db, **kwargs)
        return cls(connection_pool=connection_pool)

    def rgetbit(self, name, offset):
        "Returns a boolean indicating the value of ``offset`` in ``name``"
        return self.execute_command("R.GETBIT", name, offset)

    def rsetbit(self, name, offset, value):
        """
        Flag the ``offset`` in ``name`` as ``value``. Returns a boolean
        indicating the previous value of ``offset``.
        """
        value = value and 1 or 0
        return self.execute_command("R.SETBIT", name, offset, value)

    def pipeline(self, transaction=True, shard_hint=None):
        """
        Return a new pipeline object that can queue multiple commands for
        later execution. ``transaction`` indicates whether all commands
        should be executed atomically. Apart from making a group of operations
        atomic, pipelines are useful for reducing the back-and-forth overhead
        between the client and server.
        """
        return RoaringPipeline(
            self.connection_pool, self.response_callbacks, transaction, shard_hint
        )


class RoaringPipeline(RedisRoaring, Pipeline):
    pass
