from core.person import Person
from procedures.base import Procedure
from traits.base import TRAITTYPE


class EvaluateSiteInfectionProcedure(Procedure):
    def should_apply(self, person: Person) -> bool:
        return person.site is not None and person.traits[TRAITTYPE.INFECTED] is True

    def apply(self, person: Person):
        for person in person.site.get_peoples():
            if person.traits[TRAITTYPE.INFECTED] is True:
                continue
