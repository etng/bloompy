from . import RedisRoaring
import logging

logger = logging.getLogger(__name__)


def test_pipeline():
    conn = RedisRoaring.from_url("redis://localhost:6379/0")
    rk = "test_pipe_rmb"
    pip = conn.pipeline()
    pip.rsetbit(rk, 1, 1)
    pip.rsetbit(rk, 2, 1)
    pip.rgetbit(rk, 1)
    pip.rgetbit(rk, 2)
    logger.debug(pip.execute())
