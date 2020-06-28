from abc import (
    ABC,
    abstractmethod,
)

class File(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def content_type(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def read(self, size):
        pass

    @abstractmethod
    def seek(self, offset):
        pass