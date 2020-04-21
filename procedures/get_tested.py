from core.person import Person
from procedures.abstract import Procedure
from traits.infected import TraitInfected


class GetTestedProcedure(Procedure):
    def should_apply(self, person: Person) -> bool:
        # whatever conditions get somebody tested, use policy to mark a get tested trait?
        return False

    def apply(self, person: Person):
        person.add_trait(TraitInfected(True))
