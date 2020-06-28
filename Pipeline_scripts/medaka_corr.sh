#!/usr/bin/env bash

# ------------------------------------------------------------
# Nov 2019 Marisa Lim
# error correct spoa consensus with Medaka
# only map reads that were in majority cluster after
# isONclust and cd-hit steps
# ------------------------------------------------------------

# set conda path - depending on OS, you may need to change this path
# this path works on Macs
source /anaconda3/etc/profile.d/conda.sh
# The default path on Ubuntu is:
# source ~/anaconda3/etc/profile.d/conda.sh

# activate medaka
conda activate medaka

input_demult=$1
input_draft=$2
output=$3

# edit parsed clstr fasta and just use 1st sequence for draft assembly
head -n2 $input_draft > $input_draft.firstclstr

# run Medaka
medaka_consensus -i $input_demult -d $input_draft.firstclstr -o $output
