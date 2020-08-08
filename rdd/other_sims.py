import networkx as nx
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from rdd.measures import *

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

    df['simrank'] = normalize_rdd(df, 1, 1000, 'simrank')
    df['simrank'] = np.log10(df['simrank'])
    
    # print(df)

    return df

def k_means(df, measure_vector, k=3):
    kmeans = KMeans(n_clusters=k) 
    
    feats = []
    for m in measure_vector:
        feats.append( m.__name__ )

    y = kmeans.fit_predict(df[feats])

    df['k_mean_cluster'] = y

    return df

def k_means_other(df, target_columns, k=3):
    kmeans = KMeans(n_clusters=k) 
    
    feats = target_columns
    
    y = kmeans.fit_predict(df[feats])

    df['k_mean_cluster'] = y

    return df

def mean_shift(df, measure_vector):
    mean_shi = MeanShift()
    
    feats = []
    for m in measure_vector:
        feats.append( m.__name__ )

    y = mean_shi.fit_predict(df[feats])

    df['mean_shift_cluster'] = y

    return df

def mean_shift_other(df, target_columns):
    mean_shi = MeanShift()
    
    feats = target_columns
    y = mean_shi.fit_predict(df[feats])

    df['mean_shift_cluster'] = y

    return df