import random
from datetime import timedelta

from constants import OCCUPATION, SEX
from core.person import Person
from core.scenario import Scenario
from core.site import GeoLocation, Site
from core.world import world
from policies.lockdown import Lockdown
from procedures.person.commute_procedure import CommuteProcedure
from procedures.person.illness import IllnessProcedure
from procedures.sites.infect import InfectProcedure
from sites.household import HouseholdSite
from sites.hub import HubSite
from sites.school import SchoolSite
from sites.workplace import WorkplaceSite
from utils.time_utils import SECONDS_IN_WEEK
from core.traits import SiteTraits

def get_value(var):
    if callable(var):
        return var()
    else:
        return var


class Scenario2(Scenario):
    def __init__(self):
        self.scenario_params = {
            'seed': 23,
            'num_of_neighborhoods': 5,
            'school': {
                'num_of_sub_sites': 10,
                'hub_area': 100, 'hub_dispersion': 0.5, 'hub_capacity': 50,
                'sub_area': 100, 'sub_dispersion': 0.5, 'sub_capacity': 50,
            },
            'work': {
                'num_of_sub_sites': 10,
                'hub_area': 100, 'hub_dispersion': 0.5, 'hub_capacity': 50,
                'sub_area': 100, 'sub_dispersion': 0.5, 'sub_capacity': 50,
            },
            'work_in_neighborhood_prob': 0.5,
            'num_schools_per_neighborhood': 1,
            'num_workplaces_per_neighborhood': 10,
            'num_households_per_neighborhood': 50,
            'num_adults_in_household': 2,
            'num_children_in_household': 3,
            'person_default_params': {
                'age': 10,
                'sex': SEX.FEMALE,
                'occupation': None,
                'susceptibility_degree': 1,
                'obedient_degree': 1,
                'is_infected': False,
                'symptoms_degree': 0,
                'immunity_degree': 0,
                'timestamp_infected': None,
                'timestamp_symptomatic': None
            }
        }

        random.seed(self.scenario_params['seed'])
        self.config_file_path = 'config.yml'
        self.time_step = timedelta(minutes=120)

    def build(self):
        world.append_policy(Lockdown())
        self.gen_city(0)

    def gen_city(self, city_id):
        neighborhood_schools_dict = {}
        neighborhood_workplaces_dict = {}
        for neighborhood_id in range(get_value(self.scenario_params['num_of_neighborhoods'])):
            schools, workplaces = self.gen_neighborhood_public_sites(neighborhood_id, city_id)
            neighborhood_schools_dict[neighborhood_id] = schools
            neighborhood_workplaces_dict[neighborhood_id] = workplaces

        # generate households
        for neighborhood_id in range(get_value(self.scenario_params['num_of_neighborhoods'])):
            for _ in range(get_value(self.scenario_params['num_households_per_neighborhood'])):
                children, adults = self.gen_household()
                for child in children:
                    classroom = random.choice(neighborhood_schools_dict[neighborhood_id])
                    self.assign_person_to_work_or_school(child, classroom)
                for adult in adults:
                    office = self.select_workplace(neighborhood_workplaces_dict, neighborhood_id)
                    self.assign_person_to_work_or_school(adult, office)
        self.add_procedures_to_all_people([IllnessProcedure])
        self.add_procedures_to_all_sites([InfectProcedure])

    def add_procedures_to_all_people(self, procedures):
        for person in world.people:
            for procedure in procedures:
                person.add_procedure(procedure())

    def add_procedures_to_all_sites(self, procedures):
        for site in world.sites:
            for procedure in procedures:
                site.add_procedure(procedure())

    def assign_person_to_work_or_school(self, person, work_or_school):
        pass

    def select_workplace(self, neighborhood_workplaces_dict, neighborhood_id):
        if random.random() < self.scenario_params['work_in_neighborhood_prob']:
            work_neighborhood_id = neighborhood_id
        else:
            # select a random neighborhood that is not the original one
            work_neighborhood_id = random.choice(
                list(set(neighborhood_workplaces_dict.keys()) - {neighborhood_id})
            )
        workplaces_group = random.choice(neighborhood_workplaces_dict[work_neighborhood_id])
        return random.choice(workplaces_group)

    def gen_household(self):
        home = HouseholdSite(location=GeoLocation(0, 0), area=10,
                             dispersion_factor=10, nominal_capacity=10)
        world.append_site(home)
        num_adults_in_household = get_value(self.scenario_params['num_adults_in_household'])
        num_children_in_household = get_value(self.scenario_params['num_children_in_household'])
        adults = []
        children = []
        for _ in range(num_adults_in_household):
            adults.append(self.gen_person(home))
        for _ in range(num_children_in_household):
            children.append(self.gen_person(home))
            return children, adults

    def gen_person(self, home):
        p = Person(household=home, **self.scenario_params['person_default_params'])
        world.append_person(p)
        return p

    def gen_neighborhood_public_sites(self, neighborhood_id, city_id):
        schools = []
        workplaces = []
        for _ in range(get_value(self.scenario_params['num_schools_per_neighborhood'])):
            school_location = GeoLocation(0, 0)
            schools.append(self.gen_public_site('school', school_location, neighborhood_id, city_id))
        for _ in range(get_value(self.scenario_params['num_workplaces_per_neighborhood'])):
            work_location = GeoLocation(0, 0)
            workplaces.append(self.gen_public_site('work', work_location, neighborhood_id, city_id))
        return schools, workplaces

    def gen_public_site(self, site_type, location, neighborhood_id, city_id):
        sub_list = []
        num_of_sub_sites = get_value(self.scenario_params[site_type]['num_of_sub_sites'])
        location = GeoLocation(*get_value(location))
        hub_area = get_value(self.scenario_params[site_type]['hub_area'])
        hub_dispersion = get_value(self.scenario_params[site_type]['hub_dispersion'])
        hub_capacity = get_value(self.scenario_params[site_type]['hub_capacity'])
        if num_of_sub_sites > 1:  # this hub is only for container sites
            hub = HubSite(
                location=location,
                area=hub_area,
                dispersion_factor=hub_dispersion,
                nominal_capacity=hub_capacity,
                neighborhood_id=neighborhood_id,
                city_id=city_id
            )
            world.append_site(hub)
        else:
            hub = None

        for _ in range(num_of_sub_sites):
            sub_area = get_value(self.scenario_params[site_type]['sub_area'])
            sub_dispersion = get_value(self.scenario_params[site_type]['sub_dispersion'])
            sub_capacity = get_value(self.scenario_params[site_type]['sub_capacity'])
            sub = Site(
                location=location,
                area=sub_area,
                dispersion_factor=sub_dispersion,
                nominal_capacity=sub_capacity,
                parent_site=hub,
                neighborhood_id=neighborhood_id,
                city_id=city_id
            )
            world.append_site(sub)
            sub_list.append(sub)
        return sub_list


def main():
    s = Scenario2()
    s.build()


if __name__ == '__main__':
    main()
