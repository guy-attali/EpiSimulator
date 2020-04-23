from abc import abstractmethod

from procedures.base import SiteProcedure, PersonProcedure


class DecoratedPersonProcedure(PersonProcedure):
    def __init__(self, procedure: PersonProcedure):
        self.decorated_procedure: PersonProcedure = procedure

    @abstractmethod
    def should_apply(self, person):
        pass

    @abstractmethod
    def apply(self, person):
        pass

    def is_type(self, instance_type):
        return self.decorated_procedure.is_type(instance_type)


class DecoratedSiteProcedure(SiteProcedure):
    def __init__(self, procedure: SiteProcedure):
        self.decorated_procedure: SiteProcedure = procedure

    @abstractmethod
    def should_apply(self, site):
        pass

    @abstractmethod
    def apply(self, site):
        pass

    def is_type(self, instance_type):
        return self.decorated_procedure.is_type(instance_type)


class Policy:

    def decorate_procedure(self, procedure):
        return procedure

    def world_pretick(self):
        pass

    def world_posttick(self):
        pass
