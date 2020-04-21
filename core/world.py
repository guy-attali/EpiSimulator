from datetime import datetime, timedelta
from typing import List

from core.person import Person
from policies.abstract import Policy
from sites.abstract import Site


class World:
    def __init__(self):
        self.people: List[Person] = []
        self.sites: List[Site] = []
        self.policies: List[Policy] = []
        self.current = 0
        self.current_ts = datetime(2020, 3, 1, 0, 0)
        self.time_step = timedelta(minutes=5)
        self.autoinc_entity_id = 0

    def tick(self):
        for person in self.people:
            person.tick()
        self.current += 1
        self.current_ts = self.current_ts + self.time_step

    def entity_id(self):
        self.autoinc_entity_id += 1
        return self.autoinc_entity_id

    def get_future_tick(self, delta):
        return self.current + round(delta / self.time_step)

    def notify(self):
        # allow a notification mechanism to make visual simulation easier?
        pass


world = World()