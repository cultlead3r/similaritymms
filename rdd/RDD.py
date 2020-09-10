"""Radial Distribution Distance functions.

This module contains helper functions used in calculating
Radial Distribution Distance (RDD) in networks.
"""


from collections import defaultdict
from rdd.Node import Node
import networkx as nx
import math
import pandas as pd
import numpy as np
import numpy.linalg as la


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
    crd1_length, crd2_length = len(crd1), len(crd2)
    if len(crd1) > len(crd2):
        length_difference = len(crd1) - len(crd2)
        for i in range(length_difference):
            crd2[crd2_length + i] = crd2[crd2_length - 1]
    elif len(crd2) > len(crd1):
        length_difference = len(crd2) - len(crd1)
        for i in range(length_difference):
            crd1[crd1_length + i] = crd1[crd1_length - 1]


# TODO Make this the union and get rid of the shit above
def get_crd_union(crd1, crd2):
    """Takes two dictionaries and returns the union of their keys in a list"""
    union = set(crd1.keys()).union(set(crd2.keys()))
    return list(union)


def rdd_default_scale(rdd, r, crd1, crd2):
    """Creates a summation log scale for our rdd"""
    rdd = rdd + math.exp(-r) * abs(crd1[r] - crd2[r])
    return rdd


def get_rdd(crd1, crd2):
    """Get the radial distribution distance for two CRDs"""
    crd = get_crd_union(crd1, crd2)
    r_dd = 0
    for r in crd:
        r_dd = rdd_default_scale(r_dd, r, crd1, crd2)
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


def realworld_distance_compare(network, u, v, measure, radius, network2=None):
    """Compares the radial distribution distance between two nodes in a single or two graphs.

    Args
    ----
        network: a networkx Graph object
        u: an instance of our Node class #  gets converted to string to match nx.Graph
        v: an instance of our Node class #  gets converted to string to match nx.Graph
        measure: a function that returns a list of values representing measures for each node
        radius: the maximum radius we want to compare with
        network2: Used if node v is from a different graph

    Returns:
    --------
        radial distribution distance value of u compared to v

    """
    # Get the shortest paths for each node up to the specified radius
    real_paths1 = nx.single_source_shortest_path(network, u, radius)
    if network2:
        real_paths2 = nx.single_source_shortest_path(network2, v, radius)
    else:
        real_paths2 = nx.single_source_shortest_path(network, v, radius)

    # Create a list of Node objects from our shortest paths lists
    node_list1 = populate_node_list(real_paths1)
    node_list2 = populate_node_list(real_paths2)

    measures_u = measure(network, node_list1)
    if network2:
        measures_v = measure(network2, node_list2)
    else:
        measures_v = measure(network, node_list2)

    # take the list of degrees and set the appropriate field in all the Node objects in the list
    add_measures_to_node(node_list1, measures_u)
    add_measures_to_node(node_list2, measures_v)

    # gets the cumulative radial distributions for every radius up to threshold
    crd1 = get_crd(node_list1)
    crd2 = get_crd(node_list2)

    # each radial distribution must go up to the same threshold
    ensure_radial_parity(crd1, crd2)
    return get_rdd(crd1, crd2)


def get_rdds_for_visuals(network, u, measure, radius):
    """
    Args:
        network: a networkx Graph object
        u: Node object from which the other nodes will be considered up to radius
        measure: measures to be used that influence RDD values
        radius: how many steps from root node to consider

    Returns:
        df: pandas dataframe of nodes and information

    """
    rdd_list = []
    node_list = []
    rad_list = []
    degree_list = []

    # Populate the lists used to construct dataframe of information from nodes
    for node in network:
        r = realworld_distance_compare(network, u, node, measure, radius)
        if r == 0:
            rdd_list.append(0)
        else:
            # rdd_list.append(math.log(r, 10))
            # rdd_list.append(np.tanh(r))
            rdd_list.append(r)

        # TODO Fix this - rad_list is broken - adding 1 just to make it work
        # rad_list.append(len(shortest_paths[node]) - 1)
        rad_list.append(1)

        node_list.append(node)
        degree_list.append(network.degree(node))
    d = {'node_name': node_list, 'rdd': rdd_list, 'radius': rad_list, 'degree': degree_list}
    df = pd.DataFrame(d)

    # df['rdd'] = normalize_rdd(df, 1, 1000, 'rdd')
    df['rdd'] = np.log10(df['rdd'])
    df['rdd'] = np.tanh(df['rdd'])

    return df


