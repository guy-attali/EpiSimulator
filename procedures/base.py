import abc

from people.person import Person
from sites.base import Site


class _Procedure(abc.ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def should_apply(self, obj: object) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, obj: object):
        pass

    def is_type(self, instance_type):
        return type(self) is instance_type


class PersonProcedure(_Procedure):
    @abc.abstractmethod
    def should_apply(self, person: Person) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, person: Person):
        pass


class SiteProcedure(_Procedure):
    @abc.abstractmethod
    def should_apply(self, site: Site) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, site: Site):
        pass


__all__ = [SiteProcedure, PersonProcedure]
