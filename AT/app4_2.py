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

align_human = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ'
align_fly = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
consensus = at4.read_protein(at4.CONSENSUS_PAX_URL)
scoring_matrix = at4.read_scoring_matrix(at4.PAM50_URL)

for align in (align_human, align_fly):
    align = align.replace('-', '')
    alignment_matrix = provided.compute_alignment_matrix(align, consensus, scoring_matrix, True)
    score, alignment, cons = provided.compute_global_alignment(align, consensus, scoring_matrix, alignment_matrix)
    print sum([alignment[i] == cons[i] for i in range(len(alignment))]) / float(len(alignment))