import networkx as nx
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from rdd.measures import *
from rdd import RDD
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from sklearn_extra.cluster import KMedoids

def simrank(G, u):
    sim = nx.simrank_similarity(G, u)
    
    sim_list = []
    node_list = []
    degree_list = []

    for n in sim:
        sim_list.append(sim[n])
        node_list.append(n)
        degree_list.append(G.degree(n))

    d = {'node_name': node_list, 'degree': degree_list, 'simrank': sim_list}
    df = pd.DataFrame(d)

    # print(df)

    # df['simrank'] = normalize_rdd(df, 1, 1000, 'simrank')
    
    # df['simrank'] = np.log10(df['simrank'])
    
    # print(df)

    return df

def simrank_radius(G, u, r):
    
    real_paths1 = nx.single_source_shortest_path(G, u, r)

    g = G.subgraph(list(real_paths1.keys()))

    sim = nx.simrank_similarity(g, u)
    
    sim_list = []
    node_list = []
    degree_list = []

    for n in sim:
        sim_list.append(sim[n])
        node_list.append(n)
        degree_list.append(G.degree(n))

    d = {'node_name': node_list, 'degree': degree_list, 'simrank': sim_list}
    df = pd.DataFrame(d)

    # print(df)

    df['simrank'] = normalize_rdd(df, 1, 1000, 'simrank')
    df['simrank'] = np.log10(df['simrank'])
    
    # print(df)

    return df


def k_means(df, measure_vector, k=3):
    kmeans = KMeans(n_clusters=k) 
    
    feats = []
    for m in measure_vector:
        feats.append( m.__name__ )

    y = kmeans.fit_predict(df[['normalized_rdd']])

    df['cluster'] = y

    return df

def kmeans2(df, column, k):
    """Runs KMeans on a given DataFrame / column

    Args:
        df (DataFrame): DataFrame with column containing measures to cluster on
        column (str): Which column to use for clustering on
        k (int): Number of clusters

    Returns:
        DataFrame: Returns the DataFrame with a "cluster" column added. Warning! Modifies the DF in place!
    """
    km = KMeans(n_clusters=k)
    df['cluster'] = km.fit_predict(df[[column]])
    return df

def k_means_matrix(g, m, k):
    """Get the clustering information for kmeans clustering.

    Args:
        G (Graph): NetworkX Graph
        M (DataFrame): a matrix of similarity values
        k (int): number of clusters

    Returns:
        DataFrame: A DataFrame with node_name and cluster columns
    """
    np_of_values = np.array(m)
    kmeans = KMeans(n_clusters=k)
    cluster_data = kmeans.fit_predict(np_of_values)
    
    kmeans_results = pd.DataFrame({'node_name': g.nodes(),
                                    'cluster': cluster_data})
    return kmeans_results


def k_means_other(df, target_columns, k=3):
    kmeans = KMeans(n_clusters=k) 
    
    feats = target_columns
    
    y = kmeans.fit_predict(df[feats])

    df['k_mean_cluster'] = y

    return df

def k_means_matrix_clustering(g, r, measure, num_cluster):
    all_rdds_df = pd.DataFrame() 

    for target_one in g:
        rdd_list = []
        for target_two in g:
            rdd_list.append(RDD.realworld_distance_compare(g, target_one, target_two, measure[0], r))
        all_rdds_df[target_one] = rdd_list
    
    data = all_rdds_df
    np_of_rdds = np.array(data)
    kmeans = KMeans(n_clusters=num_cluster)
    cluster_data = kmeans.fit_predict(np_of_rdds)

    node_list = []
    degree_list = []
    rad_list = []
    # Populate and construct a DataFrame with basic node information
    for node in g:
        node_list.append(node)
        degree_list.append(g.degree(node))
        # TODO: Broken
        rad_list.append(1)
    
    df = pd.DataFrame({'node_name': node_list, 'radius': rad_list, 'degree': degree_list, 'cluster': cluster_data})

    return df

def mean_shift(df, measure_vector):
    mean_shi = MeanShift()
    
    feats = []
    for m in measure_vector:
        feats.append( m.__name__ )

    y = mean_shi.fit_predict(df[feats])

    df['cluster'] = y

    return df

def mean_shift_other(df, target_columns):
    mean_shi = MeanShift()
    
    feats = target_columns
    y = mean_shi.fit_predict(df[feats])

    df['cluster'] = y

    return df

def agglomerative_hierarchical_clustering(g, r, measure, num_cluster):
    all_rdds_df = pd.DataFrame() 

    for target_one in g:
        rdd_list = []
        for target_two in g:
            rdd_list.append(RDD.realworld_distance_compare(g, target_one, target_two, measure, r))
        all_rdds_df[target_one] = rdd_list
    
    data = all_rdds_df
    # dend = shc.dendrogram(shc.linkage(data, method='ward'))

    cluster = AgglomerativeClustering(n_clusters=num_cluster, affinity='euclidean', linkage='ward')
    cluster_data = cluster.fit_predict(data)

    node_list = []
    degree_list = []
    rad_list = []
    # Populate and construct a DataFrame with basic node information
    for node in g:
        node_list.append(node)
        degree_list.append(g.degree(node))
        # TODO: Broken
        rad_list.append(1)
    
    df = pd.DataFrame({'node_name': node_list, 'radius': rad_list, 'degree': degree_list, 'cluster': cluster_data})

    return df

def kmedoid_clustering(g, r, measure, num_cluster):
    all_rdds_df = pd.DataFrame() 

    for target_one in g:
        rdd_list = []
        for target_two in g:
            rdd_list.append(RDD.realworld_distance_compare(g, target_one, target_two, measure, r))
        all_rdds_df[target_one] = rdd_list
    
    data = all_rdds_df
    np_of_rdds = np.array(data)
    kmedoids = KMedoids(n_clusters=num_cluster, random_state=0).fit(np_of_rdds)
    cluster_data = kmedoids.labels_

    node_list = []
    degree_list = []
    rad_list = []
    # Populate and construct a DataFrame with basic node information
    for node in g:
        node_list.append(node)
        degree_list.append(g.degree(node))
        # TODO: Broken
        rad_list.append(1)
    
    df = pd.DataFrame({'node_name': node_list, 'radius': rad_list, 'degree': degree_list, 'cluster': cluster_data})

    return df

    
def kmedoid_clustering2(g, m, k):
    """Get the clustering information for KMedoid clustering.

    Args:
        G (Graph): NetworkX Graph
        M (DataFrame): a matrix of similarity values
        k (int): number of clusters

    Returns:
        DataFrame: A DataFrame with node_name and cluster columns
    """
    # KMedoids requires a numpy array
    np_of_values = np.array(m)
    kmedoids = KMedoids(n_clusters=k, random_state=0).fit(np_of_values)
    kmedoid_results = pd.DataFrame({'node_name': g.nodes(),
                                    'cluster': kmedoids.labels_})
    return kmedoid_results
