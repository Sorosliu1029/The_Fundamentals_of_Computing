"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import time
import app3_7
import matplotlib.pyplot as plt

# conditional imports
if DESKTOP:
    import project_closest_pair_clustering as alg_project3_solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    # data_file = urllib2.urlopen(data_url)
    with open(data_url) as data_file:
        data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table('unifiedCancerData_111.csv')
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    # cluster_list = sequential_clustering(singleton_list, 15)
    # print "Displaying", len(cluster_list), "sequential clusters"

    # cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
    # print 'hierarchical error', app3_7.compute_distortion(cluster_list, data_table)
    # print "Displaying", len(cluster_list), "hierarchical clusters"

    cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)
    print 'k means error', app3_7.compute_distortion(cluster_list, data_table)
    print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        # alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

def compare_distortion():
    # data_table = load_data_table('unifiedCancerData_111.csv')
    # data_table = load_data_table('unifiedCancerData_290.csv')
    data_table = load_data_table('unifiedCancerData_896.csv')
    hie_distortion = []
    kmeans_distortion = []
    num_output = range(20, 5, -1)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    hie_list = singleton_list[:]
    for num_cluster in num_output:
        hie_list = alg_project3_solution.hierarchical_clustering(hie_list, num_cluster)
        hie_distortion.append(app3_7.compute_distortion(hie_list, data_table))
        kmeans_list = alg_project3_solution.kmeans_clustering(singleton_list, num_cluster, 5)
        kmeans_distortion.append(app3_7.compute_distortion(kmeans_list, data_table))
    plt.plot(num_output, hie_distortion, '-b', label='hierarchical clustering')
    plt.plot(num_output, kmeans_distortion, '-r', label='k-means clustering')
    plt.legend(loc='upper right')
    plt.xlabel('number of output clusters')
    plt.ylabel('distortion of two clustering methods')
    plt.title('Comparison of the Distortion with ' + str(len(singleton_list)) +
              ' County Data Set')
    plt.show()


if __name__ == '__main__':
    # start_time = time.time()
    # run_example()
    # end_time = time.time()
    # print end_time - start_time
    compare_distortion()
