"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster
######################################################
# Code for closest pairs of clusters


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    result = (float('inf'), -1, -1)
    list_len = len(cluster_list)
    for idx1 in range(list_len):
        for idx2 in range(list_len):
            if cluster_list[idx1] != cluster_list[idx2]:
                result = min(result, pair_distance(cluster_list, idx1, idx2), key=lambda cluster: cluster[0])
    return result


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    list_len = len(cluster_list)
    if list_len <= 3:
        result = slow_closest_pair(cluster_list)
    else:
        half_len = list_len / 2
        left_half = [cluster_list[idx] for idx in range(0, half_len)]
        right_half = [cluster_list[idx] for idx in range(half_len, list_len)]
        left_result = fast_closest_pair(left_half)
        right_result = fast_closest_pair(right_half)
        right_result = (right_result[0], right_result[1]+half_len, right_result[2]+half_len)
        temp_result = min(left_result, right_result, key=lambda cluster: cluster[0])
        mid = (cluster_list[half_len-1].horiz_center() + cluster_list[half_len].horiz_center()) / 2
        result = min(temp_result, closest_pair_strip(cluster_list, mid, temp_result[0]),
                     key=lambda cluster: cluster[0])
    return result


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    strip_idx = [idx for idx in range(len(cluster_list))
                 if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width]
    strip_idx.sort(key=lambda idx: cluster_list[idx].vert_center())
    strip_len = len(strip_idx)
    result = (float('inf'), -1, -1)
    for idx1 in range(0, strip_len-1):
        for idx2 in range(idx1+1, min(idx1+3, strip_len-1)+1):
            result = min(result, pair_distance(cluster_list, strip_idx[idx1], strip_idx[idx2]),
                         key=lambda cluster: cluster[0])
    return result

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key=lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair(cluster_list)
        cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])
        cluster_list.pop(closest_pair[2])
    assert len(cluster_list) == num_clusters
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # position initial clusters at the location of clusters with largest populations
    list_len = len(cluster_list)
    centers = cluster_list[:]
    centers.sort(key=lambda cluster: cluster.total_population(), reverse=True)
    centers = centers[:num_clusters]
    cluster_sets = None
    for dummy_i in range(num_iterations):
        cluster_sets = [alg_cluster.Cluster(set([]), 0.0, 0.0, 0.0, 0.0) for dummy_idx in range(num_clusters)]
        for idx in range(list_len):
            min_idx = min(range(num_clusters), key=lambda center_idx: cluster_list[idx].distance(centers[center_idx]))
            cluster_sets[min_idx].merge_clusters(cluster_list[idx])
        centers = cluster_sets
    return cluster_sets
