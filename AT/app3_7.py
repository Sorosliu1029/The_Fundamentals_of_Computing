#!/usr/bin/python
# encoding:utf-8
# -*- Mode: Python -*-
# Author: Soros Liu <soros.liu1029@gmail.com>

# ==================================================================================================
# Copyright 2016 by Soros Liu
#
#                                                                          All Rights Reserved
"""

"""
import project_closest_pair_clustering as provided
import alg_project3_viz as viz
import alg_cluster
__author__ = 'Soros Liu'

def compute_distortion(cluster_list, data_table):
    distortion = 0.0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion

if __name__ == '__main__':
    data_table = viz.load_data_table('unifiedCancerData_290.csv')
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = provided.hierarchical_clustering(singleton_list, 16)
    print compute_distortion(cluster_list, data_table)
    # cluster_list = provided.kmeans_clustering(singleton_list, 16, 5)
    # print compute_distortion(cluster_list, data_table)
