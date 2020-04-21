from typing import List

from core.person import Person
from policies.abstract import Policy
from core.world import world


class Procedure:
    def use(self, person: Person):
        self.__use(person)

    def apply(self, person):
        return self.__apply(person)

    def __use(self, person):
        return True

    def __apply(self, person):
        pass
