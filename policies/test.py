from policies.base import Policy, DecoratedProcedure


class DecoratedProcedureGoHome(DecoratedProcedure):
    def should_apply(self, person):
        return self.decorated_procedure.should_apply(person)

    def apply(self, person):
        return self.decorated_procedure.apply(person)


class TestPolicy(Policy):
    def decorate_procedure(self, procedure):
        # @TODO this would prevent multiple wrapping as it'll change the class name from the POV of further policies, need to use static naming
        if (procedure.name != "GoHomeProcedure"):
            return procedure

        return DecoratedProcedureGoHome(procedure)

    def world_pretick(self):
        pass

    def world_posttick(self):
        pass
