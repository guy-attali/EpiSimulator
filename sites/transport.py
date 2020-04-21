from sites.abstract import Site


class TransportSite(Site):
    def eta_tick(self, dest_site):
        pass
        # return clock.getFutureTick(self.distance(dest_site))  # speed blah blah


class Bus(TransportSite):
    pass


class PrivateCar(TransportSite):
    pass
