from core.person import Person
from procedures.abstract import Procedure


class Policy:
    def pre_procedure(self, procedure: Procedure, person: Person) -> bool:
        """
        Method that will run before any procedure.
        :return: If returns True, the procedure will be called. Otherwise, it won't
        """
        raise NotImplementedError

    def post_procedure(self, procedure):
        raise NotImplementedError


class TestPolicyDecoratedProcedure():
    def __init__ (self, procedure):
        self.procedure = procedure
    
    __use (self)
        pass
    
    __apply (self)
        pass

class TestPolicy(Policy):
    def pre_procedure(self, procedure: Procedure, person: Person) -> bool:
        return True
    def post_procedure(self, procedure):
        return True

    def decorateProcedure(procedure):
        if procedure.c is not PROCEDURE.GOHOME:
            return procedure
        return TestPolicyDecoratedProcedure(procedure)