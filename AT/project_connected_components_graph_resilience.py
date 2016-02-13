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
Connected components and graph resilience
"""
from collections import deque
__author__ = 'Soros Liu'


def bfs_visited(ugraph, start_node):
    """
    using BFS to return connected components with start node
    """
    queue = deque()
    visited = set([start_node])
    queue.append(start_node)
    while queue:
        node = queue.pop()
        for neighbour in ugraph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return visited

def cc_visited(ugraph):
    """
    return all connected components in ugraph using bfs_visited() function above
    """
    remaining = set(ugraph.keys())
    connected = []
    while remaining:
        node = remaining.pop()
        visited = bfs_visited(ugraph, node)
        connected.append(visited)
        remaining.difference_update(visited)
    return connected

def largest_cc_size(ugraph):
    """
    return the size of the largest connected components in ugraph
    """
    return max(list(map(len, cc_visited(ugraph))) + [0])

def compute_resilience(ugraph, attack_order):
    """
    simulate network server attack
    """
    result = [largest_cc_size(ugraph)]
    for attack_node in attack_order:
        ugraph.pop(attack_node, None)
        for value in ugraph.values():
            value.discard(attack_node)
        result.append(largest_cc_size(ugraph))
    return result


# GRAPH0 = {0: set([1]),
#           1: set([0, 2]),
#           2: set([1, 3]),
#           3: set([2])}
#
# print bfs_visited(GRAPH0, 0)
# print cc_visited(GRAPH0)
# print largest_cc_size(GRAPH0)
# print compute_resilience(GRAPH0, [1, 2])