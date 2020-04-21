from random import random

from core.person import Person
from core.world import world
from policies.abstract import TestPolicy
from procedures.get_tested import GetTestedProcedure
from procedures.go_home import GoHomeProcedure
from procedures.go_work import GoWorkProcedure
from sites.abstract import GeoLocation
from sites.household import HouseholdSite
from sites.workplace import WorkplaceSite
from traits.age import TraitAge
from traits.sex import TraitSex, SEX
from utils.timeframe import TimeFrame


def random_location():
    return GeoLocation(random(), random())


def main():
    world.policies.append(TestPolicy())

    household = world.sites.append(HouseholdSite(random_location()))
    # can premake workplaces and then allocate people to them
    workplace1 = world.sites.append(WorkplaceSite(random_location()))
    workplace2 = world.sites.append(WorkplaceSite(random_location()))

    # decisions happen in order, should order decisions per all people?
    world.people.append(Person(
        [TraitSex(SEX.MALE), TraitAge(30)],
        [GetTestedProcedure(), GoHomeProcedure(household, TimeFrame()), GoWorkProcedure(workplace1, TimeFrame()),
         DecisionEvaluateSiteInfection()]
    ))
    world.appendPerson(Person(
        [TraitSex(SEX.FEMALE), TraitAge(30)],
        [GetTestedProcedure(), GoHomeProcedure(household, TimeFrame()), GoWorkProcedure(workplace2, TimeFrame()),
         DecisionEvaluateSiteInfection()]
    ))

    world.tick()
    pass


if __name__ == '__main__':
    main()
