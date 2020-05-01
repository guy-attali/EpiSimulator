from core.policy import Policy, DecoratedPersonProcedure
from procedures.person.go_home import GoHomeProcedure


class DecoratedProcedureGoHome(DecoratedPersonProcedure):
    def should_apply(self, person):
        return self.decorated_procedure.should_apply(person)


class TestPolicy(Policy):
    def decorate_procedure(self, procedure):
        if procedure.is_type(GoHomeProcedure):
            return DecoratedProcedureGoHome(procedure)
        return procedure

    def world_pretick(self):
        pass

    def world_posttick(self):
        pass
