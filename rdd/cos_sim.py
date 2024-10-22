"""
Implement cosine similarity
"""
#    Copyright (C) 2004-2010 by
#    Hung-Hsuan Chen <hhchen@psu.edu>
#    All rights reserved.
#    BSD license.
#    NetworkX:http://networkx.lanl.gov/.
import networkx as nx
import pandas as pd
import numpy as np
from rdd.measures import *

__author__ = """Hung-Hsuan Chen (hhchen@psu.edu)"""
# __all__ = ['cosine']

def cosine(G, remove_neighbors=False, dump_process=False):
    """Return the cosine similarity between nodes
    Parameters
    -----------
    G : graph
        A NetworkX graph
    remove_neighbors: boolean
        if true, only return cosine similarity of non-neighbor nodes
    dump_process: boolean
        if true, the calculation process is dumped
    Returns
    -------
    cosine: dictionary of dictionary of double
        if cosine[i][j] = k, this means the cosine similarity
        between node i and node j is k
    Examples
    --------
    >>> G=nx.Graph()
    >>> G.add_edges_from([(0,7), (0,1), (0,2), (0,3), (1,4), (2,4), (3,4), (4,5), (4,6)])
    >>> networkx_addon.similarity.cosine(G)
    Notes
    -----
    References
    ----------
    """
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("cosine() not defined for graphs with multiedges.")

    if G.is_directed():
        raise Exception("cosine() not defined for directed graphs.")

    cos = { }
    total_iter = G.number_of_nodes()
    for i, a in enumerate(G.nodes()):
        if dump_process:
            print(i+1, '/', total_iter)
        for b in G.neighbors(a):
            for c in G.neighbors(b):
                if a == c:
                    continue
                if remove_neighbors and c in G.neighbors(a):
                    continue
                s1 = set(G.neighbors(a))
                s2 = set(G.neighbors(c))
                if a not in cos:
                    cos[a] = { }
                cos[a][c] = float(len(s1 & s2)) / (len(s1) + len(s2))

    return cos

def get_cosine(G, u):
    sims = cosine(G)

    my_nodes = []
    my_degree = []
    my_sims = []
    
    for i in sims:
        my_nodes.append(i)
        my_degree.append(G.degree(i))
    
    for node in my_nodes:
        if node == u:
            my_sims.append(1)
            continue

        if sims[u].get(node) != None:
            my_sims.append(sims[u][node])
        else:
            my_sims.append(0)
    
    d = {'node_name': my_nodes, 'degree': my_degree, 'cos_sim': my_sims}
    df = pd.DataFrame(d)
    
    # df['cos_sim'] = (1-df['cos_sim'])
    # df['cos_sim'] = normalize_rdd(df, 1, 1000, 'cos_sim')
    # df['cos_sim'] = np.log(df['cos_sim'])

    return df

def get_cosine_radius(G, u, r):
    real_paths1 = nx.single_source_shortest_path(G, u, r)
    g = G.subgraph(list(real_paths1.keys()))

    sims = cosine(g)

    my_nodes = []
    my_degree = []
    my_sims = []
    
    for i in sims:
        my_nodes.append(i)
        my_degree.append(G.degree(i))
    
    for node in my_nodes:
        if node == u:
            my_sims.append(1)
            continue

        if sims[u].get(node) != None:
            my_sims.append(sims[u][node])
        else:
            my_sims.append(0)
    
    d = {'node_name': my_nodes, 'degree': my_degree, 'cos_sim': my_sims}
    df = pd.DataFrame(d)
    
    # df['cos_sim'] = (1-df['cos_sim'])
    df['cos_sim'] = normalize_rdd(df, 1, 1000, 'cos_sim')
    df['cos_sim'] = np.log(df['cos_sim'])

    return df
    
