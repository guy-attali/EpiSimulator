import abc

from procedures.base import SiteProcedure, PersonProcedure


class _DecoratedProcedure:
    def __init__(self, procedure):
        self.decorated_procedure = procedure

    def is_type(self, instance_type):
        return isinstance(self, instance_type) or \
               self.decorated_procedure.is_type(instance_type)


class DecoratedPersonProcedure(_DecoratedProcedure, PersonProcedure, abc.ABC):
    def should_apply(self, person) -> bool:
        return self.decorated_procedure.should_apply(person)

    def apply(self, person):
        return self.decorated_procedure.apply(person)


class DecoratedSiteProcedure(SiteProcedure, _DecoratedProcedure, abc.ABC):
    def should_apply(self, site) -> bool:
        return self.decorated_procedure.should_apply(site)

    def apply(self, site):
        return self.decorated_procedure.apply(site)


class Policy:

    def decorate_procedure(self, procedure):
        return procedure

    def world_pretick(self):
        pass

    def world_posttick(self):
        pass


__all__ = [DecoratedPersonProcedure, DecoratedSiteProcedure, Policy]
