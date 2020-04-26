from core.person import Person
from procedures.base import PersonProcedure
<<<<<<< HEAD

class EvaluateSiteInfectionProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        return person.site is not None and person.is_infected

    def apply(self, person: Person):
        for person in person.site.people:
            if person.is_infected:
=======


class EvaluateSiteInfectionProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        return person.site is not None and person.traits.infected is True

    def apply(self, person: Person):
        for person in person.site.get_peoples():
            if person.traits.infected is True:
>>>>>>> master
                continue
