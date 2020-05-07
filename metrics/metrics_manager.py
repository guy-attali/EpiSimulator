from core.world import world
from sites.hub import HubSite
import pandas as pd

class MetricManager:
    def __init__(self):
        self.log = []

    def calc_reproduction_number(self):
        """
        Calculate the "reproduction number".
        The idea is to calculate the average number of new infections for all the infective people
        and multiply by the infection duration.
        :return: R
        """
        n_infected = sum([1 for p in world.people if p.traits.is_infected])
        new_infections = sum([1 for p in world.people
                              if p.traits.is_infected and
                              (p.traits.timestamp_infected in world.current_tf)])
        return 1
        # infecting = (self.pop_df.status == 'I') & \
        #             (self.pop_df.days_in_status > 0) & ~self.pop_df.is_isolated
        # if infecting.sum() == 0:
        #     return np.nan
        # R = self.params['infection_duration'] * self.params['iter_per_day'] * \
        #     (new_infections.sum() / infecting.sum())
        # return R

    def get_sir_distribution(self):
        s = 0
        i = 0
        r = 0
        for person in world.people:
            if person.traits.is_infected:
                i += 1
            elif person.traits.immunity_degree > 0:
                r += 1
            else:
                s += 1

        tot = len(world.people)
        return s / tot, i / tot, r / tot

    def get_sir_people_uuid(self):
        s = []
        i = []
        r = []
        for person in world.people:
            if person.traits.is_infected:
                i.append(person.uuid)
            elif person.traits.immunity_degree > 0:
                r.append(person.uuid)
            else:
                s.append(person.uuid)

        return s, i, r

    def get_site_distribution(self):
        at_home = 0
        at_work_or_school = 0
        at_hub = 0
        for person in world.people:
            if person.site is person.household:
                at_home += 1
            elif isinstance(person.site, HubSite):
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
        print('reproduction_number: {}'.format(self.calc_reproduction_number()))
        print('')

    def connections_graph(self):
        connections = set()
        for site in world.sites:
            people = list(site.people)
            for i, person_1 in enumerate(people[:-1]):
                for person_2 in people[i+1:]:
                    if person_1 is not person_2:
                        connections.add((person_1.uuid, person_2.uuid))
        return connections

    def add_to_log(self, log_metrics=None):
        cur_metrics = {'time': world.current_time}
        if log_metrics is None or \
                'sir_distribution' in log_metrics:
            s, i, r = self.get_sir_distribution()
            cur_metrics.update({'s': s, 'i': i, 'r': r})
        if log_metrics is None or \
                'site_distribution' in log_metrics:
            at_home, at_work_or_school, at_hub = self.get_site_distribution()
            cur_metrics.update({'at_home': at_home,
                                'at_work_or_school': at_work_or_school,
                                'at_hub': at_hub
                                })
        if log_metrics is None or \
                'connections' in log_metrics:
            cur_metrics.update({'connections': self.connections_graph()})
        if log_metrics is None or \
                'sir_people_uuid' in log_metrics:
            cur_metrics.update({'sir_people_uuid': self.get_sir_people_uuid()})
        self.log.append(cur_metrics)

    def to_df(self):
        metrics_df = pd.DataFrame(self.log)
        metrics_df['time_days'] = metrics_df.time.apply(lambda x: x.timestamp()) / (24*60*60)
        metrics_df['time_days'] = metrics_df['time_days'] - metrics_df.loc[0, 'time_days']
        return metrics_df
