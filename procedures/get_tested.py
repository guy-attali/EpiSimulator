from core.person import Person
from procedures.abstract import Procedure
from traits.infected import TraitInfected


class GetTestedProcedure(Procedure):
    def __use(self, person: Person):
        # whatever conditions get somebody tested, use policy to mark a get tested trait?
        return False

    def __apply(self, person: Person):
        person.add_trait(TraitInfected(True))
