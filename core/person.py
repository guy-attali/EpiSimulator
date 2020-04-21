from enum import Enum
from typing import List, Dict

from procedures.abstract import Procedure
from sites.abstract import Site, SiteLog
from traits.abstract import Trait, TRAITTYPE


class Person:
    UUID = 0

    def __init__(self, initial_traits: List = None, default_procedures: List = None):
        self.uuid = Person.UUID
        Person.UUID += 1

        self.traits: Dict[TRAITTYPE, Trait] = {}
        self.procedures: List[Procedure] = []
        self._commute_history: List[SiteLog] = []
        self._current_site = None
        self.current_tick = 1

        for trait in initial_traits:
            self.add_trait(trait)

        for decision in default_procedures:
            self.add_procedure(decision)

    def add_trait(self, trait):
        self.traits[trait.c] = trait

    def add_procedure(self, decision, index=None):
        index = index or len(self.procedures)
        self.procedures.insert(index, decision)

    @property
    def site(self) -> Site:
        return self._current_site

    @site.setter
    def site(self, other_site):
        if self._current_site is not None:
            self._commute_history.append(SiteLog(self._current_site, self.current_tick))
            self._current_site.leave(self)

        self._current_site = other_site
        self._current_site.enter(self)

    def tick(self):
        for decision in self.procedures:
            # TODO: Where should it get policies from?
            if not decision.use(self):
                continue
            decision.apply(self)
        self.current_tick += 1

    def __hash__(self) -> int:
        return self.uuid
