from core.site import Site
from procedures.base import SiteProcedure


class TestProcedureSite(SiteProcedure):
    def apply(self, site: Site):
        pass

    def should_apply(self, site: Site) -> bool:
        return False
