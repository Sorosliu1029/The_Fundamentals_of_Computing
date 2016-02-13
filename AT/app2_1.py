#!/usr/bin/python
# encoding:utf-8
# -*- Mode: Python -*-
# Author: Soros Liu <soros.liu1029@gmail.com>

# ==================================================================================================
# Copyright 2016 by Soros Liu
#
#                                                                          All Rights Reserved
"""
Provided code for Application portion of Module 2
"""
__author__ = 'Soros Liu'

import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
import project_degree_distributions_for_graphs as provided
import project_connected_components_graph_resilience as provided1


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def random_order(ugraph):
    order = list(range(len(ugraph)))
    random.shuffle(order)
    return order

##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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

def ER_graph(node_num, prob):
    graph = {}
    for node_i in range(node_num):
        graph[node_i] = set()
    for node_i in range(node_num):
        for node_j in range(node_i+1, node_num):
            r = random.random()
            if r < prob:
                graph[node_i].add(node_j)
                graph[node_j].add(node_i)
    return graph

class UPATrial:
    """
    Simple class to encapsulate optimized trials for the UPA algorithm

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def UPA_graph(num_nodes, new_neigh_num):
    trial = UPATrial(new_neigh_num)
    result = provided.make_complete_graph(new_neigh_num)
    for new_add_node in range(new_neigh_num, num_nodes):
        new_neigh_set = trial.run_trial(new_neigh_num)
        result[new_add_node] = new_neigh_set
        for neighbour in new_neigh_set:
            result[neighbour].add(new_add_node)
    return result


if __name__ == '__main__':
    computer_network = load_graph(NETWORK_URL)
    ER = ER_graph(1239, 0.004)
    UPA = UPA_graph(1239, 3)
    # network_degree = {}
    # for value in computer_network.values():
    #     network_degree[len(value)] = network_degree.get(len(value), 0) + 1
    # network_total_degree = sum(network_degree.values())
    # network_x = []
    # network_y = []
    # for key, value in network_degree.items():
    #     network_x.append(key)
    #     network_y.append(float(value) / network_total_degree)
    # plt.plot(network_x, network_y, 'ob', label='network')
    # er_degree = {}
    # for value in ER.values():
    #     er_degree[len(value)] = er_degree.get(len(value), 0) + 1
    # er_total_degree = sum(er_degree.values())
    # er_x = []
    # er_y = []
    # for key, value in er_degree.items():
    #     er_x.append(key)
    #     er_y.append(float(value) / er_total_degree)
    # plt.plot(er_x, er_y, 'og', label='er')
    # upa_degree = {}
    # for value in UPA.values():
    #     upa_degree[len(value)] = upa_degree.get(len(value), 0) + 1
    # upa_total_degree = sum(upa_degree.values())
    # upa_x = []
    # upa_y = []
    # for key, value in upa_degree.items():
    #     upa_x.append(key)
    #     upa_y.append(float(value) / upa_total_degree)
    # plt.plot(upa_x, upa_y, 'or', label='upa')
    # plt.legend(loc='upper right')
    # plt.show()
    # input('hha')
    # ER_edge = 0
    # for node in ER:
    #     ER_edge += len(ER[node])
    # print ER_edge / 2
    # UPA_edge = 0
    # for node in UPA:
    #     UPA_edge += len(UPA[node])
    # print UPA_edge / 2
    attack_order = random_order(computer_network)
    # print attack_order
    network_resilience = provided1.compute_resilience(computer_network, attack_order)
    ER_resilience = provided1.compute_resilience(ER, attack_order)
    UPA_resilience = provided1.compute_resilience(UPA, attack_order)
    # print len(network_resilience)
    # print len(ER_resilience)
    # print len(UPA_resilience)
    xval = list(range(len(attack_order) + 1))
    plt.plot(xval, network_resilience, '-b', label='Computer Network')
    plt.plot(xval, ER_resilience, '-r', label='ER graph. p = 0.004')
    plt.plot(xval, UPA_resilience, '-g', label='UPA graph. m = 3')
    plt.legend(loc='upper right')
    plt.xlabel('number of nodes removed')
    plt.ylabel('the size of the largest connect component')
    plt.title('Resilience for All Three Graphs')
    plt.show()






