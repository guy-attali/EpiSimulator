import random

import config
from core.procedure import SiteProcedure
from core.site import Site
from core.world import world
from utils.probs import prob_over_time


class InfectProcedure(SiteProcedure):
    def should_apply(self, site: Site) -> bool:
        return True

    def apply(self, site: Site):
        people = site.people
        number_of_people = len(people)
        if number_of_people == 0:
            return

        total_infectious_level = sum([person.traits.infectious_level for person in people])
        if total_infectious_level == 0:
            return
        infectious_level_density = total_infectious_level / site.area
        site_infecting_score = infectious_level_density * site.traits.dispersion_factor * config.disease_spreading_factor
        # for each person, calculate whether it got is_infected, or maybe even
        # healed
        for person in people:

            if person.traits.is_infected:
                continue

            # a probability for this specific person of getting is_infected
            person_infecting_score = site_infecting_score * (
                    1 - person.traits.immunity_degree) * person.traits.susceptibility_degree
            infecting_prob_per_hour = min(1, person_infecting_score)
            infecting_prob = prob_over_time(infecting_prob_per_hour, world.current_tf.duration.total_seconds() / 3600)
            # perform infection
            if random.random() < infecting_prob:
                person.traits.is_infected = True
                person.traits.timestamp_infected = world.current_time
