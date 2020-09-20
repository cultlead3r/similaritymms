"""Utility functions for RDD"""


from scipy.stats import ks_2samp
import numpy as np
import pandas as pd
from rdd.RDD import realworld_distance_compare


def df_to_cluster_list(df):
    """Takes a pandas Series and returns a list of partitioned nodes

    Args:
        clustered_nodes (pandas DataFrame): A dataframe with a "cluster" column

    Returns:
        list: List of lists: first list would be all nodes in partition 0, etc.
    """
    # sort the series by (cluster) value
    clustered_nodes = df.sort_values('cluster')
    # Assuming clustering algorithms start with cluster 0
    cluster = 0
    partitioned_nodes = []
    cluster_list = []
    for name, clust in zip(clustered_nodes.node_name, clustered_nodes.cluster):
        if clust == cluster:
            cluster_list.append(name)
        else:
            cluster = clust
            partitioned_nodes.append(cluster_list)
            cluster_list = []
            cluster_list.append(name)
    # get the last partition
    partitioned_nodes.append(cluster_list)
    return partitioned_nodes


def get_histograms(dfs, bins):
    """Takes a DataFrame of node_number->RDD values

    Args:
        dfs (dict): A dictionary of DataFrames node_name->RDD values
        bins (int): Number of bins to make for histogram

    Returns:
        (dict): A dictionary of histograms.
    """
    histos = {}
    for d in dfs:
        histos[d] = np.histogram(dfs[d]['normalized_rdd'], bins=bins)
    return histos


def kstest_histograms(hist_1, hist_2):
    """Runs a kstest on two dictionaries of histograms

    Args:
        hist_1 (dict): A dictionary of histograms
        hist_2 (dict): A dictionary of histograms
    """
    for u in hist_1:
        for j in hist_2:
            print(u, " - ", j, ":", ks_2samp(hist_1[u][0], hist_2[j][0]))


def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    n = len(data)
    x = np.sort(data)
    y = np.arange(1, n+1) / n
    return x, y


def get_df_for_cluster(g, target_G, measure_list, target_rad):
    """Gets a Matrix of all RDD values to and from all nodes.

    Args:
        g (NetworkX Graph): A

    Returns:
        DataFrame: A matrix of all RDD values to and from all nodes.
    """
    all_rdds_df = pd.DataFrame()
    for target_one in g.nodes():
        rdd_list = []
        for target_two in g.nodes():
            rdd_list.append(realworld_distance_compare(target_G,
                                                       target_one,
                                                       target_two,
                                                       measure_list,
                                                       target_rad))
        all_rdds_df[target_one] = rdd_list
    return all_rdds_df
