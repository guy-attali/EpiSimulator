from collections import namedtuple

from core.base_objects import ProceduresHolder
from core.traits import PersonTraits
from core.world import world

SiteLog = namedtuple('SiteLog', ['site', 'time'])


class Person(ProceduresHolder):
    def __init__(
            self,
            household,
            person_traits: PersonTraits = None,
            **kwargs):
        ProceduresHolder.__init__(self)
        self.uuid = world.next_entity_id()
        self.traits = person_traits or PersonTraits(**kwargs)

        self.alive = True

        # the houshold site where the person lives
        self.household = household

        self._commute_history = []
        self._current_site = None
        self.timestamp_arrived = None

        self.site = household

    @property
    def site(self):
        return self._current_site

    @site.setter
    def site(self, new_site):
        if new_site is not self._current_site:
            self._commute_history.append(SiteLog(self._current_site, world.current))
            if self._current_site is not None:
                self._current_site.leave(self)

        self._current_site = new_site
        new_site.enter(self)
        self.timestamp_arrived = world.current_time

    def __hash__(self) -> int:
        return self.uuid
