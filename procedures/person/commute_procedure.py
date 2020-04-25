from typing import Optional, Union, Iterable, Tuple
from enum import Enum
from datetime import timedelta
import random

from people.person import Person
from core.world import world
from procedures.base import PersonProcedure
from sites.base import Site
from sites.transport import TransportSite
from utils.timeframe import TimeFrame
from utils.time_utils import get_start_of_day, time_since

class CommuteProcedure(PersonProcedure):
    def __init__(
            self,
            destination_sites: Union[Site, Iterable[Site]],
            initial_sites: Optional[Union[Site, Iterable[Site]]] = None,
            days: Optional[Union[int,Iterable[int]]] = None,
            time_in_day_interval: Optional[Tuple[timedelta, timedelta]] = None,
            time_in_site: Optional[timedelta] = None,
            probability_per_minute = 1.0
    ):
        self.dest_sites = destination_sites
        self.initial_sites = initial_sites
        self.days = days
        self.time_in_day_interval = time_in_day_interval
        self.time_in_site = time_in_site
        self.probability_per_minute = probability_per_minute

    def should_apply(self, person: Person) -> bool:

        # check condition for initial location
        if self.initial_sites is not None:
            if isinstance(self.initial_sites, Site):
                if person is not self.initial_sites:
                    return False
            else:
                if all(person not in init_site for init_site in self.initial_sites):
                    return False

        # check condition for day of weak
        if self.days is not None:
            current_day = world.current_time.weekday
            if isinstance(self.days, int):
                if current_day != self.days:
                    return False
                else:
                    if current_day not in self.days:
                        return False

        # check condition for time of day
        if self.time_in_day_interval is not None:
            start_of_today = get_start_of_day()
            dt1 = self.time_in_day_interval[0]
            dt2 = self.time_in_day_interval[1]
            timeframe = TimeFrame(start_of_today+dt1, start_of_today+dt2)
            if world.current_tf.overlap(timeframe) == 0.0:
                return False

        # check condition for total time in current site
        if self.time_in_site is not None:
            time_in_site = time_since(person.timestamp_arrived)
            if time_in_site < self.time_in_site:
                return False

        # randomly decide whether the pattern will be executed
        if random.random() > ((world.current_tf.duration.total_seconds()/60) * self.probability_per_minute):
            return False

        return True

    def apply(self, person: Person):
        person.site = self._get_destination()

    def _get_destination(self):
        if isinstance(self.dest_sites, Site):
            return self.dest_sites
        else:
            return random.choice(self.dest_sites)
