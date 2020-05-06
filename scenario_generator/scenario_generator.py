from random import random, choice, choices, normalvariate
from datetime import time

from core.person import Person
from core.world import world
from policies.test import TestPolicy
from procedures.person.evaluate_site_infection import EvaluateSiteInfectionProcedure
from procedures.person.get_tested import GetTestedProcedure
from procedures.person.go_home import GoHomeProcedure
from procedures.person.go_work import GoWorkProcedure
from sites.base import GeoLocation
from sites.household import HouseholdSite
from sites.workplace import WorkplaceSite
from traits.person.age import TraitAge
from traits.person.sex import TraitSex, SEX
from traits.sites.interaction_factor import SiteTraitInfectionFactor
from procedures.sites.test import TestProcedureSite
from utils.timeframe import TimeFrame
import numpy as np

def random_location():
    return GeoLocation(random(), random())


def gen_random_person(home=None, work=None, mean_age=30, std_age=0,
                      start_work_time=time(9), end_work_time=time(17), sex=None):
    if sex is None:
        sex = TraitSex(choice([SEX.MALE, SEX.FEMALE]))
    age = TraitAge(max(0, normalvariate(mean_age, std_age)))
    procedures = [GetTestedProcedure(), EvaluateSiteInfectionProcedure()]
    if home is not None:
        procedures.append(
            GoHomeProcedure(home, TimeFrame(end_work_time, start_work_time))
        )
    if work is not None:
        procedures.append(
            GoWorkProcedure(work, TimeFrame(start_work_time, end_work_time))
        )
    return Person([sex, age], procedures)


def gen_random_home(n_people=None):
    # todo: take into account n_people_in_household in calculating the area
    return HouseholdSite(random_location())


def gen_random_work(n_people=None):
    # todo: take into account n_people in calculating the area
    return HouseholdSite(random_location())


def gen_random_household(work_places, work_prob, school, household_size_dist):
    people = []
    n_people_in_household = choices(*household_size_dist)[0]
    n_adults = 2
    n_children = max(n_people_in_household - n_adults, 0)
    home = gen_random_home(n_people_in_household)
    for _ in range(n_adults):
        work = choices(work_places, work_prob)[0]
        people.append(gen_random_person(home=home, work=work, mean_age=45, std_age=20))
    for _ in range(n_children):
        people.append(gen_random_person(home=home, work=school, mean_age=10, std_age=5))
    return people


def main():
    n_people = 1000
    average_work_place_workers = 10
    household_size_dist = ([1, 2, 3, 4, 5], [0.1, 0.2, 0.2, 0.4, 0.1])

    average_household_people = round(np.average(household_size_dist[0], weights=household_size_dist[1]))
    n_household_sites = round(n_people / average_work_place_workers)
    n_work_sites = round(n_people / average_work_place_workers)
    work_places = []
    for _ in range(n_work_sites):
        work_places.append(gen_random_work())
    school = gen_random_work()
    work_prob = np.ones(n_work_sites) / n_work_sites
    people = []
    for _ in range(int(n_people / average_household_people)):
        people.extend(gen_random_household(work_places, work_prob, school, household_size_dist))

    sites = work_places + [school]
    world.people = people
    world.sites = sites
    return world


if __name__ == '__main__':
    main()



