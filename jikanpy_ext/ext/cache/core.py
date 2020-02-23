
from abc import ABCMeta, abstractmethod

class Strategy(metaclass=ABCMeta):

    @abstractmethod
    def key_exists(self, key):
        pass

    @abstractmethod
    def delete_key(self, key):
        pass


    @abstractmethod
    def get_data(self, key):
        pass

    @abstractmethod
    def update_data(self, key, value):
        pass


class Memory(Strategy):

    def __init__(self):
        pass


class File(Strategy):
    pass
