#!/usr/bin/env bash

# ------------------------------------------------------------
# Nov 2019 Marisa Lim
# use cd-hit-est to cluster spoa consensus sequences
# used to check whether smaller isONclust clusters are rev-comp reads
# ------------------------------------------------------------

source ~/.bashrc

clstr_file=$1
cdhit_out=$2
thresh=$3

# note, -c must be >= 0.8
cd-hit-est -i $clstr_file -o $cdhit_out -c $thresh
