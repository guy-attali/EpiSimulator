from core.person import Person
from procedures.base import PersonProcedure
from traits.person.infected import TraitInfected


class GetTestedProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        # whatever conditions get somebody tested, use policy to mark a get tested trait?
        return False

    def apply(self, person: Person):
        person.add_trait(TraitInfected(True))
