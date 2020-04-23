# from random import random
import random

from core.person import Person
from core.world import world
from core.constants import SEX
from policies.test import TestPolicy
from procedures.person.evaluate_site_infection import EvaluateSiteInfectionProcedure
from procedures.person.get_tested import GetTestedProcedure
from procedures.person.go_home import GoHomeProcedure
from procedures.person.go_work import GoWorkProcedure
from sites.base import GeoLocation
from sites.household import HouseholdSite
from sites.workplace import WorkplaceSite
from traits.person import PersonTraits
from traits.site import SiteTraits
from procedures.sites.meetings import MeetingProcedureSite
from utils.timeframe import TimeFrame


def random_location():
    return GeoLocation(random.random(), random.random())


# @TODO: World building should be based on coded scenarios or configuration?

def main():
    world.policies.append(TestPolicy())

    household = world.sites.append(
        HouseholdSite(
            random_location(),
            SiteTraits({ "area": random.randint(40,100) })))

    # can premake workplaces and then allocate people to them
    workplace1 = world.sites.append(
        WorkplaceSite(
            random_location(),
            SiteTraits({ "infection_factor": 1.5, "dispersion_factor": 1.0, "area": random.randint(100,600) }),
            [MeetingProcedureSite()]))

    workplace2 = world.sites.append(
        WorkplaceSite(
            random_location(),
            SiteTraits({ "infection_factor": 1.5, "dispersion_factor": 1.0, "area": random.randint(100,600) }),
            [MeetingProcedureSite()])) 

    # decisions happen in order, should order decisions per all people?
    world.people.append(Person(
        PersonTraits({ "sex": SEX.MALE, "age": 30 }),
        [
            GetTestedProcedure(),
            GoHomeProcedure(household, TimeFrame(1, 2)),
            GoWorkProcedure(workplace1, TimeFrame(1, 2)),
            EvaluateSiteInfectionProcedure()
        ]))
    world.people.append(Person(
        PersonTraits({ "sex": SEX.FEMALE, "age": 30 }),
        [GetTestedProcedure(), GoHomeProcedure(household, TimeFrame(1, 2)),
         GoWorkProcedure(workplace2, TimeFrame(1, 2)),
         EvaluateSiteInfectionProcedure()]
    ))

    world.tick()


if __name__ == '__main__':
    main()
