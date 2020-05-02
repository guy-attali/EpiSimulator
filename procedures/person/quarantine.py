from core.person import Person
from core.procedure import PersonProcedure


class HomeQuarantineProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        pass

    def apply(self, person: Person):
        pass


class HospitalQuarantineProcedure(PersonProcedure):
    def should_apply(self, person: Person) -> bool:
        pass

    def apply(self, person: Person):
        pass
