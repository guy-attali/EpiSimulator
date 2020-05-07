# use an actual spatial map?
import math
from collections import namedtuple
from typing import Set, Optional

from core.world import world
from core.base_objects import ProceduresHolder
from core.person import Person
from core.traits import SiteTraits

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

    def __iter__(self):
        yield self.x
        yield self.y


class Site(ProceduresHolder):
    def __init__(self,
                 location: GeoLocation,
                 area: float,
                 site_traits: SiteTraits = None,
                 name: Optional[str]=None,
                 **kwargs):
        ProceduresHolder.__init__(self)

        # TODO: Is this necessary?
        self.uuid: int = id(self)
        if name is None:
            name = str(self.uuid)
        self.name = name
        self.geolocation: GeoLocation = location
        self.people: Set[Person] = set()
        self.traits: SiteTraits = site_traits or SiteTraits(**kwargs)
        # the "effective" area, in meters squared, of the site.
        self.area = area
        world.append_site(self)

    def enter(self, person: Person):
        self.people.add(person)

    def leave(self, person):
        if person not in self.people:
            raise Exception("This person {uuid} never entered the site".format(uuid=person.uuid))
        self.people.remove(person)

    def __contains__(self, person):
        return person.site is self

    def distance_from(self, dest_site) -> float:
        return self.geolocation - dest_site

    def __str__(self):
        return self.name

SiteLog = namedtuple('SiteLog', ['site', 'time'])
