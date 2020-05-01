from core.person import Person
from core.procedure import PersonProcedure


class EvaluateSiteInfectionProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        return person.site is not None and person.traits.is_infected is True

    def apply(self, person: Person):
        for person in person.site.get_peoples():
            if person.traits.infected is True:
                continue
