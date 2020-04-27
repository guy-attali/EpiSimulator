import random
from math import exp

from core.person import Person
from core.world import world
from procedures.base import PersonProcedure
from utils.time_utils import time_since, SECONDS_IN_WEEK
from config import params_dict


class IllnessProcedure(PersonProcedure):
    def __init__(self):
        self.last_date_updated = None

    def should_apply(self, person: Person) -> bool:
        if not person.traits.is_infected:
            return False
        return True

    def apply(self, person: Person):
        if person.traits.is_infected:
            time_infected = time_since(person.traits.timestamp_infected)
            if time_infected.total_seconds() > 0*SECONDS_IN_WEEK:
                dt_days = world.current_tf.duration.total_seconds() / (60*60*24)
                heal_probability = dt_days / (params_dict['average_sick_duration_days'])
                if random.random() < heal_probability:
                    person.traits.is_infected = False
                    person.traits.symptoms_degree = 0.0
                    person.traits.immunity_degree = 1.0
                    return
            if (person.traits.symptoms_degree > 0) or time_infected.total_seconds() > 0 * SECONDS_IN_WEEK:
                person.traits.symptoms_degree += random.uniform(0, person.traits.age / 400)
                person.traits.symptoms_degree = min(person.traits.symptoms_degree, 1.0)
                if person.traits.timestamp_symptomatic is None:
                    person.traits.timestamp_symptomatic = world.current_time
