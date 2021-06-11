# Python BloomFilter With multiple backends

## Server Config
* get code `git clone https://github.com/aviggiano/redis-roaring.git`
* install dependencies like `cmake`
* `./configure.sh`
* cp `dist/libredis-roaring.so` to your host `cp dist/libredis-roaring.so /opt/libs/libredis-roaring.so`
* add `loadmodule /opt/libs/libredis-roaring.so` to `redis.conf` and restart redis `systemctl restart redis`

## Client Update

### only roaring
```python
from bloompy.redis_roaring import RedisRoaring
conn = RedisRoaring.from_url("redis://localhost:6379/0")
rk = "test_roaring"
pip = conn.pipeline()
pip.rsetbit(rk, 1, 1)
pip.rsetbit(rk, 2, 1)
pip.rgetbit(rk, 1)
pip.rgetbit(rk, 2)
print(pip.execute())
```

### use filter
```python
from datetime import datetime, timedelta
from bloompy import BloomPyFilter
from bloompy.backend.bitarray import BackendBitArray
start_num = 2000_0000
item_cnt = 10_0000
    backend = BackendBitArray()
    bf = BloomPyFilter(backend)
    begin_time = datetime.now()
    backend.show()
    for word in range(start_num, start_num + item_cnt + 1):
        word = str(word)
        if bf.is_exist(word):
            pass
        else:
            bf.add(word)
    backend.show()
    duration = datetime.now() - begin_time
    print(f"duration: {duration}")
    exists = str(start_num + 1)
    print(f"checking {exists}:{bf.is_exist(exists)}")
    not_exists = str(start_num + item_cnt + 1)
    print(f"checking {not_exists}: {bf.is_exist(not_exists)}")
```