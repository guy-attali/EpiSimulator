from datetime import datetime, timedelta
from typing import List


class World:
    def __init__(self):
        self.UUID = 0
        self.people = []
        self.sites = []
        self.policies = []
        self.current = 0
        self.current_ts = datetime(2020, 3, 1, 0, 0)
        self.time_step = timedelta(minutes=5)
        self.autoinc_entity_id = 0

    def appendPerson (self, person):
        self.people.append(person)

    def appendPolicy (self, policy):
        self.policies.append(policy)

    def appendSite (self, site):
        self.sites.append(site)

    def tick(self):
        for policy in self.policies:
            policy.world_pretick()

        for person in self.people:
            person.tick()

        for policy in self.policies:
            policy.world_posttick()
            
        self.current += 1
        self.current_ts = self.current_ts + self.time_step

    def next_entity_id(self):
        self.UUID += 1
        return self.UUID

    def get_future_tick(self, delta):
        return self.current + round(delta / self.time_step)

    def notify(self):
        # allow a notification mechanism to make visual simulation easier?
        pass


world = World()

__all__ = ['world']
