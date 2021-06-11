import logging


from bitarray import bitarray

__all__ = ["BackendBitArray"]
logger = logging.getLogger(__name__)


class BackendBitArray:
    def __init__(self):
        pass

    def init(self, size):
        self.data = bitarray(size)

    def sets(self, key, postions):
        for pos in postions:
            self.data[pos] = 1

    def gets(self, key, postions):
        return [self.data[pos] for pos in postions]

    def show(self):
        # logger.debug(self.data)
        pass
