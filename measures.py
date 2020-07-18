"""Measure functions.

This module contains functions to be passed into the RDD comparison function.
They need to return lists of numbers representing values for each node.

"""


import networkx as nx
from RDD import *


def triangles(network, node_list):
    measures = list(nx.triangles(network).values())
    return measures
    

def realworld_distance_compare_no_measure_finding(network, u, v, measure, radius, network2=None):
    """Compares the radial distribution distance between two nodes in a single or two graphs.

    Args
    ----
        network: a networkx Graph object
        u: an instance of our Node class #  gets converted to string to match nx.Graph
        v: an instance of our Node class #  gets converted to string to match nx.Graph
        measure: a function that returns a list of values representing measures for each node
        radius: the maximum radius we want to compare with
        network2=None: Used if node v is from a different graph
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
        measures_v = measure(network2, node_list2, network2)
    else:
        measures_v = measure(network, node_list2)


    # # get the list of degrees from the main graph for each node in our sub_graph / list of nodes
    # # measures1 = global_degree_measure(network, node_list1)
    # # measures2 = global_degree_measure(network, node_list2)
    # measures1 = list(nx.triangles(g1).values())
    # measures2 = list(nx.triangles(g2).values())


    # take the list of degrees and set the appropriate field in all the Node objects in the list
    add_measures_to_node(node_list1, measures_u)
    add_measures_to_node(node_list2, measures_v)

    # gets the cumulative radial distributions for every radius up to threshhold
    cRD1 = get_CRD(node_list1)
    cRD2 = get_CRD(node_list2)
    
    # each radial distribution must go up to the same threshhold
    ensure_radial_parity(cRD1, cRD2)

    return get_rdd(cRD1,cRD2)