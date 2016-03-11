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
import app4 as at4
import project_alignment_of_sequence as provided
__author__ = 'Soros Liu'

human = at4.read_protein(at4.HUMAN_EYELESS_URL)
fly = at4.read_protein(at4.FRUITFLY_EYELESS_URL)
scoring_matrix = at4.read_scoring_matrix(at4.PAM50_URL)

alignment_matrix = provided.compute_alignment_matrix(human, fly, scoring_matrix, False)

score, align_human, align_fly = provided.compute_local_alignment(human, fly, scoring_matrix, alignment_matrix)
print score
print align_human
print align_fly
