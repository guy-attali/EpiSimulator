# use an actual spatial map?
import math
from collections import namedtuple
from typing import Dict, List

from core.person import Person


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
    def __init__(self, location: GeoLocation):
        # TODO: Is this necessary?
        self.uuid = id(self)
        self.geolocation: GeoLocation = location
        self.people: Dict[Person, int] = {}
        self.log = []  # has a point?

    def enter(self, person: Person, enter_time: int):
        # TODO: Originally, this was clock.current_tick, but I assume we don't want clock to be global
        self.people[person] = enter_time

    def leave(self, person):
        if person not in self.people:
            raise Exception("This person {uuid} never entered the site".format(uuid=person.uuid))
        self.people.pop(person)

    def get_peoples(self) -> List[Person]:
        return list(self.people.keys())

    def distance_from(self, dest_site) -> float:
        return self.geolocation - dest_site


SiteLog = namedtuple('SiteLog', ['site', 'time'])
