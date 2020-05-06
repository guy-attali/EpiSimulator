import random
from datetime import timedelta

from constants import OCCUPATION, SEX
from core.person import Person
from core.scenario import Scenario
from core.site import GeoLocation, Site
from core.world import world
import policies.lockdown
from procedures.person.commute_procedure import CommuteProcedure
from procedures.person.illness import IllnessProcedure
from procedures.sites.infect import InfectProcedure
from sites.household import HouseholdSite
from sites.hub import HubSite
from sites.school import SchoolSite
from sites.workplace import WorkplaceSite
from utils.time_utils import SECONDS_IN_WEEK, WORK_DAYS
from core.traits import SiteTraits

def get_value(var):
    if callable(var):
        return var()
    else:
        return var


class Scenario2(Scenario):
    def __init__(self, scenario_params):
        self.scenario_params = scenario_params

        random.seed(self.scenario_params['seed'])
        self.config_file_path = 'config.yml'
        self.time_step = timedelta(minutes=120)

    def build(self):
        for policy in self.scenario_params['policies']:
            world.append_policy(policy)
        self.gen_city(0)
        self.initial_infected(self.scenario_params['initial_infected_percentage'],
                              self.scenario_params['initial_infected_neighborhoods'])

    def gen_city(self, city_id):
        neighborhood_schools_dict = {}
        neighborhood_workplaces_dict = {}
        neighborhood_hub_dict = {}
        num_of_neighborhoods = get_value(self.scenario_params['num_of_neighborhoods'])
        for neighborhood_id in range(num_of_neighborhoods):
            neighborhood_params = {'location': GeoLocation(0, 0)}
            schools, workplaces = self.gen_neighborhood_public_sites(neighborhood_id, city_id, neighborhood_params)
            neighborhood_hub_dict[neighborhood_id] = self.gen_neighborhood_hub(neighborhood_id, city_id, neighborhood_params)
            neighborhood_schools_dict[neighborhood_id] = schools
            neighborhood_workplaces_dict[neighborhood_id] = workplaces

        # generate households
        for neighborhood_id in range(num_of_neighborhoods):
            for _ in range(get_value(self.scenario_params['num_households_per_neighborhood'])):
                children, adults = self.gen_household(neighborhood_id, city_id)
                for child in children:
                    classroom = random.choice(neighborhood_schools_dict[neighborhood_id])
                    self.assign_person_to_work_or_school(child, classroom)
                for adult in adults:
                    office = self.select_workplace(neighborhood_workplaces_dict, neighborhood_id, neighborhood_hub_dict)
                    self.assign_person_to_work_or_school(adult, office)
        self.send_people_to_hubs(neighborhood_hub_dict)
        self.add_procedures_to_all_people([IllnessProcedure])
        self.add_procedures_to_all_sites([InfectProcedure])

    def gen_neighborhood_hub(self, neighborhood_id, city_id, neighborhood_params):
        hub = HubSite(
            neighborhood_params['location'], area=100,
            dispersion_factor=1,
            nominal_capacity=100,
            neighborhood_id=neighborhood_id, city_id=city_id,
            name=f'neighborhood_{neighborhood_id}_hub')
        return hub

    def send_people_to_hubs(self, neighborhood_hub_dict):
        for person in world.people:
            hub = neighborhood_hub_dict[person.household.traits.neighborhood_id]
            to_hub = CommuteProcedure(
                destination_sites=hub,
                initial_sites=person.household,
                probability_per_minute=0.001  # add to params
            )
            from_hub = CommuteProcedure(
                destination_sites=person.household,
                initial_sites=hub,
                time_in_site=timedelta(hours=1)  # add to params
            )
            person.add_procedure(to_hub)
            person.add_procedure(from_hub)


    def add_procedures_to_all_people(self, procedures):
        for person in world.people:
            for procedure in procedures:
                person.add_procedure(procedure())

    def add_procedures_to_all_sites(self, procedures):
        for site in world.sites:
            for procedure in procedures:
                site.add_procedure(procedure())

    def assign_person_to_work_or_school(self, person, work_or_school):
        start_time = timedelta(hours=8)  # add to params
        end_time = timedelta(hours=14)  # add to params
        if work_or_school.traits.parent_site is not None:
            self.assign_person_to_work_or_school_cluster(person, work_or_school, start_time, end_time)
        else:
            self.assign_person_to_work_or_school_not_cluster(person, work_or_school, start_time, end_time)

    def assign_person_to_work_or_school_cluster(self, person, work_or_school, start_time, end_time):
            to_work = CommuteProcedure(
                destination_sites=work_or_school, days=WORK_DAYS,
                time_in_day_interval=(start_time, end_time),
                probability_per_minute=1)
            from_work = CommuteProcedure(
                destination_sites=person.household,
                initial_sites=[work_or_school, work_or_school.traits.parent_site],
                time_in_day_interval=(end_time, timedelta(hours=24)),
                probability_per_minute=1)  # add to params
            to_work_hub = CommuteProcedure(
                destination_sites=work_or_school.traits.parent_site,
                initial_sites=work_or_school,
                probability_per_minute=0.001)  # add to params
            from_work_hub = CommuteProcedure(
                destination_sites=work_or_school,
                initial_sites=work_or_school.traits.parent_site,
                time_in_site=timedelta(hours=1),  # add to params
                probability_per_minute=1)
            person.add_procedure(to_work)
            person.add_procedure(from_work)
            person.add_procedure(to_work_hub)
            person.add_procedure(from_work_hub)

    def assign_person_to_work_or_school_not_cluster(self, person, work_or_school, start_time, end_time):
            to_work = CommuteProcedure(
                destination_sites=work_or_school, days=WORK_DAYS,
                time_in_day_interval=(start_time, end_time),
                probability_per_minute=1)
            from_work = CommuteProcedure(
                destination_sites=person.household,
                initial_sites=work_or_school,
                time_in_day_interval=(end_time, timedelta(hours=24)),
                probability_per_minute=1)  # add to params
            person.add_procedure(to_work)
            person.add_procedure(from_work)

    def select_workplace(self, neighborhood_workplaces_dict, neighborhood_id, neighborhood_hub_dict):
        if random.random() < self.scenario_params['work_in_hub_prob']:
            return neighborhood_hub_dict[neighborhood_id]
        else:
            if random.random() < self.scenario_params['work_in_neighborhood_prob']:
                work_neighborhood_id = neighborhood_id
            else:
                # select a random neighborhood that is not the original one
                work_neighborhood_id = random.choice(
                    list(set(neighborhood_workplaces_dict.keys()) - {neighborhood_id})
                )
            return random.choice(neighborhood_workplaces_dict[work_neighborhood_id])

    def gen_household(self, neighborhood_id, city_id):
        home = HouseholdSite(location=GeoLocation(0, 0), area=10,
                             dispersion_factor=10, nominal_capacity=10,
                             neighborhood_id=neighborhood_id, city_id=city_id,
                             name=f'house_in_neighborhood_{neighborhood_id}')
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

    def gen_neighborhood_public_sites(self, neighborhood_id, city_id, neighborhood_params):
        schools = []
        workplaces = []
        for _ in range(get_value(self.scenario_params['num_schools_per_neighborhood'])):
            school_location = neighborhood_params['location']
            schools.extend(self.gen_public_site('school', school_location, neighborhood_id, city_id))
        for _ in range(get_value(self.scenario_params['num_workplaces_per_neighborhood'])):
            work_location = GeoLocation(0, 0)
            workplaces.extend(self.gen_public_site('work', work_location, neighborhood_id, city_id))
        return schools, workplaces

    def gen_public_site(self, site_type, location, neighborhood_id, city_id):
        sub_list = []
        num_of_sub_sites = get_value(self.scenario_params[site_type]['num_of_sub_sites'])
        location = GeoLocation(*get_value(location))
        hub_area = get_value(self.scenario_params[site_type]['hub_area'])
        hub_dispersion = get_value(self.scenario_params[site_type]['hub_dispersion'])
        hub_capacity = get_value(self.scenario_params[site_type]['hub_capacity'])
        if num_of_sub_sites > 1:  # this hub is only for container sites
            hub = Site(
                location=location,
                area=hub_area,
                dispersion_factor=hub_dispersion,
                nominal_capacity=hub_capacity,
                neighborhood_id=neighborhood_id,
                city_id=city_id,
                name=f'{site_type}_hub_in_neighborhood_{neighborhood_id}'
            )
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
                city_id=city_id,
                name=f'{site_type}_in_neighborhood_{neighborhood_id}'
            )
            sub_list.append(sub)
        return sub_list

    def initial_infected(self, initial_infected_percentage, initial_infected_neighborhoods=None):
        for person in world.people:
            if random.random() < initial_infected_percentage / 100 and \
                    (initial_infected_neighborhoods is None or
                     person.household.traits.neighborhood_id in initial_infected_neighborhoods):
                person.traits.is_infected = True
                person.traits.timestamp_infected = world.current_time - timedelta(days=1) * random.uniform(0, 5)

