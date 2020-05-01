import sys, types
from datetime import datetime, timedelta
from utils.timeframe import TimeFrame

class World:
    def __init__(self):
        self.reset()

    def reset (self):
        self.UUID = 0
        self.people = []
        self.sites = []
        self.policies = []
        self.plugins = []
        self.current = 0
        self.time_step = timedelta(minutes=5)
        self.current_tf = TimeFrame(datetime(2020, 3, 1, 18, 0), self.time_step)
        self.autoinc_entity_id = 0

    def run_scenario(self, scenario):
        # ugly
        if (scenario.time_step):
            self.time_step = scenario.time_step
        scenario.build()
        
        for policy in self.policies:
            policy.world_post_scenario_build()

        for plugin in self.plugins:
            plugin.world_post_scenario_build()

    def append_site(self, site):
        self.sites.append(site)

    def append_person(self, person):
        self.people.append(person)

    def append_policy(self, policy):
        self.policies.append(policy)

    def append_plugin(self, plugin):
        self.plugins.append(plugin)

    @property
    def time_step(self):
        return self.__time_step

    @time_step.setter
    def time_step(self, time_step):
        if hasattr(self, 'current_tf'):
            self.current_tf = TimeFrame(self.current_tf.start, self.current_tf.start + time_step)
        self.__time_step = time_step

    def tick(self):
        for policy in self.policies:
            policy.world_pretick()

        for plugin in self.plugins:
            plugin.world_pretick()

        for person in self.people:
            person.tick()

        for site in self.sites:
            site.tick()

        for policy in self.policies:
            policy.world_posttick()

        for plugin in self.plugins:
            plugin.world_posttick()

        self.current += 1
        self.current_tf = self.current_tf.next_tf(self.time_step)

    def finish (self):
        for policy in self.policies:
            policy.finish()

        for plugin in self.plugins:
            plugin.finish()

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




