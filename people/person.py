from collections import namedtuple
from typing import List, Optional
from datetime import datetime

from core.base_objects import ObjectWithAcquiredTraits, ObjectWithProcedures
from core.world import world
from people.traits import Sex, Occupation
from sites import household

SiteLog = namedtuple('SiteLog', ['site', 'time'])

class Person(ObjectWithAcquiredTraits, ObjectWithProcedures):
    def __init__(
            self,
            age: float,
            sex: Sex,
            occupation: Occupation,
            susceptibility_degree: float,
            obedient_degree: float,
            is_infected: bool,
            symptoms_degree: float,
            immunity_degree: float,
            timestamp_arrived: datetime,
            timestamp_infected: Optional[datetime],
            timestamp_symptomatic: Optional[datetime],
            household: household
    ):
        ObjectWithAcquiredTraits.__init__(self)
        ObjectWithProcedures.__init__(self)

        self.uuid = world.next_entity_id()

        self.check_input_validity(is_infected, symptoms_degree, timestamp_infected, timestamp_symptomatic)

        self.age = age # age, in years
        self.sex = sex
        self.occupation = occupation

        self.susceptibility_degree = susceptibility_degree
        self.obedient_degree = obedient_degree

        self.is_infected = is_infected
        self.alive = True
        self.symptoms_degree = symptoms_degree
        self.immunity_degree = immunity_degree

        # time arrived at current site
        self.timestamp_arrived = timestamp_arrived

        # time since infection started and symptoms started
        self.timestamp_infected = timestamp_infected
        self.timestamp_symptomatic = timestamp_symptomatic

        # the houshold site where the person lives
        self.household = household

        self._commute_history = []
        self.current_site = household

    @staticmethod
    def check_input_validity(infected, symptoms_degree, timestamp_infected, timestamp_symptomatic):
        assert  ((not infected) and
                 (timestamp_infected is None) and
                 (timestamp_symptomatic is None) and
                 (symptoms_degree == 0)) \
                or (infected and
                    (timestamp_infected is not None) and
                    (timestamp_symptomatic is not None) and
                    (timestamp_symptomatic >= timestamp_infected ))

    @property
    def site(self):
        return self.current_site

    @site.setter
    def site(self, new_site):
        if new_site is not self.current_site:
            self._commute_history.append(SiteLog(self.current_site, world.current))
            self.current_site.leave(self)

        self.current_site = new_site
        new_site.enter(self)
        self.timestamp_arrived = world.current_tf.start

    def __hash__(self) -> int:
        return self.uuid
