import abc
from core.person import Person


class Procedure(abc.ABC):
    @abc.abstractmethod
    def should_apply(self, person: Person) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, person: Person):
        pass
