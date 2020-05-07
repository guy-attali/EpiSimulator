import config
from core.world import world
import random
from collections import namedtuple

PersonResult = namedtuple('PersonResult', ['time', 'person', 'result'])


class LabTest:
    def __init__(self, test_sensitivity, test_specificity, time_to_test_results):
        self.test_sensitivity = test_sensitivity
        self.test_specificity = test_specificity
        self.time_to_test_results = time_to_test_results
        self.test_results_log = []

    def perform_test_on_person(self, person):
        if person.traits.is_infected:
            if random.random() < self.test_sensitivity:
                result = True
            else:
                result = False
        else:
            if random.random() < self.test_specificity:
                result = False
            else:
                result = True
        self.test_results_log.append(PersonResult(time=world.current_time, person=person, result=result))

    def get_test_results(self):
        i = 0
        while world.current_time - self.test_results_log[i].time > self.time_to_test_results:
            i += 1
            if i == len(self.test_results_log):
                break

        delivered_results = self.test_results_log[:i]
        self.test_results_log = self.test_results_log[i:]
        return delivered_results

