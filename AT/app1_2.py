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
import matplotlib.pyplot as plt
import random
import project_degree_distributions_for_graphs as provided

__author__ = 'Soros Liu'


def ER(node_num, prob):
    graph = {}
    for from_node in range(node_num):
        graph[from_node] = set()
        for to_node in range(node_num):
            if from_node != to_node:
                r = random.random()
                if r < prob:
                    graph[from_node].add(to_node)
    return graph

graph = ER(1000, 0.5)
unnor_in_degree_dstr = provided.in_degree_distribution(graph)
in_degree_sum = sum(unnor_in_degree_dstr.values())
nor_in_degree_dsrt = [value / float(in_degree_sum) for value in unnor_in_degree_dstr.values()]
plt.plot(unnor_in_degree_dstr.keys(), nor_in_degree_dsrt, 'ro')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('log of in-degree')
plt.ylabel('log of the normalized distribution')
plt.title('ER Graph')
plt.show()