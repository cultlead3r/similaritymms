"""Measure functions.

This module contains functions to be passed into the RDD comparison function.
They need to return lists of numbers representing values for each node.

"""


from rdd.RDD import *


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

    local_graph = paths_to_graph(
        nx.single_source_shortest_path(network, target_node, largest_rad))

    for node in node_list:
        # if local_graph.degree[node.name] > 1:
        # print(f'Name : {node.name} Degree: {local_graph.degree[node.name]}')
        measures.append(local_graph.degree[node.name])

    return measures


def global_graph_triangles(network, node_list):
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
    triangle_dic = nx.triangles(network)
    for node in node_list:
        measures.append(triangle_dic[node.name])

    return measures


def local_graph_triangles(network, node_list):
    """

    Args:
        network: NetworkX Graph object
        node_list: list of nodes for which we want the number of triangles

    Returns:
        measures: list of how many triangles each node is a part of

    """
    measures = []
    list_of_nodes = []
    for node in node_list:
        list_of_nodes.append(node.name)

    local_graph = nodes_to_graph(network, list_of_nodes)

    triangle_dic = nx.triangles(local_graph)
    for node in node_list:
        measures.append(triangle_dic[node.name])

    return measures


def local_path_triangles(network, node_list):
    """

    Args:
        network: NetworkX Graph object
        node_list: list of nodes for which we want the number of triangles

    Returns:
        measures: list of how many triangles each node is a part of

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

    local_graph = paths_to_graph(
        nx.single_source_shortest_path(network, target_node, largest_rad))
    triangle_dic = nx.triangles(local_graph)
    for node in node_list:
        measures.append(triangle_dic[node.name])

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
        cliques = nx.algorithms.clique.cliques_containing_node(
            network, node.name)
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
        cliques = nx.algorithms.clique.cliques_containing_node(
            local_graph, node.name)
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

    local_graph = paths_to_graph(
        nx.single_source_shortest_path(network, target_node, largest_rad))

    for node in node_list:
        # if local_graph.degree[node.name] > 1:
        # print(f'Name : {node.name} Degree: {local_graph.degree[node.name]}')
        cliques = nx.algorithms.clique.cliques_containing_node(
            local_graph, node.name)
        measures.append(len(cliques))

    return measures


def global_graph_katz_centrality(network, node_list):
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
    katz_dic = nx.katz_centrality(network)
    for node in node_list:
        measures.append(katz_dic[node.name])

    return measures


def local_graph_katz_centrality(network, node_list):
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

    katz_dic = nx.katz_centrality(local_graph)
    for node in node_list:
        measures.append(katz_dic[node.name])

    return measures


def local_path_katz_centrality(network, node_list):
    """

    Args:
        network: NetworkX Graph object
        node_list: list of nodes for which we want the number of triangles

    Returns:
        measures: list of how many triangles each node is a part of

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

    local_graph = paths_to_graph(
        nx.single_source_shortest_path(network, target_node, largest_rad))

    katz_dic = nx.katz_centrality(local_graph)
    for node in node_list:
        measures.append(katz_dic[node.name])

    return measures


def global_graph_harmonic_centrality(network, node_list):
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
    harmonic_dic = nx.harmonic_centrality(network)
    for node in node_list:
        measures.append(harmonic_dic[node.name])

    return measures


def local_graph_harmonic_centrality(network, node_list):
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

    harmonic_dic = nx.harmonic_centrality(local_graph)
    for node in node_list:
        measures.append(harmonic_dic[node.name])

    return measures


def local_path_harmonic_centrality(network, node_list):
    """

    Args:
        network: NetworkX Graph object
        node_list: list of nodes for which we want the number of triangles

    Returns:
        measures: list of how many triangles each node is a part of

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

    local_graph = paths_to_graph(
        nx.single_source_shortest_path(network, target_node, largest_rad))

    harmonic_dic = nx.harmonic_centrality(local_graph)
    for node in node_list:
        measures.append(harmonic_dic[node.name])

    return measures


def global_graph_pagerank(network, node_list):
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
    pagerank_dic = nx.pagerank(network, max_iter=1000)
    for node in node_list:
        measures.append(pagerank_dic[node.name])

    return measures


def local_graph_pagerank(network, node_list):
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

    pagerank_dic = nx.pagerank(local_graph, max_iter=1000)
    for node in node_list:
        measures.append(pagerank_dic[node.name])

    return measures


def local_path_pagerank(network, node_list):
    """

    Args:
        network: NetworkX Graph object
        node_list: list of nodes for which we want the number of triangles

    Returns:
        measures: list of how many triangles each node is a part of

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

    local_graph = paths_to_graph(
        nx.single_source_shortest_path(network, target_node, largest_rad))

    pagerank_dic = nx.pagerank(local_graph, max_iter=1000)
    for node in node_list:
        measures.append(pagerank_dic[node.name])

    return measures


def global_graph_morgan_index(target_network, node_list, target_iterations=8):
    network = target_network.copy()
    for iteration in range(target_iterations):
        new_measures = []
        for node in network:
            if(iteration == 0):
                network.nodes[node]['measure'] = 1
            else:
                neighbors = list(network.neighbors(node))
                total_new_measure = 0

                for neighbor in neighbors:
                    total_new_measure = total_new_measure + \
                        network.nodes[neighbor]['measure']

                new_measures.append(total_new_measure)

                # print(neighbors)

        # print(new_measures)

        if(iteration != 0):
            count = 0
            for node in network:
                network.nodes[node]['measure'] = new_measures[count]
                # print(network.nodes[node]['measure'])
                count = count+1

    # returning_measures = []
    # for node in network:
    #     returning_measures.append(network.nodes[node]['measure'])

    returning_measures = []
    for node in node_list:
        returning_measures.append(network.nodes[node.name]['measure'])

    return returning_measures

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
