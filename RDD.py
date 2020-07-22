"""Radial Distribution Distance functions.

This module contains helper functions used in calculating
Radial Distribution Distance (RDD) in networks.
"""


from collections import defaultdict
from Node import Node
import networkx as nx
import math
import matplotlib.pyplot as plt


def populate_node_list(shortest_paths):
    """Populate a list of nodes from a shortest_path dict
    
    Takes input typically from nx.single_source_shortest_path()
    Returns a list of Node objects
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
    """Add measures to node_list
    
    Takes a list of Node objects and list of measure values
    """
    for i, n in enumerate(list_of_nodes):
        n.measure = measures[n.name - 1]


def get_CRD(list_of_nodes):
    """Calculate Cumulative Radial Distributions
    
    Args:
    ------
        list_of_nodes : list of Node objects
    
    Returns:
    --------
        M: a defaultdict radius->radial distribution
    """
    M = defaultdict(int)
    for n in list_of_nodes:
        M[n.radius] += n.measure
    for i in range(len(M) - 1):
        M[i + 1] += M[i]
    return M


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


def get_CRD_union(crd1, crd2):
    """Takes two dictionaries and returns the union of their keys in a list"""
    union = set(crd1.keys()).union(set(crd2.keys()))
    return list(union)

def rdd_log_scale(rDD, r, crd1,crd2):
    """Creates a sumation log scale for our rdd"""
    sum = 0
    for i in range(r):
        i=i+1
        sum = sum + 1/i
    rDD = rDD + math.log(math.exp(-r))*abs(crd1[r] - crd2[r])

    return rDD

def rdd_default_scale(rDD, r, crd1,crd2):
    """Creates a sumation log scale for our rdd"""

    rDD = rDD + math.exp(-r)*abs(crd1[r] - crd2[r])

    return rDD



def get_rdd(crd1, crd2):
    """Get the radial distribution distance for two CRDs
    
    Takes two cumulative radial distribution dictionaries as arguments.
    Returns a radial distribution distance float
    """

    CRD = get_CRD_union(crd1, crd2)
    rDD = 0
    for r in CRD:
        #r goes from 0 to 3 when radius 4 to indicate a open circle(nodes on edge of circle are not encluded).
        #This might be a problem if the paper calls for a closed circle(i.e. r should go from 1or0 to 4).
        #!!!!CHECK LATER!!!!!
        rDD = rdd_default_scale(rDD, r, crd1, crd2)
    return rDD


def realworld_distance_compare(network, first, second, radius, network2=None):
    """Compares the radial distribution distance between two nodes in a single or two graphs.

    Args:
    -----
        network: a networkx Graph object
        first: an instance of our Node class #  gets converted to string to match nx.Graph
        second: an instance of our Node class #  gets converted to string to match nx.Graph
        radius: the maximum radius we want to compare with

    Returns:
    -------
        A float representing the radial distribution distance difference.
    """
    # Get the shortest paths for each node up to the specified radius
    real_paths1 = nx.single_source_shortest_path(network, first, radius)
    if network2:
        real_paths2 = nx.single_source_shortest_path(network2, second, radius)
    else:
        real_paths2 = nx.single_source_shortest_path(network, second, radius)
    
    # Create a list of Node objects from our shortest paths lists
    node_list1 = populate_node_list(real_paths1)
    node_list2 = populate_node_list(real_paths2)

    # get the list of degrees from the main graph for each node in our sub_graph / list of nodes
    measures1 = global_degree(network, node_list1)
    if network2:
        measures2 = global_degree(network2, node_list2)
    else:
        measures2 = global_degree(network, node_list2)

    # take the list of degrees and set the appropriate field in all the Node objects in the list
    add_measures_to_node(node_list1, measures1)
    add_measures_to_node(node_list2, measures2)

    # gets the cumulative radial distributions for every radius up to threshhold
    cRD1 = get_CRD(node_list1)
    cRD2 = get_CRD(node_list2)
    
    # each radial distribution must go up to the same threshhold
    ensure_radial_parity(cRD1, cRD2)

    return get_rdd(cRD1,cRD2)


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
        count = 0
        for num in given_paths[path]:
            if(count == 0):
                sec = num
            if (count > 0):
                fir = sec
                sec = num
                adj_list.append((fir, sec))
            count+=1

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
