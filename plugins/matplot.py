import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from collections import namedtuple
from math import sqrt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Rectangle, RegularPolygon
from core.plugin import Plugin
from core.world import world

class PluginMatplot(Plugin):
    def __init__(self, display_interval):
        self._display_interval = display_interval
    
    def world_post_scenario_build(self):
        self.fig = plt.figure(figsize=(6, 6), facecolor='black',
                              edgecolor='black', frameon=True)
        self.ax = plt.axes(facecolor='black', frameon=False, xticks=[],
                           yticks=[], aspect='equal')

        minx = min(site.geolocation.x for site in world.sites)
        maxx = max(site.geolocation.x for site in world.sites)
        miny = min(site.geolocation.y for site in world.sites)
        maxy = max(site.geolocation.y for site in world.sites)
        dx = (maxx - minx) * 0.05
        dy = (maxy - miny) * 0.05
        self.ax.set_xlim(minx - dx, maxx + dx)
        self.ax.set_ylim(miny - dy, maxy + dy)

        self.sites_props = {}
        all_site_types = set()
        for site in world.sites:
            site_type = site.__class__.__name__
            all_site_types.add(site_type)
            self.sites_props[site] = {
                'site_type': site_type,
                'patch': None
            }
        all_site_types = list(all_site_types)

        # TODO: this is temporary! it makes `all_site_types` be in a nicer order
        all_site_types = ['HouseholdSite', 'WorkplaceSite', 'SchoolSite', 'HubSite']

        PatchProps = namedtuple('PatchProps', ['patch_class', 'kwargs', 'size_kwargs'])
        patch_props = [
            PatchProps(
                patch_class=Circle,
                kwargs={},
                size_kwargs=lambda area: {'radius': sqrt(area / 3.14) * 3}
            ),
            PatchProps(
                patch_class=Rectangle,
                kwargs={},
                size_kwargs=lambda area: {
                    'width': sqrt(area) * 3,
                    'height': sqrt(area) * 3,
                }
            ),
            PatchProps(
                patch_class=RegularPolygon,
                kwargs={
                    'numVertices': 3,
                    'orientation': 0
                },
                size_kwargs=lambda area: {'radius': sqrt(4 * area / (3 * sqrt(3))) * 3}
            ),
            PatchProps(
                patch_class=Rectangle,
                kwargs={},
                size_kwargs=lambda area: {
                    'width': sqrt(area) * 4 * 3,
                    'height': sqrt(area) / 4 * 3,
                }
            ),

        ]

        if len(all_site_types) > len(patch_props):
            raise RuntimeError('you need to define more patch props')

        for site in world.sites:
            patch_props_index = all_site_types.index(self.sites_props[site]['site_type'])
            patch = patch_props[patch_props_index].patch_class(
                xy=tuple(site.geolocation),
                linewidth=0.2,
                facecolor='white',
                edgecolor=(0.5, 0.5, 0.5, 1.0),
                alpha=0.8,
                axes=self.ax,
                **patch_props[patch_props_index].size_kwargs(site.area),
                **patch_props[patch_props_index].kwargs,
            )
            self.ax.add_artist(patch)
            self.sites_props[site]['patch'] = patch

        self.time_txt = plt.text(
            x=minx,
            y=maxy,
            s='',
            fontdict={
                'color': 'white',
                'size': 12
            }
        )

    def world_posttick(self):
        if world.current % self._display_interval == 0:
            self.update()

    def plot_connections_graph(logs, reset_pos=False, fig=None, ax=None):
        if fig is None:
            fig, ax = plt.subplots()
        ax.cla()

        con_list = [con for log in logs for con in log['connections']]
        g = [list(k) + [v] for k, v in Counter(con_list).items()]
        G = nx.Graph()
        G.add_nodes_from([p.uuid for p in world.people])
        G.add_weighted_edges_from(g)
        if reset_pos or not hasattr(plot_connections_graph, 'pos'):
            plot_connections_graph.pos = nx.spring_layout(G)  # positions for all nodes
        weights = np.array([abs(G[u][v]['weight']) for u, v in G.edges])
        weights = weights / weights.max()
        # plt.figure()

        s_nodes = [p.uuid for p in world.people if p.traits.immunity_degree == 0 and not p.traits.is_infected]
        i_nodes = [p.uuid for p in world.people if p.traits.is_infected]
        r_nodes = [p.uuid for p in world.people if p.traits.immunity_degree > 0 and not p.traits.is_infected]
        nx.draw_networkx_nodes(G, plot_connections_graph.pos, node_size=1,
                            nodelist=s_nodes, node_color='b')
        nx.draw_networkx_nodes(G, plot_connections_graph.pos, node_size=1,
                            nodelist=i_nodes, node_color='r')
        nx.draw_networkx_nodes(G, plot_connections_graph.pos, node_size=1,
                            nodelist=r_nodes, node_color='g')
        nx.draw_networkx_edges(G, plot_connections_graph.pos, width=weights)
        plt.draw()
        plt.pause(0.001)
        return fig, ax

    def update(self):
        self.time_txt.set_text(str(world.current_time))

        cmap = LinearSegmentedColormap.from_list('my_cmap', ['blue', 'red'])

        for site in world.sites:
            patch = self.sites_props[site]['patch']
            if len(site.people) == 0:
                patch.set_facecolor(None)
                patch.set_fill(False)
            else:
                infected = sum(
                    person.traits.is_infected for person in site.people)
                infected = infected / len(site.people)
                patch.set_fill(True)
                patch.set_facecolor(cmap(infected))
        plt.draw()
        plt.pause(0.001)