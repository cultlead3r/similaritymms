"""Measure functions.

This module contains functions to be passed into the RDD comparison function.
They need to return lists of numbers representing values for each node.

"""


from RDD import *
import pandas as pd


def global_graph_degree(network, node_list):
    """Creates a list of degree of all nodes from main/global graph

    Args:
    -----
        network: main/global graph
        node_list: list of Node objects in our graph of set radius

    Returns:
    --------
        measures: a list of global degrees for each node in graph / node list

    """
    measures = []
    for node in node_list:
        measures.append(network.degree[node.name])
    
    return measures


def local_graph_degree(network, node_list):
    """Creates a list of degree of all nodes from root to given radius

    Args:
        network: NetworkX Graph object
        node_list: list of Node objects used for RDD

    Returns:
        measures: list of degrees created by local graph of given radius

    """

    measures = []
    list_of_nodes = []
    for node in node_list:
        list_of_nodes.append(node.name)

    local_graph = nodes_to_graph(network, list_of_nodes)

    for node in node_list:
        measures.append(local_graph.degree[node.name])
    
    return measures


def local_path_degree(network, node_list):
    """Creates a list of degrees given

    Args:
        network: NetworkX Graph object
        node_list: list of Node objects used for RDD

    Returns:
        measures: list of degrees created by graph made of shortest paths

    """
    measures = []
    largest_rad = -1
    target_node = -1
    
    for node in node_list:
        # find largest radius
        if node.radius >= largest_rad:
            largest_rad = node.radius
        
        if node.radius == 0:
            target_node = node.name
    
    local_graph = paths_to_graph(nx.single_source_shortest_path(network, target_node, largest_rad))
    
    for node in node_list:
        # if local_graph.degree[node.name] > 1:
        # print(f'Name : {node.name} Degree: {local_graph.degree[node.name]}')
        measures.append(local_graph.degree[node.name])
    
    return measures


def triangles(network, node_list):
    """

    Args:
        network: NetworkX Graph object
        node_list: list of nodes for which we want the number of triangles

    Returns:
        measures: list of how many triangles each node is a part of

    """
    measures = list(nx.triangles(network).values())
    return measures


def global_graph_clique(network, node_list):
    """Creates a list containing the number of cliques each node is apart of.

    Args:
    -----
        network: main/global graph
        node_list: list of nodes in our graph

    Returns:
    --------
        measures: a list of global cliques for each node in node list

    """
    measures = []
    for node in node_list:
        cliques = nx.algorithms.clique.cliques_containing_node(network, node.name)
        measures.append(len(cliques))
    
    return measures


def local_graph_clique(network, node_list):
    """Creates a list containing the number of cliques each node is apart of.

    Args:
    -----
        network: main/global graph
        node_list: list of nodes in our local graph / subgraph of set radius

    Returns:
    --------
        a list of local cliques for each node in node list

    """
    measures = []
    list_of_nodes = []
    for node in node_list:
        list_of_nodes.append(node.name)

    local_graph = nodes_to_graph(network, list_of_nodes)

    for node in node_list:
        cliques = nx.algorithms.clique.cliques_containing_node(local_graph, node.name)
        measures.append(len(cliques))
    
    return measures


def local_path_clique(network, node_list):
    measures = []
    largest_rad = -1
    target_node = -1
    
    for node in node_list:
        if node.radius >= largest_rad:
            largest_rad = node.radius
        
        if node.radius == 0:
            target_node = node.name

    local_graph = paths_to_graph(nx.single_source_shortest_path(network, target_node, largest_rad))

    for node in node_list:
        # if local_graph.degree[node.name] > 1:
        # print(f'Name : {node.name} Degree: {local_graph.degree[node.name]}')
        cliques = nx.algorithms.clique.cliques_containing_node(local_graph, node.name)
        measures.append(len(cliques))
    
    return measures

# TODO: Implement

# def global_graph_basis_cycles(network, node_list):
#     """Creates a list containing the number of base cycles each node is apart of.

#     Args:
#     -----
#         network: main/global graph
#         node_list: list of nodes in our local graph / subgraph of set radius

#     Returns:
#     --------
#         a list of global cycles for each node in node list"""
#     measures = []
#     for node in node_list:
#         Note Working RN
#         cycles = nx.find_cycle(network, node.name)
#         measures.append(len(cycles))
    
#     return measures


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
            rdd_list.append(math.log(r, 10))

        # TODO Fix this - rad_list is broken - adding 1 just to make it work
        # rad_list.append(len(shortest_paths[node]) - 1)
        rad_list.append(1)

        node_list.append(node)
        degree_list.append(network.degree(node))
    d = {'node_name': node_list, 'rdd': rdd_list, 'radius': rad_list, 'degree': degree_list}
    df = pd.DataFrame(d)
    return df     


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

  
# def realworld_distance_compare_for_visual(network, u, v, measure, radius, network2=None):
#     """Compares the radial distribution distance between two nodes in a single or two graphs.
#
#     Args
#     ----
#         network: a networkx Graph object
#         u: an instance of our Node class #  gets converted to string to match nx.Graph
#         v: an instance of our Node class #  gets converted to string to match nx.Graph
#         measure: a function that returns a list of values representing measures for each node
#         radius: the maximum radius we want to compare with
#         network2=None: Used if node v is from a different graph
#     """
#     # Get the shortest paths for each node up to the specified radius
#     real_paths1 = nx.single_source_shortest_path(network, u, radius)
#     if network2:
#         real_paths2 = nx.single_source_shortest_path(network2, v, radius)
#     else:
#         real_paths2 = nx.single_source_shortest_path(network, v, radius)
#
#     # Create a list of Node objects from our shortest paths lists
#     node_list1 = populate_node_list(real_paths1)
#     node_list2 = populate_node_list(real_paths2)
#
#     measures_u = measure(network, node_list1)
#     if network2:
#         measures_v = measure(network2, node_list2)
#     else:
#         measures_v = measure(network, node_list2)
#
#     # take the list of degrees and set the appropriate field in all the Node objects in the list
#     add_measures_to_node(node_list1, measures_u)
#     add_measures_to_node(node_list2, measures_v)
#
#     # for node in node_list1:
#     #     print(f'{node.name}, {node.measure}')
#
#     # for node in node_list2:
#     #     print(f'{node.name}, {node.measure}')
#
#
#     # gets the cumulative radial distributions for every radius up to threshhold
#     cRD1 = get_crd(node_list1)
#     cRD2 = get_crd(node_list2)
#
#     # each radial distribution must go up to the same threshhold
#     ensure_radial_parity(cRD1, cRD2)
#
#     return get_rdd(cRD1, cRD2, node_list1, node_list2)
