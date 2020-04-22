from policies.base import Policy, DecoratedProcedure
from procedures.go_home import GoHomeProcedure


class DecoratedProcedureGoHome(DecoratedProcedure):
    def should_apply(self, person):
        return self.decorated_procedure.should_apply(person)

    def apply(self, person):
        return self.decorated_procedure.apply(person)


class TestPolicy(Policy):
    def decorate_procedure(self, procedure):
        if procedure.is_type(GoHomeProcedure):
            return DecoratedProcedureGoHome(procedure)
        return procedure

    def world_pretick(self):
        pass

    def world_posttick(self):
        pass
