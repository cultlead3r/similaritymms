# test.py

from Node import Node
from RDD import *
import measures
from measures import *
from visualize import visualize_rdd

g1, g2 = nx.Graph(), nx.Graph()


g1.add_edges_from([
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 4),
    (3, 6),
    (4, 5),
])


g2.add_edges_from([
    (1,2),
    (2,4),
    (2,3),
  # (4,3),
    (3,5),
    (4,5),
    (5,6),
    (3,7)    
])


# for i in range(1,7):
#    for j in range(1,7):
#         print(f'Radial distribution distance: {i} and {j}: ', realworld_distance_compare(g1, i, j, measures.global_graph_degree, 2),
#                     realworld_distance_compare(g1, i, j, measures.local_graph_degree, 2),
#                     realworld_distance_compare(g1, i, j, measures.local_path_degree, 2))
# print(get_rdds_for_visuals(g1, 1, measures.local_path_degree, 4, g2))
# visualize_rdd(g1).show()

import networkx as nx
from Node import Node
from RDD import *
import measures
# from measures import *
# from visualize import visualize_rdd
#
real_network = nx.read_adjlist("data/facebook_combined2.txt", nodetype=int)
# fig = visualize_rdd(real_network)
# fig.show()


import networkx as nx
from Node import Node
from RDD import *
import measures
from measures import *
from visualize import visualize_rdd

real_network2 = nx.read_adjlist("data/facebook_combined.txt", nodetype=int)
real_paths1 = nx.single_source_shortest_path(real_network2, 1, 2)
node_list1 = populate_node_list(real_paths1)
list_of_nodes = []
for node in node_list1:
    list_of_nodes.append(node.name)
subgraph = nodes_to_graph(real_network2, list_of_nodes)
# subgraph.nodes
fig = visualize_rdd(subgraph)
fig.show()
# print("hi", subgraph)
# real_paths2 = nx.single_source_shortest_path(subgraph, 1, 4)