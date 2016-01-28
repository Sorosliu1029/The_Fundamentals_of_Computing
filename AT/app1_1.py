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
__author__ = 'Soros Liu'
"""
Provided code for Application portion of Module 1

Imports physics citation graph
"""

# general imports
import urllib2
import matplotlib.pyplot as plt
import project_degree_distributions_for_graphs as provided

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)
unnor_in_degree_dstr = provided.in_degree_distribution(citation_graph)
in_degree_sum = sum(unnor_in_degree_dstr.values())
nor_in_degree_dsrt = [value / float(in_degree_sum) for value in unnor_in_degree_dstr.values()]
plt.plot(unnor_in_degree_dstr.keys(), nor_in_degree_dsrt, 'ro')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('log of in-degree')
plt.ylabel('log of the normalized distribution')
plt.title('Citation Graph In-degree Distribution')
plt.show()





