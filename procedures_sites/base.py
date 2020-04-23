import abc

from sites.base import Site


class SiteProcedure(abc.ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def should_apply(self, site: Site) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, site: Site):
        pass

    def is_type(self, instance_type):
        return type(self) == instance_type
