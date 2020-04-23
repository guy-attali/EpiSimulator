# use an actual spatial map?
import math
from collections import namedtuple
from typing import Dict, List
import random

from core.person import Person
from core.world import world
from core.meetings import Meeting
from traits.base import Trait, SITE_TRAIT_TYPE


class GeoLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other) -> float:
        """
        Calculates air distance
        """
        x_distance = other.x - self.x
        y_distance = other.y - self.y
        return math.sqrt(x_distance ** 2 + y_distance ** 2)


class Site:
    def __init__(self, location: GeoLocation, initial_traits=None, initial_procedures=None, area: int = None,
                 dispersion_factor: float = 1.0):
        # TODO: Is this necessary?
        self.uuid = id(self)
        self.geolocation: GeoLocation = location
        self.people: Dict[Person, int] = {}
        self.log = []  # has a point?
        self.traits: Dict[SITE_TRAIT_TYPE, Trait] = {}
        self.procedures = []
        self._area = area
        self._dispersion_factor = dispersion_factor

        initial_traits = initial_traits or []
        for trait in initial_traits:
            self.add_trait(trait)

        initial_procedures = initial_procedures or []
        for procedure in initial_procedures:
            self.add_procedure(procedure)

    def add_trait(self, trait):
        self.traits[trait.c] = trait

    def add_procedure(self, procedure, index=None):
        index = index or len(self.procedures)

        for policy in world.policies:
            procedure = policy.decorate_site_procedure(procedure)

        self.procedures.insert(index, procedure)

    def enter(self, person: Person):
        self.people[person] = world.current_ts

    def leave(self, person):
        if person not in self.people:
            raise Exception("This person {uuid} never entered the site".format(uuid=person.uuid))
        self.people.pop(person)

    def get_peoples(self) -> List[Person]:
        return list(self.people.keys())

    def distance_from(self, dest_site) -> float:
        return self.geolocation - dest_site

    def calculate_meeting_probability(self, time_step):
        """
        calculates the meeting probabilty in a 'Site' in a certain moment.
        multiplying the number of people in square meters with the dispersion factor.
        the meeting probability is in scale of 0 to 1.
        :param time_step - the time intervals
        """
        if len(self.people) < 2:
            return 0
        else:
            m_p = (len(self.people)*time_step/self._area)*self._dispersion_factor
            return m_p if m_p < 1 else 1

    def create_meetings(self):
        """
        checks for meetings randomly using the meeting probability.
        if the randomized number is in the range of the meeting probability a 'Meeting' object is created.
        :return list of meetings that occured in the 'Site'.
                if no meetings were created returns an empty list.
        """
        meetings = []
        meeting_probability = self.calculate_meeting_probability(time_step=world.time_step)
        if meeting_probability > 0:
            for i in range(len(self.people)):
                if random.uniform(0, 1) <= meeting_probability:
                    person1 = self.get_peoples()[i]
                    person2 = random.choice([person for person in self.get_peoples() if person != person1])
                    meeting = Meeting(person1=person1, person2=person2, site=self)
                    meetings.append(meeting)
        return meetings

    def tick(self):
        meetings = self.create_meetings()



SiteLog = namedtuple('SiteLog', ['site', 'time'])
