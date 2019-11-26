#!/usr/bin/env python

# -*- coding: utf-8 -*-

# ---------------------------------------------
# Marisa Lim
# 1. reverse complement indexes and primers

# on hold -- wanted to make the input file here, but need to think how to design
        # so that it takes all cases (diff name and number of samples, diff combinations of indexes for F and R)
        # for now, just generating a file that has all the rev comp sequences that can be copy/pasted to input text file
# 2. generate input file for minibar demultiplexing
	# requires sample ID, F primer ID, F index seq, F index revcomp seq, F primer seq, F primer revcomp seq,
	# R primer ID, R index seq, R index revcomp seq, R primer seq, R primer revcomp seq

# edit all_primerindex_seqs.csv file with your SampleID, primerID & seq, and index seq information
#
#  Dependency:
    # all_primerindex_seqs.csv #has index and primer sequences
# July 2019
# ---------------------------------------------

import os, sys, argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description='''Get reverse complement sequence for index and primers.
    Input for MiniBar.''',
    epilog='''Example: python revcomp.py'''
)
args=parser.parse_args()

# open file
revcompfile = pd.read_csv('all_primerindex_seqs.csv', sep=',')

# define function to derive complement of any seq
def reverse_comp(seq):
    # check if sequence is lower case, if True then make uppercase
    if seq.islower() == True:
        seq = seq.upper()
    # ATCG, including ambiguity codes to translate [only translates upper case, if you want lower case, must add in lower case letters]
    comp_table = str.maketrans('ACTGKMSWRYBDHVN', 'TGACMKSWYRVHDBN')
    # seq[::-1] reverses sequence and translate(comp_table) gives complement sequence
    comp_barcode = seq[::-1].translate(comp_table)
    # return value from this function
    return comp_barcode

# get rev comp seqs and save
newseqs = []
for i in revcompfile.index:
    myseq = revcompfile.at[i, 'MarkerSeq']
    revcompseq = reverse_comp(myseq)
    newseqs.append(revcompseq)
revcompfile['MarkerRCSeq'] = newseqs

revcompfile.to_csv('all_primerindex_seqs_RCseqs.csv', sep='\t')
