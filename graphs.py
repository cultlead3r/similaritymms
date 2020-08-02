import networkx as nx
from Node import Node
from RDD import *
import measures
from measures import *
from visualize import visualize_rdd

g1, g2 = nx.Graph(), nx.Graph()
g1.add_edges_from([
    (0, 5),
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

real_network2 = nx.read_adjlist("data/facebook_combined.txt", nodetype=int)
real_paths1 = nx.single_source_shortest_path(real_network2, 1, 4)
node_list1 = populate_node_list(real_paths1)
list_of_nodes = []
for node in node_list1:
    list_of_nodes.append(node.name)
subgraph = nodes_to_graph(real_network2, list_of_nodes)

real_paths2 = nx.single_source_shortest_path(subgraph, 1, 4)

df = get_rdds_for_visuals(subgraph, 1, measures.local_path_degree, 4)
#print(df)
    