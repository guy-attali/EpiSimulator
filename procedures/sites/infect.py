import random

from core.site import Site
from core.world import world
from procedures.base import SiteProcedure



disease_spreading_factor = 1


class InfectProcedure(SiteProcedure):
    def should_apply(self, site: Site) -> bool:
        return True

    def apply(self, site: Site):
        people = site.people
        number_of_people = len(people)
        if number_of_people == 0:
            return

        number_of_ill_people = sum([person.traits.is_infected for person in people])
        ratio_of_ill_people = number_of_ill_people / number_of_people
        density = number_of_people / site.area
        ratio_of_capacity = number_of_people / site.traits.nominal_capacity

        # from these variables, get a "score" for the site, where a high score
        # means higher chance if infection
        site_infecting_score = (world.current_tf.duration.total_seconds()/60) \
                               * ratio_of_ill_people \
                               * density \
                               * site.traits.dispersion_factor \
                               * disease_spreading_factor
        # for each person, calculate whether it got is_infected, or maybe even
        # healed
        for person in people:

            if person.traits.is_infected:
                continue

            # a probability for this specific person of getting is_infected
            person_infecting_score = site_infecting_score * (
                    1 - person.traits.immunity_degree) * person.traits.susceptibility_degree

            # perform infection
            if random.random() < person_infecting_score:
                person.traits.is_infected = True
                person.traits.timestamp_infected = world.current_time
