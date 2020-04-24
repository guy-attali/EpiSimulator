# use an actual spatial map?
import math
from collections import namedtuple
from typing import Dict, List
from datetime import timedelta

from people.person import Person
from core.world import world
from core.base_objects import ObjectWithAcquiredTraits, ObjectWithProcedures


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


class Site(ObjectWithAcquiredTraits, ObjectWithProcedures):
    def __init__(
            self,
            location: GeoLocation,
            area: float,
            dispersion_factor: float,
            nominal_capacity:int
    ):
        ObjectWithAcquiredTraits.__init__(self)
        ObjectWithProcedures.__init__(self)

        # TODO: Is this necessary?
        self.uuid = id(self)
        self.geolocation: GeoLocation = location
        self.people: Dict[Person, int] = {}
        self.log = []  # has a point?


        # the "effective" area, in meters squared, of the site.
        self.area = area

        # the typical maximal number of people that the site can contain
        self.nominal_capacity = nominal_capacity

        # this value determines the tendency of people in the site to move around
        # (lower values mean that people are relatively static)
        self.dispersion_factor = dispersion_factor

    def enter(self, person: Person):
        # TODO: why start?
        self.people[person] = world.current_tf.start

    def leave(self, person):
        if person not in self.people:
            raise Exception("This person {uuid} never entered the site".format(uuid=person.uuid))
        self.people.pop(person)

    def get_peoples(self) -> List[Person]:
        return list(self.people.keys())

    def distance_from(self, dest_site) -> float:
        return self.geolocation - dest_site

    def meeting_probability(self, time_step:timedelta):
        """
        calculates the meeting probabilty in a 'Site' in a certain moment.
        multiplying the number of people in square meters with the dispersion factor.
        the meeting probability is in scale of 0 to 100.
        """
        num_people = len(self.people)
        if num_people  < 2:
            return 0.0
        else:
            m_p = (num_people*(time_step.total_seconds()/60)/self.area)*self.dispersion_factor
            return min(m_p, 1.0)




SiteLog = namedtuple('SiteLog', ['site', 'time'])
