from random import random

from core.person import Person
from core.world import world
from policies.test import TestPolicy
from procedures.evaluate_site_infection import EvaluateSiteInfectionProcedure
from procedures.get_tested import GetTestedProcedure
from procedures.go_home import GoHomeProcedure
from procedures.go_work import GoWorkProcedure
from sites.base import GeoLocation
from sites.household import HouseholdSite
from sites.workplace import WorkplaceSite
from traits.age import TraitAge
from traits.sex import TraitSex, SEX
from site_traits.infetion_factor import SiteTraitInfectionFactor
from utils.timeframe import TimeFrame


def random_location():
    return GeoLocation(random(), random())


# @TODO: World building should be based on coded scenarios or configuration?

def main():
    world.policies.append(TestPolicy())

    household = world.sites.append(HouseholdSite(random_location()))
    # can premake workplaces and then allocate people to them
    workplace1 = world.sites.append(WorkplaceSite(random_location()), [SiteTraitInfectionFactor(1.5)])
    workplace2 = world.sites.append(WorkplaceSite(random_location()), [SiteTraitInfectionFactor(1.2)])

    # decisions happen in order, should order decisions per all people?
    world.people.append(Person(
        [TraitSex(SEX.MALE), TraitAge(30)],
        [GetTestedProcedure(), GoHomeProcedure(household, TimeFrame(1, 2)),
         GoWorkProcedure(workplace1, TimeFrame(1, 2)),
         EvaluateSiteInfectionProcedure()]
    ))
    world.people.append(Person(
        [TraitSex(SEX.FEMALE), TraitAge(30)],
        [GetTestedProcedure(), GoHomeProcedure(household, TimeFrame(1, 2)),
         GoWorkProcedure(workplace2, TimeFrame(1, 2)),
         EvaluateSiteInfectionProcedure()]
    ))

    world.tick()


if __name__ == '__main__':
    main()
