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
import time
import matplotlib.pyplot as plt
import app2_1 as provided
__author__ = 'Soros Liu'

def fast_targeted_order(ugraph):
    new_graph = provided.copy_graph(ugraph)
    n = len(new_graph)
    degree_set = {}
    for k in range(n):
        degree_set[k] = set()
    for i in range(n):
        if i in new_graph:
            d = len(new_graph[i])
            degree_set[d].update(set([i]))
    l = []
    for k in range(n-1, -1, -1):
        while degree_set[k]:
            u = degree_set[k].pop()
            for neighbour in new_graph[u]:
                d = len(new_graph[neighbour])
                degree_set[d].difference_update(set([neighbour]))
                degree_set[d-1].update(set([neighbour]))
            l.append(u)
            neigh = new_graph[u]
            new_graph.pop(u)
            for nei in neigh:
                new_graph[nei].remove(u)
    return l

if __name__ == '__main__':
    node_number = range(10, 1000, 10)
    normal_time = []
    fast_time = []
    for number in node_number:
        upa = provided.UPA_graph(number, 5)
        from_time = time.time()
        provided.targeted_order(upa)
        to_time = time.time()
        normal_time.append(to_time - from_time)
        from_time = time.time()
        fast_targeted_order(upa)
        to_time = time.time()
        fast_time.append(to_time - from_time)

    plt.plot(node_number, normal_time, '-b', label='targeted_order function')
    plt.plot(node_number, fast_time, '-r', label='fast_targeted_order function')
    plt.legend(loc='upper right')
    plt.xlabel('node number for UPA graph')
    plt.ylabel('running time for two functions')
    plt.title('Timing Result using Desktop Python')
    plt.show()