def main():
    scenario_params = {
        'seed': None,
        'num_of_neighborhoods': 3,
        'school': {
            'num_of_sub_sites': 10,
            'hub_area': 100, 'hub_dispersion': 0.5, 'hub_capacity': 50,
            'sub_area': 100, 'sub_dispersion': 0.5, 'sub_capacity': 50,
        },
        'work': {
            'num_of_sub_sites': 2,
            'hub_area': 100, 'hub_dispersion': 0.5, 'hub_capacity': 50,
            'sub_area': 100, 'sub_dispersion': 0.5, 'sub_capacity': 50,
        },
        'work_in_neighborhood_prob': 0.5,
        'work_in_hub_prob': 1.,
        'num_schools_per_neighborhood': 3,
        'num_workplaces_per_neighborhood': 10,
        'num_households_per_neighborhood': 100,
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
        },
        'initial_infected_percentage': 20,
        'initial_infected_neighborhoods': [1],
        'policies': [policies.lockdown.Lockdown()]
    }
    s = Scenario2(scenario_params)
    s.build()


if __name__ == '__main__':
    main()

# sites_in_procedures = []
# for person in world.people:
#     for procedure in person.procedures:
#         if procedure.is_type(CommuteProcedure):
#             sites_in_procedures.append(procedure.decorated_procedure.initial_sites)
#             sites_in_procedures.append(procedure.decorated_procedure.dest_sites)
