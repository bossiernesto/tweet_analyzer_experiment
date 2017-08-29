from abc import ABCMeta

class Persistance:
    __metaclass__ = ABCMeta

    def __init__(self, filename, header):
        self.filename = filename
        self.persist_header(header)

    def persist_header(self, header):
        raise NotImplementedError

    def persist_data(self, results):
        raise NotImplementedError
