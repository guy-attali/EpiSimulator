from core.world import world
from sites.hub import Hub


class MetricManager:
    def __init__(self):
        pass

    def get_sir_distribution(self):
        s = 0
        i = 0
        r = 0
        for person in world.people:
            if person.is_infected:
                i += 1
            elif person.immunity_degree > 0:
                r += 1
            else:
                s += 1

        tot = len(world.people)
        return s / tot, i / tot, r / tot

    def get_site_distribution(self):
        at_home = 0
        at_work_or_school = 0
        at_hub = 0
        for person in world.people:
            if person.site is person.household:
                at_home += 1
            elif isinstance(person.site, Hub):
                at_hub += 1
            else:
                at_work_or_school += 1

        tot = len(world.people)

        return at_home / tot, at_work_or_school / tot, at_hub / tot

    def show(self):
        s, i, r = self.get_sir_distribution()
        at_home, at_work_or_school, at_hub = self.get_site_distribution()
        print(world.current_time)
        print('S: {:6.2f}%   I: {:6.2f}%   R: {:6.2f}%'.format(s * 100, i * 100,
                                                               r * 100))
        print('home: {:6.2f}%   work/school: {:6.2f}%   hub: {:6.2f}%'.format(
            at_home * 100, at_work_or_school * 100, at_hub * 100))
        print('')
