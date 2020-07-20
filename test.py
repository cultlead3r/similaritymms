# test.py

from Node import Node
from RDD import *
import measures
from measures import *


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
    (5,6)
])


# for i in range(1,7):
#    for j in range(1,7):
#         print(f'Radial distribution distance: {i} and {j}: ', realworld_distance_compare_no_measure_finding(g1, i, j, measures.triangles, 4),
#                     realworld_distance_compare_no_measure_finding(g1, i, j, measures.local_degree_measure, 4), 
#                     realworld_distance_compare_no_measure_finding(g1, i, j, measures.global_degree_measure, 4))

print(realworld_distance_compare_no_measure_finding(g1, 1, 5, measures.local_clique, 4))
