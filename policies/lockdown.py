from core.world import world
from policies.base import Policy, DecoratedPersonProcedure
from procedures.person.commute_procedure import CommuteProcedure
from utils.time_utils import time_since, SECONDS_IN_WEEK


class DecoratedCommutingProcedureLockdown(DecoratedPersonProcedure, CommuteProcedure):
    def __init__(self, procedure, policy: 'StayHomeIfHasSymptoms'):
        DecoratedPersonProcedure.__init__(self, procedure)
        self.policy = policy

    def should_apply(self, person):
        if (not self.policy.in_effect) or (person.site is not person.household):
            return self.decorated_procedure.should_apply(person)
        else:
            return False


class Lockdown(Policy):
    def __init__(self):
        self.in_effect = True
        self.last_time_evaluated = None

    def decorate_procedure(self, procedure):
        if procedure.is_type(CommuteProcedure):
            return DecoratedCommutingProcedureLockdown(procedure, self)
        return procedure

    def world_pretick(self):
        if (self.last_time_evaluated is None) or time_since(self.last_time_evaluated).total_seconds() > SECONDS_IN_WEEK:
            self.last_time_evaluated = world.current_time

            self.in_effect = not self.in_effect
