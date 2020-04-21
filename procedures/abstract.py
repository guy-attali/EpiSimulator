from typing import List

from core.person import Person
from policies.abstract import Policy


class Procedure:
    def use(self, person: Person, policies: List[Policy]):
        for policy in policies:
            if not policy.pre_procedure(self, person):
                return
        self.__use(person)

    def apply(self, person):
        return self.__apply(person)

    def __use(self, person):
        return True

    def __apply(self, person):
        pass
