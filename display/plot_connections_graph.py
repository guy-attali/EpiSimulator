import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

from core.world import world


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
