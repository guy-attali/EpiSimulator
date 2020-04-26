from datetime import datetime, timedelta

from utils.timeframe import TimeFrame


class World:
    def __init__(self):
        self.UUID = 0
        self.people = []
        self.sites = []
        self.policies = []
        self.current = 0
        self.time_step = timedelta(minutes=5)
        self.current_tf = TimeFrame(datetime(2020, 3, 1, 18, 0), self.time_step)
        self.autoinc_entity_id = 0

    def append_site(self, site):
        self.sites.append(site)

    def append_person(self, person):
        self.people.append(person)

    def append_policy(self, policy):
        self.policies.append(policy)

    def tick(self):
        for policy in self.policies:
            policy.world_pretick()

        for person in self.people:
            person.tick()

        for site in self.sites:
            site.tick()

        for policy in self.policies:
            policy.world_posttick()

        self.current += 1
        self.current_tf = self.current_tf + self.time_step

    def next_entity_id(self):
        self.UUID += 1
        return self.UUID

    @property
    def current_time(self):
        """
        return the time of the beginning of current timeframe
        """
        return self.current_tf.start

    def get_future_tick(self, delta):
        return self.current + round(delta / self.time_step)

    def notify(self):
        # allow a notification mechanism to make visual simulation easier?
        pass


world = World()

__all__ = ['world']
