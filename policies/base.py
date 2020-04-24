import abc

from procedures.base import SiteProcedure, PersonProcedure


class _DecoratedProcedure:
    def __init__(self, procedure):
        self.decorated_procedure = procedure

    def is_type(self, instance_type):
        return self.decorated_procedure.is_type(instance_type)


class DecoratedPersonProcedure(PersonProcedure, _DecoratedProcedure, abc.ABC):
    pass


class DecoratedSiteProcedure(SiteProcedure, _DecoratedProcedure, abc.ABC):
    pass


class Policy:

    def decorate_procedure(self, procedure):
        return procedure

    def world_pretick(self, timeframe):
        pass

    def world_posttick(self, timeframe):
        pass


__all__ = [DecoratedPersonProcedure, DecoratedSiteProcedure, Policy]
