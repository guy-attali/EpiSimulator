from traits.base import Trait, PERSON_TRAIT_TYPE


class TraitInfected(Trait):
    c = PERSON_TRAIT_TYPE.INFECTED

    def set_infected_time(self, ticks):
        self.infected_time = ticks
