#!/usr/bin/python
# encoding:utf-8
# -*- Mode: Python -*-
# Author: Soros Liu <soros.liu1029@gmail.com>

# ==================================================================================================
# Copyright 2016 by Soros Liu
#
#                                                                          All Rights Reserved
"""
Algorithm Thinking: Project 1
Degree distributions for graphs
"""
__author__ = 'Soros Liu'
EX_GRAPH0 = {0: {1, 2},
             1: set([]),
             2: set([])}
EX_GRAPH1 = {0: {1, 4, 5},
             1: {2, 6},
             2: {3},
             3: {0},
             4: {1},
             5: {2},
             6: set([])}
EX_GRAPH2 = {0: {1, 4, 5},
             1: {2, 6},
             2: {3, 7},
             3: {7},
             4: {1},
             5: {2},
             6: set([]),
             7: {3},
             8: {1, 2},
             9: {0, 3, 4, 5, 6, 7}}

def make_complete_graph(num_nodes):
    """
    return complete graph with 'num_nodes' nodes
    """
    if num_nodes <= 0:
        return {}
    node_dict = {}
    for node_id in range(num_nodes):
        node_dict[node_id] = set([nid for nid in range(num_nodes) if nid != node_id])
    return node_dict

def compute_in_degrees(digraph):
    """
    compute in-degree of all nodes in the 'digraph'
    """
    result = dict(zip(digraph.keys(), [0] * len(digraph)))
    for value in digraph.values():
        for node in value:
            result[node] = result.get(node, 0) + 1
    return result

def in_degree_distribution(digraph):
    """
    compute unnormalized distribution of in-degree of the 'digraph'
    """
    result = {}
    for in_degree in compute_in_degrees(digraph).values():
        result[in_degree] = result.get(in_degree, 0) + 1
    return result
