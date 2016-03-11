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
import project_alignment_of_sequence as provided
import random
import app4 as at4
import math
import matplotlib.pyplot as plt
__author__ = 'Soros Liu'


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    scoring_distribution = dict()
    list_y = list(seq_y)
    for i in range(num_trials):
        temp_seq_y = list_y
        random.shuffle(temp_seq_y)
        rand_y = ''.join(temp_seq_y)
        alignment_matrix = provided.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = provided.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)[0]
        scoring_distribution[score] = scoring_distribution.get(score, 0) + 1
    return scoring_distribution

TOTAL_TRIALS = 1000
human = at4.read_protein(at4.HUMAN_EYELESS_URL)
fly = at4.read_protein(at4.FRUITFLY_EYELESS_URL)
scoring_matrix = at4.read_scoring_matrix(at4.PAM50_URL)
scoring_distribution = generate_null_distribution(human, fly, scoring_matrix, TOTAL_TRIALS)
# plt.bar(scoring_distribution.keys(),
#         list(map(lambda value: value / float(TOTAL_TRIALS), scoring_distribution.values())))
# plt.xlabel('score')
# plt.ylabel('fraction of total trials')
# plt.title('Normalized Score Distribution')
# plt.show()

scores = scoring_distribution.keys()
num_score = scoring_distribution.values()
length = len(scoring_distribution)
mean = sum([scores[i] * num_score[i] for i in range(length)]) / float(TOTAL_TRIALS)
deviation = math.sqrt(sum(list(map(lambda score, num: (score - mean) ** 2 * num,
                                   scores, num_score))) / float(TOTAL_TRIALS))

print mean
print deviation
print (875 - mean) / deviation
