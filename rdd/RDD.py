"""Radial Distribution Distance functions.

This module contains helper functions used in calculating
Radial Distribution Distance (RDD) in networks.
"""


from collections import defaultdict
from rdd.Node import Node
import networkx as nx
import math


def populate_node_list(shortest_paths):
    """Creates list of Node objects from list of shortest paths

    Args:
        shortest_paths: Dictionary of nodes and path from root to radius

    Returns:
        node_list: list of Node objects with information added

    """
    node_list = []
    for node in shortest_paths:
        n = Node()
        n.name = node
        n.path = shortest_paths[node]
        n.radius = len(shortest_paths[node]) - 1
        node_list.append(n)
    return node_list

        
def add_measures(list_of_nodes, measures):
    """Add measures to node list

    Args:
        list_of_nodes: list of Node objects
        measures:

    Returns:

    """
    for i, n in enumerate(list_of_nodes):
        n.measure = measures[n.name - 1]


def get_crd(list_of_nodes):
    """Calculate Cumulative Radial Distributions
    
    Args:
    ------
        list_of_nodes : list of Node objects
    
    Returns:
    --------
        m: a defaultdict radius->radial distribution
    """
    m = defaultdict(int)
    for n in list_of_nodes:
        m[n.radius] += n.measure
    for i in range(len(m) - 1):
        m[i + 1] += m[i]
    return m


def ensure_radial_parity(crd1, crd2):
    """Make sure both CRDs have the same maximum radius value"""
    if len(crd1) > len(crd2):
        length_difference = len(crd1) - len(crd2)
        for i in range(length_difference):
            crd2[len(crd2)+i] = crd2[len(crd2) - 1]
    elif len(crd2) > len(crd1): 
        length_difference = len(crd2) - len(crd1)
        for i in range(length_difference):
            crd1[len(crd1)+i] = crd1[len(crd1) - 1]


# TODO Make this the union and get rid of the shit above
def get_crd_union(crd1, crd2):
    """Takes two dictionaries and returns the union of their keys in a list"""
    union = set(crd1.keys()).union(set(crd2.keys()))
    return list(union)


def rdd_default_scale(rdd, r, crd1, crd2):
    """Creates a sumation log scale for our rdd"""
    rdd = rdd + math.exp(-r) * abs(crd1[r] - crd2[r])

    return rdd


def get_rdd(crd1, crd2):
    """Get the radial distribution distance for two CRDs
    
    Takes two cumulative radial distribution dictionaries as arguments.
    Returns a radial distribution distance float
    """

    crd = get_crd_union(crd1, crd2)
    r_dd = 0
    for r in crd:
        # if r == 0:
        #     continue
        # r goes from 0 to 3 when radius 4 to indicate a open circle(nodes on edge of circle are not encluded).
        # This might be a problem if the paper calls for a closed circle(i.e. r should go from 1or0 to 4).
        # !!!!CHECK LATER!!!!!
        r_dd = rdd_default_scale(r_dd, r, crd1, crd2)
        # r_dd = r_dd + math.exp(-r)*abs(crd1[r] - crd2[r])
    return r_dd


def add_measures_to_node(list_nodes, measures):
    """Populates the measure field for each Node in a list of Node objects

    Args:
    ------
        list_nodes : list of Node objects
        measures : list of values (floats)
    """
    for i in range(len(measures)):
        list_nodes[i].measure = measures[i]


def paths_to_graph(given_paths):
    """Takes a list of paths of under the given radius and creates a nx.Graph instance of the local/subgraph

    Args:
    ------
        given_paths: list of paths from nx.single_source_shortest_path()

    Returns:
    -------
        g: An nx.Graph() object.
    """
    adj_list = []
    for path in given_paths:
        sec = 0
        count = 0
        for num in given_paths[path]:
            if count == 0:
                sec = num
            if count > 0:
                fir = sec
                sec = num
                adj_list.append((fir, sec))
            count += 1

    adj_list = list(dict.fromkeys(adj_list))
    g = nx.Graph()
    g.add_edges_from(adj_list)

    return g


def nodes_to_graph(network, node_list):
    """Takes the global network and a list of nodes then returns a subgraph with the specified nodes.

    Args:
    -----
        network: global graph, nx graph
        node_list: A list of nodes for the subgraph
    
    Returns:
    --------
        g: The subgraph, nx.Graph() object.
    
    """
    g = network.subgraph(node_list)
    return g
