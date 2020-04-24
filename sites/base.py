# use an actual spatial map?
import math
from typing import Dict, List

from core.person import Person
from core.world import world
from traits.base import RestrictTraits, SITE_TRAITS


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


class Site(RestrictTraits):
    def __init__(self, location: GeoLocation, initial_procedures=None, **kwargs):
        super().__init__(**kwargs)
        # TODO: Is this necessary?
        self.uuid = id(self)
        self.geolocation: GeoLocation = location
        self.people: Dict[Person, int] = {}
        self.log = []  # has a point?
        self.procedures = []
        initial_procedures = initial_procedures or []
        for procedure in initial_procedures:
            self.add_procedure(procedure)


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

    def tick(self):
        for procedure in self.procedures:
            if procedure.should_apply(self):
                procedure.apply(self)

    def _attribute_allowed(self, name):
        return name in SITE_TRAITS
