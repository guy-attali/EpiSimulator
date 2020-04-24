# use an actual spatial map?
import math
from collections import namedtuple
from typing import Dict, List

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
            meeting_probability:float,
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

        # the probability of creating a meeting, depending on the area, number of people in the site
        # and the dispersion factor of the site
        # TODO: the right magnitude should be meeting probability per unit time
        self.meeting_probability = meeting_probability

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




SiteLog = namedtuple('SiteLog', ['site', 'time'])
