import random
from datetime import timedelta

import numpy as np

from core.world import world
from people.person import Person
from people.traits import Occupation, Sex
from policies.stay_home_if_has_symptoms import StayHomeIfHasSymptoms
from procedures.person.commute_procedure import CommuteProcedure
from procedures.person.illness import IllnessProcedure
from procedures.sites.infect import InfectProcedure
from sites.base import GeoLocation
from sites.base import Site
from sites.household import HouseholdSite
from sites.workplace import WorkplaceSite
from sites.school import SchoolSite
from sites.hub import HubSite
from utils.time_utils import SECONDS_IN_WEEK

def setup_world():

    number_of_family_households = 200
    number_of_elder_households = 20
    number_of_schools = 1
    number_of_workplaces = 20
    percentage_of_sick = 1

    policy = StayHomeIfHasSymptoms()
    world.policies.append(policy)

    hub = HubSite(
        location=GeoLocation(-300.0, -300.0),
        area=500.0,
        dispersion_factor=1.0,
        nominal_capacity=100
    )
    world.sites.append(hub)
    hub.add_procedure(InfectProcedure())


    def get_hub_procedures(house):
        to_hub = CommuteProcedure(
            destination_sites=hub,
            probability_per_minute=60 / SECONDS_IN_WEEK
        )

        from_hub = CommuteProcedure(
            destination_sites=house,
            initial_sites=hub,
            time_in_site=timedelta(hours=1))

        return to_hub, from_hub

    def get_workplace_procedures(workplace, house):
        to_workplace = CommuteProcedure(
            destination_sites=workplace,
            initial_sites=house,
            days=[6, 0, 1, 2, 3],
            time_in_day_interval=(timedelta(hours=7), timedelta(hours=9)),
            probability_per_minute=0.01
        )

        from_workplace = CommuteProcedure(
            destination_sites=house,
            initial_sites=workplace,
            time_in_day_interval=(timedelta(hours=16), timedelta(hours=24)),
            probability_per_minute=0.04,
        )

        return to_workplace, from_workplace


    def create_elder_household():
        house = HouseholdSite(
            location=GeoLocation(random.uniform(-300, 300),
                                 random.uniform(-300, 300)),
            area=random.uniform(40, 60),
            dispersion_factor=1.0,
            nominal_capacity=random.randint(3, 6)
        )
        world.sites.append(house)

        house.add_procedure(InfectProcedure())

        to_hub, from_hub = get_hub_procedures(house)
        age = 60 + np.random.exponential(7)

        for _ in range(2):
            person = Person(
                age=age + random.uniform(-5, 5),
                sex=Sex.MALE,
                occupation=Occupation.UNEMPLOYED,
                susceptibility_degree=1.0,
                obedient_degree=1.0,
                is_infected=False,
                symptoms_degree=0.0,
                immunity_degree=0.0,
                timestamp_infected=None,
                timestamp_symptomatic=None,
                household=house
            )
            if to_hub is not None:
                person.add_procedure(to_hub)
                person.add_procedure(from_hub)
            person.add_procedure(IllnessProcedure())

            world.people.append(person)


    def create_family_household(workplace1, workplace2, school):
        house = HouseholdSite(
            location=GeoLocation(random.uniform(-300, 300),
                                 random.uniform(-300, 300)),
            area=random.uniform(40, 60),
            dispersion_factor=1.0,
            nominal_capacity=random.randint(3, 6)
        )
        world.sites.append(house)

        house.add_procedure(InfectProcedure())

        to_hub, from_hub = get_hub_procedures(house)
        parents_age = random.uniform(25, 60)
        workplaces = [workplace1, workplace2]

        # parents
        for i in range(2):
            person = Person(
                age=parents_age + random.uniform(-5, 5),
                sex=Sex.MALE,
                occupation=Occupation.WORKER,
                susceptibility_degree=1.0,
                obedient_degree=1.0,
                is_infected=False,
                symptoms_degree=0.0,
                immunity_degree=0.0,
                timestamp_infected=None,
                timestamp_symptomatic=None,
                household=house
            )
            world.people.append(person)

            to_workplace, from_workplace = get_workplace_procedures(workplaces[i],
                                                                    house)

            person.add_procedure(to_workplace)
            person.add_procedure(from_workplace)
            if to_hub is not None:
                person.add_procedure(to_hub)
                person.add_procedure(from_hub)
            person.add_procedure(IllnessProcedure())

        if (parents_age > 30) and (parents_age < 50):

            to_school, from_school = get_workplace_procedures(
                school, house)

            # children
            for _ in range(random.choices(range(6),
                                          [0.087, 0.174, 0.348, 0.174, 0.13,
                                           0.087])[0]):
                person = Person(
                    age=parents_age - 25 + random.uniform(-5, 5),
                    sex=Sex.MALE,
                    occupation=Occupation.STUDENT,
                    susceptibility_degree=1.0,
                    obedient_degree=1.0,
                    is_infected=False,
                    symptoms_degree=0.0,
                    immunity_degree=0.0,
                    timestamp_infected=None,
                    timestamp_symptomatic=None,
                    household=house
                )
                world.people.append(person)

                person.add_procedure(to_school)
                person.add_procedure(from_school)
                if to_hub is not None:
                    person.add_procedure(to_hub)
                    person.add_procedure(from_hub)
                person.add_procedure(IllnessProcedure())


    def create_workplaces():
        workplaces = []
        for _ in range(number_of_workplaces):
            workplace = WorkplaceSite(
                location=GeoLocation(random.normalvariate(0, 100), random.normalvariate(0, 100)),
                area=random.uniform(100, 300),
                dispersion_factor=1.0,
                nominal_capacity=random.randint(15, 25))
            world.sites.append(workplace)
            workplace.add_procedure(InfectProcedure())
            workplaces.append(workplace)

        return workplaces


    def create_schools():
        schools = []
        for _ in range(number_of_schools):
            school = SchoolSite(
                location=GeoLocation(random.uniform(-300, 300),
                                     random.uniform(-300, 300)),
                area=random.uniform(300, 1000),
                dispersion_factor=1.0,
                nominal_capacity=random.randint(100, 500))
            world.sites.append(school)
            school.add_procedure(InfectProcedure())
            schools.append(school)

        return schools

    def initial_infected():
        for person in world.people:
            if random.random() < percentage_of_sick/100:
                person.is_infected = True
                person.timestamp_infected = world.current_time - timedelta(days=1)*random.uniform(0,5)


    workplaces = create_workplaces()
    schools = create_schools()

    for _ in range(number_of_elder_households):
        create_elder_household()

    for _ in range(number_of_family_households):
        workplace1 = random.choice(workplaces)
        workplace2 = random.choice(workplaces)
        school = random.choice(schools)
        create_family_household(workplace1,workplace2,school)

    initial_infected()

