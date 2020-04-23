from core.person import Person
from procedures.base import PersonProcedure
from traits.base import PERSON_TRAIT_TYPE


class EvaluateSiteInfectionProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        return person.site is not None and person.traits[PERSON_TRAIT_TYPE.INFECTED] is True

    def apply(self, person: Person):
        for person in person.site.get_peoples():
            if person.traits[PERSON_TRAIT_TYPE.INFECTED] is True:
                continue
