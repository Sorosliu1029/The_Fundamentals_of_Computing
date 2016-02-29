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
import random
import alg_cluster
import time
import matplotlib.pyplot as plt
import project_closest_pair_clustering as provided
__author__ = 'Soros Liu'


def gen_random_clusters(num_clusters):
    return [alg_cluster.Cluster(set([]), random.uniform(-1, 1), random.uniform(-1, 1), 0.0, 0.0)
            for dummy_i in range(num_clusters)]

if __name__ == '__main__':
    slow_time = []
    fast_time = []
    num_list = range(2, 201)
    for num_clusters in num_list:
        cluster_list = gen_random_clusters(num_clusters)
        slow_time_start = time.time()
        dummy_result1 = provided.slow_closest_pair(cluster_list)
        slow_time_end = time.time()
        slow_time.append(slow_time_end-slow_time_start)

        cluster_list.sort(key=lambda cluster: cluster.horiz_center())
        fast_time_start = time.time()
        dummy_result2 = provided.fast_closest_pair(cluster_list)
        fast_time_end = time.time()
        fast_time.append(fast_time_end-fast_time_start)

        assert dummy_result1[0] == dummy_result2[0]

    plt.plot(num_list, slow_time, '-b', label='slow_closest_pair')
    plt.plot(num_list, fast_time, '-r', label='fast_closest_pair')
    plt.legend(loc='upper left')
    plt.xlabel('number of clusters generated')
    plt.ylabel('time used to compute (in seconds)')
    plt.title('Comparison of Running Time of Two Closest-pair Function')
    plt.show()
