import abc
from typing import Dict, List

from core.person import Person
from procedures.abstract import Procedure


class PolicyEnforcementMeta(type):
    """
    Metaclass for policy enforcement rules. Mostly for type annotation
    """
    pass


class PolicyEnforcement(Procedure, metaclass=PolicyEnforcementMeta):
    """
    Represents a specific policy enforcement. This class will alter the procedure, fitting the policy desires
    """

    def __init__(self, procedure):
        self.procedure = procedure

    @abc.abstractmethod
    def pre_should_apply(self, person: Person) -> bool:
        """
        A function that will happen before original should_apply function. If you have no interest in this, simply return True
        :return: True if should continue, False otherwise
        """
        pass

    @abc.abstractmethod
    def post_should_apply(self, person: Person, original_result: bool):
        """
        A function that will happen after original should_apply function. If you have no interest in this, return original_result
        :param original_result: The return value from the original should_apply function
        """
        pass

    def should_apply(self, person: Person) -> bool:
        if not self.pre_should_apply(person):
            return False
        result = self.procedure.should_apply(person)
        return self.post_should_apply(person, result)

    @abc.abstractmethod
    def pre_apply(self, person: Person):
        """
        A function that will be called before original apply function.
        """
        pass

    @abc.abstractmethod
    def post_apply(self, person: Person, original_result=None):
        """
        A function that will be called before original apply function. If you have no interest in this, return original_result
        """
        pass

    def apply(self, person: Person):
        self.pre_should_apply(person)
        result = self.procedure.apply(person)
        return self.post_apply(person, result)


class Policy(abc.ABC):
    """
    A class to implement a policy. This class gets a dict mapping a procedure and a list of PolicyEnforcements *classes* to run on it.
    You may also pass a default list that would apply on all procedures
    Pay attention that the list is of classes, and not objects
    For example:
    policy = Policy({GoHomeProcedure: [PolicyEnforcementType1, PolicyEnforcementType2]})

    """

    def __init__(self, enforcements: Dict[Procedure, List[PolicyEnforcementMeta]], default: List[PolicyEnforcementMeta]):
        self.enforcements = enforcements
        self.default = default

    def decorate_procedure(self, procedure: Procedure):
        enforcements = set()
        if procedure in self.enforcements:
            for enforcement in self.enforcements[procedure]:
                enforcements.add(enforcement)
        enforcements.update(self.default)

        policy_procedure = procedure
        for enforcement in enforcements:
            policy_procedure = enforcement(policy_procedure)
        return policy_procedure
