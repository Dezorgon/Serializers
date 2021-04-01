from abc import abstractmethod


class Parser(object):
    @abstractmethod
    def dump(self, obj, fp):
        pass

    @abstractmethod
    def dumps(self, obj) -> str:
        pass

    @abstractmethod
    def load(self, fp):
        pass

    @abstractmethod
    def loads(self, s):
        pass
