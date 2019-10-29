#!/usr/bin/env bash

source /anaconda3/etc/profile.d/conda.sh
conda activate medaka

input_demult=$1
input_draft=$2
output=$3

# edit cd-hit fasta - just use Cluster_0 sequence for draft assembly
head -n2 $input_draft > $input_draft.cluster0

# run Medaka
medaka_consensus -i $input_demult -d $input_draft.cluster0 -o $output
