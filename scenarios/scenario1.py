import random
from datetime import timedelta

import numpy as np

from core.world import world
from core.person import Person
from core.site import GeoLocation
from core.scenario import Scenario

from policies.stay_home_if_has_symptoms import StayHomeIfHasSymptoms
from procedures.person.commute_procedure import CommuteProcedure
from procedures.person.illness import IllnessProcedure
from procedures.sites.infect import InfectProcedure
from sites.household import HouseholdSite
from sites.workplace import WorkplaceSite
from sites.school import SchoolSite
from sites.hub import HubSite
from utils.time_utils import SECONDS_IN_WEEK
from constants import OCCUPATION, SEX


class Scenario1(Scenario):
    def build(self):
        number_of_family_households = 200
        number_of_elder_households = 20
        number_of_schools = 1
        number_of_workplaces = 20
        percentage_of_sick = 1
        workplaces = []
        schools = []

        world.append_policy(StayHomeIfHasSymptoms())

        self.hub = HubSite(
            location=GeoLocation(-300.0, -300.0),
            area=500.0,
            dispersion_factor=1.0,
            nominal_capacity=100
        )

        world.append_site(self.hub)
        self.hub.add_procedure(InfectProcedure())

        for _ in range(number_of_workplaces):
            workplaces.append(self.create_workplace())

        for _ in range(number_of_schools):
            schools.append(self.create_school())
             
        for _ in range(number_of_elder_households):
            self.create_elder_household()

        for _ in range(number_of_family_households):
            workplace1 = random.choice(workplaces)
            workplace2 = random.choice(workplaces)
            school = random.choice(schools)
            self.create_family_household(workplace1,workplace2,school)

        self.initial_infected(percentage_of_sick)


    def get_hub_procedures(self, house):
        to_hub = CommuteProcedure(
            destination_sites=self.hub,
            probability_per_minute=60 / SECONDS_IN_WEEK
        )

        from_hub = CommuteProcedure(
            destination_sites=house,
            initial_sites=self.hub,
            time_in_site=timedelta(hours=1))

        return to_hub, from_hub

    def get_workplace_procedures(self, workplace, house):
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


    def create_elder_household(self):
        house = HouseholdSite(
            location=GeoLocation(random.uniform(-300, 300),
                                 random.uniform(-300, 300)),
            area=random.uniform(40, 60),
            dispersion_factor=1.0,
            nominal_capacity=random.randint(3, 6)
        )
        world.append_site(house)

        house.add_procedure(InfectProcedure())

        to_hub, from_hub = self.get_hub_procedures(house)
        age = 60 + np.random.exponential(7)

        for _ in range(2):
            person = Person(
                age=age + random.uniform(-5, 5),
                sex=SEX.MALE,
                occupation=OCCUPATION.UNEMPLOYED,
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

            world.append_person(person)


    def create_family_household(self, workplace1, workplace2, school):
        house = HouseholdSite(
            location=GeoLocation(random.uniform(-300, 300),
                                 random.uniform(-300, 300)),
            area=random.uniform(40, 60),
            dispersion_factor=1.0,
            nominal_capacity=random.randint(3, 6)
        )
        world.append_site(house)

        house.add_procedure(InfectProcedure())

        to_hub, from_hub = self.get_hub_procedures(house)
        parents_age = random.uniform(25, 60)
        workplaces = [workplace1, workplace2]

        # parents
        for i in range(2):
            person = Person(
                age=parents_age + random.uniform(-5, 5),
                sex=SEX.MALE,
                occupation=OCCUPATION.WORKER,
                susceptibility_degree=1.0,
                obedient_degree=1.0,
                is_infected=False,
                symptoms_degree=0.0,
                immunity_degree=0.0,
                timestamp_infected=None,
                timestamp_symptomatic=None,
                household=house
            )
            world.append_person(person)

            to_workplace, from_workplace = self.get_workplace_procedures(workplaces[i],
                                                                    house)

            person.add_procedure(to_workplace)
            person.add_procedure(from_workplace)
            if to_hub is not None:
                person.add_procedure(to_hub)
                person.add_procedure(from_hub)
            person.add_procedure(IllnessProcedure())

        if (parents_age > 30) and (parents_age < 50):

            to_school, from_school = self.get_workplace_procedures(
                school, house)

            # children
            for _ in range(random.choices(range(6),
                                          [0.087, 0.174, 0.348, 0.174, 0.13,
                                           0.087])[0]):
                person = Person(
                    age=parents_age - 25 + random.uniform(-5, 5),
                    sex=SEX.MALE,
                    occupation=OCCUPATION.STUDENT,
                    susceptibility_degree=1.0,
                    obedient_degree=1.0,
                    is_infected=False,
                    symptoms_degree=0.0,
                    immunity_degree=0.0,
                    timestamp_infected=None,
                    timestamp_symptomatic=None,
                    household=house
                )
                world.append_person(person)

                person.add_procedure(to_school)
                person.add_procedure(from_school)
                if to_hub is not None:
                    person.add_procedure(to_hub)
                    person.add_procedure(from_hub)
                person.add_procedure(IllnessProcedure())


    def create_workplace(self):
        workplace = WorkplaceSite(
            location=GeoLocation(random.normalvariate(0, 100), random.normalvariate(0, 100)),
            area=random.uniform(100, 300),
            dispersion_factor=1.0,
            nominal_capacity=random.randint(15, 25))
        world.append_site(workplace)
        workplace.add_procedure(InfectProcedure())
        return workplace


    def create_school(self):
        school = SchoolSite(
            location=GeoLocation(random.uniform(-300, 300),
                                    random.uniform(-300, 300)),
            area=random.uniform(300, 1000),
            dispersion_factor=1.0,
            nominal_capacity=random.randint(100, 500))
        world.append_site(school)
        school.add_procedure(InfectProcedure())
        
        return school

    def initial_infected(self, percentage_of_sick):
        for person in world.people:
            if random.random() < percentage_of_sick/100:
                person.is_infected = True
                person.timestamp_infected = world.current_time - timedelta(days=1)*random.uniform(0,5)