def get_rdds_for_visuals_vector(network, u, measure_vector, radius):
    node_list = []
    degree_list = []
    rad_list = []

    # Populate and construct a DataFrame with basic node information
    for node in network:
        node_list.append(node)
        degree_list.append(network.degree(node))
        # TODO: Broken
        rad_list.append(1)
    df = pd.DataFrame({'node_name': node_list, 'radius': rad_list, 'degree': degree_list})

    # Now iterate through the measures and add them as columns to the frame
    measure_lists = []
    for m in measure_vector:
        rdd_list = []
        for node in network:
            r = realworld_distance_compare(network, u, node, m, radius)
            rdd_list.append(r)
        # we use __name__ to get the string name of the function
        df[m.__name__] = rdd_list
        measure_lists.append(rdd_list)

    # for m in measure_vector:
    # df[m.__name__] = normalize_rdd(df, 1, 1000, m.__name__)
    # df[m.__name__] = np.log10(df[m.__name__])
    df_norm = df[list(map(lambda f: f.__name__, measure_vector))]
    df['normalized_rdd'] = la.norm(df_norm, axis=1)
    df['normalized_rdd'] = normalize_rdd(df, 1, 1000, 'normalized_rdd')
    # df['normalized_rdd'] = np.log10(df['normalized_rdd'])
    return df

def get_rdds_for_visuals_vector_radius(network, u, measure_vector, radius):
    node_list = []
    degree_list = []
    rad_list = []

    real_paths1 = nx.single_source_shortest_path(network, u, radius)

    network = network.subgraph(list(real_paths1.keys()))

    # Populate and construct a DataFrame with basic node information
    for node in network:
        node_list.append(node)
        degree_list.append(network.degree(node))
        # TODO: Broken
        rad_list.append(1)
    df = pd.DataFrame({'node_name': node_list, 'radius': rad_list, 'degree': degree_list})

    # Now iterate through the measures and add them as columns to the frame
    measure_lists = []
    for m in measure_vector:
        rdd_list = []
        for node in network:
            r = realworld_distance_compare(network, u, node, m, radius)
            rdd_list.append(r)
        # we use __name__ to get the string name of the function
        df[m.__name__] = rdd_list
        measure_lists.append(rdd_list)

    # for m in measure_vector:
    # df[m.__name__] = normalize_rdd(df, 1, 1000, m.__name__)
    # df[m.__name__] = np.log10(df[m.__name__])
    df_norm = df[list(map(lambda f: f.__name__, measure_vector))]
    df['normalized_rdd'] = la.norm(df_norm, axis=1)
    # df['normalized_rdd'] = normalize_rdd(df, 1, 1000, 'normalized_rdd')
    # df['normalized_rdd'] = np.log10(df['normalized_rdd'])
    return df

def normalize_rdd(df, d_min, d_max, col):
    r_min = df[col].min()
    r_max = df[col].max()
    t_min = d_min
    t_max = d_max

    return ((df[col] - r_min) / (r_max - r_min)) * (t_max - t_min) + t_min


# TODO: Not working yet
def get_rdds_for_visuals_diff_graph(network, u, measure, radius, network2):
    shortest_paths = nx.single_source_shortest_path(network, u, radius)
    rdd_list = []
    node_list = []
    rad_list = []
    # used for single graph. Add multigraph later.
    for node in network:
        rdd_list.append(realworld_distance_compare(network, u, node, measure, radius))
        rad_list.append(len(shortest_paths[node]) - 1)
        node_list.append(node)

    d = {'node_name': node_list, 'rdd': rdd_list, 'radius': rad_list}
    df = pd.DataFrame(d)
    return df