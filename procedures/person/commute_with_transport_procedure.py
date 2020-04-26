from enum import Enum

from core.person import Person
from core.site import Site
from core.world import world
from procedures.person.commute_procedure import CommuteProcedure
from sites.transport import TransportSite


class COMMUTE_STATE(Enum):
    PREVIOUS_DEST = 1
    COMMUTING = 2
    ARRIVED = 3


class CommuteWithTransportProcedure(CommuteProcedure):
    def __init__(
            self,
            destination_sites,
            initial_sites=None,
            days=None,
            time_in_day_interval=None,
            time_in_site=None,
            probability_per_minute=1.0
    ):
        CommuteProcedure.__init__(self, destination_sites, initial_sites, days, time_in_day_interval, time_in_site,
                                  probability_per_minute)

        self.commute_state = COMMUTE_STATE.PREVIOUS_DEST
        self.current_dest = None
        self.commuting_eta_tick = None

    def should_apply(self, person: Person) -> bool:
        return self.commute_state.COMMUTING or \
               ((self.commute_state == COMMUTE_STATE.PREVIOUS_DEST) and
                (CommuteProcedure.should_apply(self, person)))

    def apply(self, person: Person):
        if self.commute_state is COMMUTE_STATE.PREVIOUS_DEST:
            self.current_dest = self._get_destination()
            site_transport = self.find_transport(person, person.site, self.current_dest)
            self.commuting_eta_tick = site_transport.eta_tick(self.current_dest)
            person.site = site_transport
            self.commute_state = COMMUTE_STATE.COMMUTING
        elif self.commute_state is COMMUTE_STATE.COMMUTING and (self.commuting_eta_tick in world.current_tf):
            person.site = self.current_dest
            self.commute_state = COMMUTE_STATE.ARRIVED
            self.current_dest = None
            self.commuting_eta_tick = None

    def find_transport(self, person: Person, from_site: Site, to_site: Site) -> TransportSite:
        return TransportSite()
