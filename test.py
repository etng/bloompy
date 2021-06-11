import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from datetime import datetime, timedelta
    from bloompy import BloomPyFilter
    from bloompy.backend.bitarray import BackendBitArray
    from bloompy.backend.redisbm import BackendRedis
    from bloompy.backend.redisrbm import BackendRedisRoaring

    logging.basicConfig(
        filename="test.log",
        level=logging.DEBUG,
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    backend_redis = BackendRedis(
        "redis://localhost:6379/0",
        "benchmark:bloomfilterv2:bm",
    )
    backend_redis_roaring = BackendRedisRoaring(
        "redis://localhost:6379/0",
        "benchmark:bloomfilterv2:rbm",
    )
    backend_bitarray = BackendBitArray()
    sentence = "There are several ways to specify a database number. The parse function will return the first specified option"

    start_num = 2000_0000
    item_cnt = 10_0000
    if 1:
        backend = backend_redis
        logger.debug(
            f"using backend {backend.name()} start_num {start_num} item_cnt {item_cnt}"
        )
        bf = BloomPyFilter(backend)
        begin_time = datetime.now()
        backend.show()
        # for word in sentence.split():
        for word in range(start_num, start_num + item_cnt + 1):
            word = str(word)
            if bf.is_exist(word):
                # logger.debug(f'{word} exists, continue')
                pass
            else:
                bf.add(word)
                # logger.debug(f'{word} missing, add it now')
        backend.show()
        duration = datetime.now() - begin_time
        logger.debug(f"duration: {duration}")
        exists = str(start_num + 1)
        logger.debug(f"checking {exists}:{bf.is_exist(exists)}")
        not_exists = str(start_num + item_cnt + 1)
        logger.debug(f"checking {not_exists}: {bf.is_exist(not_exists)}")
    if 1:
        backend = backend_redis_roaring
        logger.debug(
            f"using backend {backend.name()} start_num {start_num} item_cnt {item_cnt}"
        )
        bf = BloomPyFilter(backend)
        begin_time = datetime.now()
        backend.show()
        # for word in sentence.split():
        for word in range(start_num, start_num + item_cnt + 1):
            word = str(word)
            if bf.is_exist(word):
                # logger.debug(f'{word} exists, continue')
                pass
            else:
                bf.add(word)
                # logger.debug(f'{word} missing, add it now')
        backend.show()
        duration = datetime.now() - begin_time
        logger.debug(f"duration: {duration}")
        exists = str(start_num + 1)
        logger.debug(f"checking {exists}:{bf.is_exist(exists)}")
        not_exists = str(start_num + item_cnt + 1)
        logger.debug(f"checking {not_exists}: {bf.is_exist(not_exists)}")
    # logger.debug('*' * 80)
    # backend.show()
    # for word in sentence.split():
    #     if bf.is_exist(word):
    #         logger.debug(f'{word} exists')
    #     else:
    #         logger.debug(f'{word} missing, bad')
    logger.debug("done")
    print("done")
