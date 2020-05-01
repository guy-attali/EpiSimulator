import random

import config
from core.person import Person
from core.procedure import PersonProcedure
from core.world import world
from utils.time_utils import time_since


def heal_person(person: Person):
    person.traits.is_infected = False
    person.traits.symptoms_degree = 0.0
    person.traits.immunity_degree = 1.0


class IllnessProcedure(PersonProcedure):
    def __init__(self):
        self.last_date_updated = None

    def should_apply(self, person: Person) -> bool:
        return person.traits.is_infected

    def apply(self, person: Person):
        time_infected = time_since(person.traits.timestamp_infected)
        if time_infected.total_seconds() > 0:
            dt_days = world.current_tf.duration.total_seconds() / (60 * 60 * 24)
            heal_probability = dt_days / config.average_sick_duration_days
            if random.random() < heal_probability:
                heal_person(person)
        if person.traits.symptoms_degree > 0 or time_infected.total_seconds() > 0:
            person.traits.symptoms_degree += random.uniform(0, person.traits.age / 400)
            person.traits.symptoms_degree = min(person.traits.symptoms_degree, 1.0)
            if person.traits.timestamp_symptomatic is None:
                person.traits.timestamp_symptomatic = world.current_time
