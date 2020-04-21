from typing import List, Dict
from core.world import world

from procedures.abstract import Procedure
from sites.base import Site, SiteLog
from traits.base import Trait, TRAITTYPE


class Person:
    UUID = 0

    def __init__(self, initial_traits: List = None, default_procedures: List = None):
        self.uuid = Person.UUID
        Person.UUID += 1

        self.traits: Dict[TRAITTYPE, Trait] = {}
        self.procedures: List[Procedure] = []
        self._commute_history: List[SiteLog] = []
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
            if not hasattr(policy, 'decorateProcedure'):
                continue
            procedure = policy.decorateProcedure(procedure)

        self.procedures.insert(index, procedure)

    @property
    def site(self) -> Site:
        return self._current_site

    @site.setter
    def site(self, other_site):
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
