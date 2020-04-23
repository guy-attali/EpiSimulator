from enum import Enum

from core.person import Person
from core.world import world
from procedures.base import PersonProcedure
from sites.base import Site
from sites.transport import TransportSite
from utils.timeframe import TimeFrame


class COMMUTE_STATE(Enum):
    PREVIOUS_DEST = 1
    COMMUTING = 2
    ARRIVED = 3


class CommuteProcedure(PersonProcedure):
    def __init__(self, dest_site: Site, timeframe):
        self.dest_site: Site = dest_site
        self.timeframe: TimeFrame = timeframe
        self.commute_state: COMMUTE_STATE = COMMUTE_STATE.PREVIOUS_DEST
        # self.commuting_eta_tick = None

    def should_apply(self, person: Person) -> bool:
        return self.timeframe.within(world.current)

    def apply(self, person: Person):
        # if within travel time?
        # add policy hook?
        # should decide on a transport site here instead of as a static?
        if self.commute_state is COMMUTE_STATE.ARRIVED and not person.current_site.equals(self.dest_site):
            self.commute_state = COMMUTE_STATE.PREVIOUS_DEST  # reset

        if self.commute_state is COMMUTE_STATE.PREVIOUS_DEST:
            site_transport = self.find_transport(person)
            self.commuting_eta_tick = site_transport.eta_tick(self.dest_site)
            person.site = site_transport
            self.commute_state = COMMUTE_STATE.COMMUTING
        elif self.commute_state is COMMUTE_STATE.COMMUTING and (self.commuting_eta_tick >= world.current):
            person.site = self.dest_site
            self.commute_state = COMMUTE_STATE.ARRIVED

        person.site = self.dest_site

    def find_transport(self, person: Person) -> TransportSite:
        return TransportSite()
