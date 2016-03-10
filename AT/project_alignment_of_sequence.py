#!/usr/bin/python
# encoding:utf-8
# -*- Mode: Python -*-
# Author: Soros Liu <soros.liu1029@gmail.com>

# ==================================================================================================
# Copyright 2016 by Soros Liu
#
#                                                                          All Rights Reserved
"""
Project for Module 4
Compute alignment of sequence
"""
__author__ = 'Soros Liu'


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    return a scoring matrix depending on the input score and alphabet set
    """
    alp = set(alphabet)
    alp.add('-')
    result = dict()
    for char_a in alp:
        row_result = dict()
        for char_b in alp:
            if char_a == '-' or char_b == '-':
                row_result[char_b] = dash_score
            elif char_a == char_b:
                row_result[char_b] = diag_score
            else:
                row_result[char_b] = off_diag_score
        result[char_a] = row_result
    return result


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    return an (global or local) alignment matrix of seq_x and seq_y
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    result = [[0 for dummy_j in range(len_y+1)] for dummy_i in range(len_x+1)]
    for row in range(1, len_x+1):
        result[row][0] = result[row-1][0] + scoring_matrix[seq_x[row-1]]['-']
        if not global_flag and result[row][0] < 0:
            result[row][0] = 0
    for col in range(1, len_y+1):
        result[0][col] = result[0][col-1] + scoring_matrix['-'][seq_y[col-1]]
        if not global_flag and result[0][col] < 0:
            result[0][col] = 0
    for row in range(1, len_x+1):
        for col in range(1, len_y+1):
            result[row][col] = max(result[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]],
                                   result[row-1][col] + scoring_matrix[seq_x[row-1]]['-'],
                                   result[row][col-1] + scoring_matrix['-'][seq_y[col-1]])
            if not global_flag and result[row][col] < 0:
                result[row][col] = 0
    return result


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    return the global alignment of seq_x and seq_y
    """
    row = len(seq_x)
    col = len(seq_y)
    align_x = ''
    align_y = ''
    while row != 0 and col != 0:
        if alignment_matrix[row][col] == alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]:
            align_x = seq_x[row-1] + align_x
            align_y = seq_y[col-1] + align_y
            row -= 1
            col -= 1
        else:
            if alignment_matrix[row][col] == alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']:
                align_x = seq_x[row-1] + align_x
                align_y = '-' + align_y
                row -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[col-1] + align_y
                col -= 1
    while row != 0:
        align_x = seq_x[row-1] + align_x
        align_y = '-' + align_y
        row -= 1
    while col != 0:
        align_x = '-' + align_x
        align_y = seq_y[col-1] + align_y
        col -= 1
    return alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    return the local alignment of seq_x, seq_y
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    max_pos = (-1, -1)
    max_score = float('-inf')
    for row in range(len_x+1):
        for col in range(len_y+1):
            if alignment_matrix[row][col] > max_score:
                max_score = alignment_matrix[row][col]
                max_pos = (row, col)
    align_x = ''
    align_y = ''
    row, col = max_pos
    while alignment_matrix[row][col] != 0:
        if alignment_matrix[row][col] == alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]:
            align_x = seq_x[row-1] + align_x
            align_y = seq_y[col-1] + align_y
            row -= 1
            col -= 1
        else:
            if alignment_matrix[row][col] == alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']:
                align_x = seq_x[row-1] + align_x
                align_y = '-' + align_y
                row -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[col-1] + align_y
                col -= 1
    return max_score, align_x, align_y
