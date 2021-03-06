import abc
from datetime import datetime
from typing import Optional

from constants import OCCUPATION, SEX


class Traits(abc.ABC):
    pass


# TODO: Maybe the specific traits in another file?
class PersonTraits(Traits):
    def __init__(self,
                 age: float,
                 sex: SEX,
                 occupation: OCCUPATION,
                 susceptibility_degree: float,
                 obedient_degree: float,
                 is_infected: bool,
                 symptoms_degree: float,
                 immunity_degree: float,
                 timestamp_infected: Optional[datetime],
                 timestamp_symptomatic: Optional[datetime],
                 infectious_level: float):
        self.age: float = age
        self.sex: SEX = sex
        self.occupation: OCCUPATION = occupation
        self.susceptibility_degree: float = susceptibility_degree
        self.obedient_degree: float = obedient_degree
        self.is_infected: bool = is_infected
        self.symptoms_degree: float = symptoms_degree
        self.immunity_degree: float = immunity_degree
        self.timestamp_infected: Optional[datetime] = timestamp_infected
        self.timestamp_symptomatic: Optional[datetime] = timestamp_symptomatic
        self.infectious_level: float = infectious_level

        self.check_input_validity()

    def check_input_validity(self):
        assert ((not self.is_infected) and
                (self.timestamp_infected is None) and
                (self.timestamp_symptomatic is None) and
                (self.symptoms_degree == 0)) \
               or (self.is_infected and
                   (self.timestamp_infected is not None) and
                   (self.timestamp_symptomatic is not None) and
                   (self.timestamp_symptomatic >= self.timestamp_infected))


class SiteTraits(Traits):
    def __init__(self, dispersion_factor: float, nominal_capacity: int,
                 neighborhood_id: Optional[int]=None, city_id: Optional[int]=None,
                 parent_site: 'Site'=None):
        # the typical maximal number of people that the site can contain
        self.nominal_capacity = nominal_capacity

        # this value determines the tendency of people in the site to move around
        # (lower values mean that people are relatively static)
        self.dispersion_factor = dispersion_factor

        self.parent_site = parent_site
        self.city_id = city_id
        self.neighborhood_id = neighborhood_id
