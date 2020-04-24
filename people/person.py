from collections import namedtuple
from typing import List, Optional
from datetime import datetime

from core.base_objects import ObjectWithAcquiredTraits
from core.world import world
from people.traits import Sex, Occupation
from sites import household

SiteLog = namedtuple('SiteLog', ['site', 'time'])

class Person(ObjectWithAcquiredTraits):
    def __init__(
            self,
            age: float,
            sex: Sex,
            occupation: Occupation,
            susceptibility_degree: float,
            obedient_degree: float,
            infected: bool,
            symptoms_degree: float,
            immunity_degree: float,
            timestamp_arrived: datetime,
            timestamp_infected: Optional[datetime],
            timestamp_symptomatic: Optional[datetime],
            household: household
    ):
        ObjectWithAcquiredTraits.__init__(self)

        self.uuid = world.next_entity_id()

        self.check_input_validity(infected, symptoms_degree, timestamp_infected, timestamp_symptomatic)

        self.age = age # age, in years
        self.sex = sex
        self.occupation = occupation
        self.infected = infected

        # magnitudes of various variables that characterize aspects of the illness.
        self.susceptibility_degree = susceptibility_degree
        self.obedient_degree = obedient_degree
        self.symptoms_degree = symptoms_degree
        self.immunity_degree = immunity_degree

        # time arrived at current site
        self.timestamp_arrived = timestamp_arrived

        # time since infection started and symptoms started
        self.timestamp_infected = timestamp_infected
        self.timestamp_symptomatic = timestamp_symptomatic

        # the houshold site where the person lives
        self.household = household

        self.procedures = []
        self._commute_history = []
        self._current_site = household

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

    def add_procedure(self, procedure, index=None):
        index = index or len(self.procedures)

        for policy in world.policies:
            procedure = policy.decorate_procedure(procedure)

        self.procedures.insert(index, procedure)

    @property
    def site(self):
        return self._current_site

    def move(self, other_site):
        if self._current_site is not None:
            self._commute_history.append(SiteLog(self._current_site, world.current))
            self._current_site.leave(self)

        self._current_site = other_site
        self._current_site.enter(self)

    def tick(self, timestamp):
        for procedure in self.procedures:
            if procedure.should_apply(self):
                procedure.apply(self)

    def __hash__(self) -> int:
        return self.uuid
