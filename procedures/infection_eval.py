from procedures.abstract import Procedure
from traits.abstract import TRAITTYPE


class EvaluateSiteInfectionProcedure(Procedure):
    def __use(self, person):
        return person.current_site is not None and person.traits[TRAITTYPE.INFECTED] is True

    def __apply(self, person):
        for person in person.current_site.getPeople():
            if person.traits[TRAITTYPE.INFECTED] is True:
                continue
