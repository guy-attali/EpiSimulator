import abc
from core.person import Person


class Procedure(abc.ABC):
    @property
    def name (self):
        return self.__class__.__name__

    @abc.abstractmethod
    def should_apply(self, person: Person) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, person: Person):
        pass
