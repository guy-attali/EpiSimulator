from policies.base import Policy, DecoratedPersonProcedure
from procedures.person.commute_procedure import CommuteProcedure
from core.world import world
from utils.time_utils import time_since, SECONDS_IN_WEEK

class DecoratedCommutingProcedure(DecoratedPersonProcedure):
    def __init__(self, procedure, policy: 'StayHomeIfHasSymptoms'):
        DecoratedPersonProcedure.__init__(self, procedure)
        self.policy = policy

    def should_apply(self, person):
        if (not self.policy.in_effect) or (person.site is not person.household) or \
            (person.symptoms_degree < 0.2):
            return self.decorated_procedure.should_apply(person)
        else:
            return False


class StayHomeIfHasSymptoms(Policy):
    def __init__(self):
        self.in_effect = False
        self.last_time_evaluated = None

    def decorate_site_procedure(self, procedure):
        return procedure

    def decorate_procedure(self, procedure):
        if procedure.is_type(CommuteProcedure):
            return DecoratedCommutingProcedure(procedure, self)
        return procedure

    def world_pretick(self):
        if (self.last_time_evaluated is None) or time_since(self.last_time_evaluated).total_seconds() > SECONDS_IN_WEEK:
            self.last_time_evaluated = world.current_time

            num_people_with_symptoms = sum(person.symptoms_degree>0.2 for person in world.people)

            self.in_effect = num_people_with_symptoms > 0.05 * len(world.people)