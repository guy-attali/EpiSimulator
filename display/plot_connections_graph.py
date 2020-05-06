import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from random import sample

from core.world import world


def plot_connections_graph(logs, s_nodes, i_nodes, r_nodes,
                           reset_pos=False, fig=None, ax=None, sample_ratio=1):
    if fig is None:
        fig, ax = plt.subplots()
    ax.cla()

    G = generate_graph(logs, sample_ratio=sample_ratio)

    if reset_pos or not hasattr(plot_connections_graph, 'pos'):
        plot_connections_graph.pos = nx.spring_layout(G)  # positions for all nodes
    weights = np.array([abs(G[u][v]['weight']) for u, v in G.edges])
    weights = weights / weights.max()
    weights = weights / weights.max()
    # s_nodes = [p.uuid for p in world.people if p.traits.immunity_degree == 0 and not p.traits.is_infected]
    # i_nodes = [p.uuid for p in world.people if p.traits.is_infected]
    # r_nodes = [p.uuid for p in world.people if p.traits.immunity_degree > 0 and not p.traits.is_infected]
    nx.draw_networkx_nodes(G, plot_connections_graph.pos, node_size=1,
                           nodelist=s_nodes, node_color='b')
    nx.draw_networkx_nodes(G, plot_connections_graph.pos, node_size=1,
                           nodelist=i_nodes, node_color='r')
    nx.draw_networkx_nodes(G, plot_connections_graph.pos, node_size=1,
                           nodelist=r_nodes, node_color='g')
    nx.draw_networkx_edges(G, plot_connections_graph.pos, width=weights)
    # plt.draw()
    # plt.pause(0.001)
    return fig, ax, plot_connections_graph.pos

    # plt.figure()


def generate_graph(logs, sample_ratio=1):
    con_list = [con for log in logs for con in log['connections']]
    con_list = sample(con_list, int(sample_ratio * len(con_list)))
    g = [list(k) + [v] for k, v in Counter(con_list).items()]
    G = nx.Graph()
    G.add_nodes_from([p.uuid for p in world.people])
    G.add_weighted_edges_from(g)
    return G


# def plot_nodes(pos, s_nodes, i_nodes, r_nodes):