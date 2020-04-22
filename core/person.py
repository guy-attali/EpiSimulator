from typing import List, Dict
from core.world import world


class Person:
    def __init__(self, initial_traits: List = None, default_procedures: List = None):
        self.uuid = world.next_entity_id()

        self.traits = {}
        self.procedures = []
        self._commute_history = []
        self._current_site = None

        for trait in initial_traits:
            self.add_trait(trait)

        for decision in default_procedures:
            self.add_procedure(decision)

    def add_trait(self, trait):
        self.traits[trait.c] = trait

    def add_procedure(self, procedure, index=None):
        index = index or len(self.procedures)

        for policy in world.policies:
            procedure = policy.decorate_procedure(procedure)

        self.procedures.insert(index, procedure)

    @property
    def site (self):
        return self._current_site

    def move (self, site):
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
