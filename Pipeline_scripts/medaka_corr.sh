#!/usr/bin/env bash

source /anaconda3/etc/profile.d/conda.sh
conda activate medaka

input_demult=$1
input_draft=$2
output=$3

# edit parsed clstr fasta and just use 1st sequence for draft assembly
head -n2 $input_draft > $input_draft.firstclstr

# run Medaka
medaka_consensus -i $input_demult -d $input_draft.firstclstr -o $output
