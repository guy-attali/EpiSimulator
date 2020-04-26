from core.person import Person
from procedures.base import PersonProcedure


class GetTestedProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        # whatever conditions get somebody tested, use policy to mark a get tested trait?
        return False

    def apply(self, person: Person):
<<<<<<< HEAD
        person.is_infected = True
=======
        person.traits.infected = True
>>>>>>> master
