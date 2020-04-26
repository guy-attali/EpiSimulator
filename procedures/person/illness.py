import random
from math import exp

from core.person import Person
from core.world import world
from procedures.base import PersonProcedure
from utils.time_utils import time_since, SECONDS_IN_WEEK


class IllnessProcedure(PersonProcedure):
    def __init__(self):
        self.last_date_updated = None

    def should_apply(self, person: Person) -> bool:
        if not person.traits.is_infected:
            return False
        current_date = world.current_time.date()
        if self.last_date_updated != current_date:
            self.last_date_updated = current_date
            return True
        return False

    def apply(self, person: Person):
        if person.is_infected:
            time_infected = time_since(person.traits.timestamp_infected)
            if time_infected.total_seconds() > 2 * SECONDS_IN_WEEK:
                heal_probability = exp(-0.03 * person.traits.age - 1.28)
                if random.random() < heal_probability:
                    person.is_infected = False
                    person.symptoms_degree = 0.0
                    person.immunity_degree = 1.0
                    return
            if (person.symptoms_degree > 0) or time_infected.total_seconds() > 2 * SECONDS_IN_WEEK:
                person.symptoms_degree += random.uniform(0, person.traits.age / 400)
                person.symptoms_degree = min(person.symptoms_degree, 1.0)
                if person.timestamp_symptomatic is None:
                    person.timestamp_symptomatic = world.current_time
