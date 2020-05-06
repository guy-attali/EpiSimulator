import abc

from core.procedure import SiteProcedure, PersonProcedure


class _DecoratedProcedure:
    def __init__(self, procedure):
        self.decorated_procedure = procedure

    def is_type(self, instance_type):
        return self.decorated_procedure.is_type(instance_type)


class DecoratedPersonProcedure(PersonProcedure, _DecoratedProcedure, abc.ABC):
    def __init__(self, procedure: PersonProcedure):
        _DecoratedProcedure.__init__(self, procedure)


class DecoratedSiteProcedure(SiteProcedure, _DecoratedProcedure, abc.ABC):
    def __init__(self, procedure: SiteProcedure):
        _DecoratedProcedure.__init__(self, procedure)



class Policy(abc.ABC):
    @abc.abstractmethod
    def decorate_procedure(self, procedure):
        pass

    @abc.abstractmethod
    def world_pretick(self):
        pass

    @abc.abstractmethod
    def world_posttick(self):
        pass

    @abc.abstractmethod
    def world_post_scenario_build(self):
        pass

    @abc.abstractmethod
    def finish(self):
        pass


__all__ = [DecoratedPersonProcedure, DecoratedSiteProcedure, Policy]
