from people.person import Person
from procedures.base import PersonProcedure

class EvaluateSiteInfectionProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        return person.site is not None and person.infected

    def apply(self, person: Person):
        for person in person.site.get_peoples():
            if person.infected is True:
                continue
