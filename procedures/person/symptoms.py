import random

import config
from core.person import Person
from core.procedure import PersonProcedure
from core.world import world
from utils.time_utils import time_since, SECONDS_IN_DAY


class SymptomsProcedure(PersonProcedure):
    def __init__(self):
        self.last_date_updated = None

    def should_apply(self, person: Person) -> bool:
        return True

    def apply(self, person: Person):
        dt = world.current_tf.duration.total_seconds() / SECONDS_IN_DAY # assuming dt is small
        if person.traits.is_infected:
            if person.traits.symptoms_degree == 0:
                # assuming dt is small
                if random.random() < dt / config.infected_days_to_symptoms:
                    person.traits.symptoms_degree = 1
                    person.traits.timestamp_symptomatic = world.current_time
            else:
                # assuming dt is small
                if random.random() < dt / config.infected_days_to_end_symptoms:
                    person.traits.symptoms_degree = 0
                    person.traits.timestamp_symptomatic = None

        else:
            if person.traits.symptoms_degree == 0:
                # assuming dt is small
                if random.random() < dt / config.susceptible_days_to_symptoms:
                    person.traits.symptoms_degree = 1
                    person.traits.timestamp_symptomatic = world.current_time
            else:
                # assuming dt is small
                if random.random() < dt / config.susceptible_days_to_end_symptoms:
                    person.traits.symptoms_degree = 0
                    person.traits.timestamp_symptomatic = None
