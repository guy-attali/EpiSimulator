from traits.abstract import Trait, TRAITTYPE


class TraitInfected(Trait):
    c = TRAITTYPE.INFECTED

    def set_infected_time(self, ticks):
        self.infected_time = ticks
