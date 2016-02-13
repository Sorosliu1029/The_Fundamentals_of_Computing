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
import app2_1 as provided
import app2_3 as provided1
import project_connected_components_graph_resilience as provided2
import matplotlib.pyplot as plt
__author__ = 'Soros Liu'

if __name__ == '__main__':
    computer_network = provided.load_graph(provided.NETWORK_URL)
    ER = provided.ER_graph(1239, 0.004)
    UPA = provided.UPA_graph(1239, 3)
    network_attack_order = provided1.fast_targeted_order(computer_network)
    er_attack_order = provided1.fast_targeted_order(ER)
    upa_attack_order = provided1.fast_targeted_order(UPA)
    network_resilience = provided2.compute_resilience(computer_network, network_attack_order)
    er_resilience = provided2.compute_resilience(ER, er_attack_order)
    upa_resilience = provided2.compute_resilience(UPA, upa_attack_order)
    xval = list(range(len(network_attack_order) + 1))
    plt.plot(xval, network_resilience, '-b', label='Computer Network')
    plt.plot(xval, er_resilience, '-r', label='ER graph. p = 0.004')
    plt.plot(xval, upa_resilience, '-g', label='UPA graph. m = 3')
    plt.legend(loc='upper right')
    plt.xlabel('number of nodes removed')
    plt.ylabel('the size of the largest connect component')
    plt.title('Resilience for All Three Graphs under Max-degree Node Attack')
    plt.show()


