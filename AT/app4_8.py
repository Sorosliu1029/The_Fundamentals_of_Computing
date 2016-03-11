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
import string
__author__ = 'Soros Liu'

words = at4.read_words(at4.WORD_LIST_URL)
scoring_matrix = provided.build_scoring_matrix(string.ascii_letters, 2, 1, 0)


def check_spelling(checked_word, dist, word_list):
    checked_word_len = len(checked_word)
    result = set()
    for word in word_list:
        alignment_matrix = provided.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        score = provided.compute_global_alignment(checked_word, word, scoring_matrix, alignment_matrix)[0]
        distance = checked_word_len + len(word) - score
        if distance <= dist:
            result.add(word)
    return result

s1 = check_spelling('humble', 1, words)
print len(s1)
print s1
s2 = check_spelling('firefly', 2, words)
print len(s2)
print s2