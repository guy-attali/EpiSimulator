from collections import namedtuple
from typing import List

from core.world import world
from traits.base import RestrictTraits, PERSON_TRAITS

SiteLog = namedtuple('SiteLog', ['site', 'time'])


class Person(RestrictTraits):
    def __init__(self, initial_procedures: List = None, **kwargs):
        super().__init__(**kwargs)
        self.uuid = world.next_entity_id()

        self.procedures = []
        self._commute_history = []
        self._current_site = None

        for procedure in initial_procedures:
            self.add_procedure(procedure)

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

    def tick(self):
        for procedure in self.procedures:
            if procedure.should_apply(self):
                procedure.apply(self)

    def __hash__(self) -> int:
        return self.uuid

    def _attribute_allowed(self, name):
        return name in PERSON_TRAITS
