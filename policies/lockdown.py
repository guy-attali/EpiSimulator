import config
from core.person import Person
from core.policy import Policy, DecoratedPersonProcedure
from core.procedure import PersonProcedure
from core.world import world
from procedures.person.commute_procedure import CommuteProcedure
from utils.time_utils import time_since, SECONDS_IN_WEEK, SECONDS_IN_DAY
import random
from policies.lab_test import LabTest
from collections import Counter
from datetime import timedelta



class DecoratedCommutingProcedureLockdown(DecoratedPersonProcedure):
    def __init__(self, procedure: PersonProcedure, policy: 'Lockdown'):
        DecoratedPersonProcedure.__init__(self, procedure)
        self.policy = policy

    def should_apply(self, person):
        if (not self.policy.in_effect) or (person.site is not person.household):
            return self.decorated_procedure.should_apply(person)
        else:
            return False

    def apply(self, person: Person):
        self.decorated_procedure.apply(person)


class Lockdown(Policy):
    def __init__(self):
        self.lab_test = LabTest(config.test_sensitivity, config.test_specificity, config.time_to_test_results)
        self.in_effect = True
        self.last_time_evaluated = None
        self.movmean_infected = 0
        self.movmean_window = config.movmean_window
        self.infected_thresh = config.infected_thresh

    def decorate_procedure(self, procedure):
        if procedure.is_type(CommuteProcedure):
            return DecoratedCommutingProcedureLockdown(procedure, self)
        return procedure

    def world_pretick(self):
        for p in random.sample(world.people,
                               int(config.tests_per_day / (SECONDS_IN_DAY / world.current_tf.duration.total_seconds()))):
            self.lab_test.perform_test_on_person(p)

        test_results = self.lab_test.get_test_results()
        positive_counter = sum([t.result for t in test_results])
        r = world.current_tf.duration / self.movmean_window
        w = r / (r + 1)
        self.movmean_infected = w * positive_counter + (1 - w) * self.movmean_infected
        print(f'm = {self.movmean_infected}, l = {len(self.lab_test.test_results_log)}')
        if self.movmean_infected < self.infected_thresh:
            self.in_effect = False
        else:
            self.in_effect = True
        #  if (self.last_time_evaluated is None) or time_since(self.last_time_evaluated).total_seconds() > SECONDS_IN_WEEK:
        #     self.last_time_evaluated = world.current_time
        #
        #     self.in_effect = not self.in_effect

    def world_posttick(self):
        pass

    def world_post_scenario_build(self):
        pass

    def finish(self):
        pass

