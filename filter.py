import logging


import math
import mmh3

__all__ = ["BloomPyFilter"]

logger = logging.getLogger(__name__)


class BloomPyFilter:
    """seeds"""

    SEEDS = [
        543,
        460,
        171,
        876,
        796,
        607,
        650,
        81,
        837,
        545,
        591,
        946,
        846,
        521,
        913,
        636,
        878,
        735,
        414,
        372,
        344,
        324,
        223,
        180,
        327,
        891,
        798,
        933,
        493,
        293,
        836,
        10,
        6,
        544,
        924,
        849,
        438,
        41,
        862,
        648,
        338,
        465,
        562,
        693,
        979,
        52,
        763,
        103,
        387,
        374,
        349,
        94,
        384,
        680,
        574,
        480,
        307,
        580,
        71,
        535,
        300,
        53,
        481,
        519,
        644,
        219,
        686,
        236,
        424,
        326,
        244,
        212,
        909,
        202,
        951,
        56,
        812,
        901,
        926,
        250,
        507,
        739,
        371,
        63,
        584,
        154,
        7,
        284,
        617,
        332,
        472,
        140,
        605,
        262,
        355,
        526,
        647,
        923,
        199,
        518,
    ]

    def __init__(self, backend, capacity=1000_0000, error_rate=0.01):
        self.m = math.ceil(
            capacity * math.log2(math.e) * math.log2(1 / error_rate)
        )
        self.k = math.ceil(math.log1p(2) * self.m / capacity)
        self.mem = math.ceil(self.m / 8 / 1024 / 1024)
        logger.debug(f"bit {self.m} hash {self.k} mem: {self.mem}")
        self.blocknum = math.ceil(
            self.mem / 512
        )
        self.seeds = self.SEEDS[0 : self.k]
        self.backend = backend
        self.backend.init(self.m)

    def add(self, value):
        key = "seg" + str(ord(value[0]) % self.blocknum)
        self.backend.sets(key, self.get_hashs(value))

    def is_exist(self, value):
        key = "seg" + str(ord(value[0]) % self.blocknum)
        return all(self.backend.gets(key, self.get_hashs(value)))

    def get_hashs(self, value):
        for seed in self.seeds:
            hash_ = mmh3.hash(value, seed, signed=False)
            if hash_ > self.m:
                hash_ = hash_ % self.m
            yield hash_
