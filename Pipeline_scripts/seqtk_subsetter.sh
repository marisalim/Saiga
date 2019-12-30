#!/usr/bin/env bash

# ------------------------------------------------------------
# Nov 2019 Marisa Lim
# generate data subsets
# ------------------------------------------------------------


source ~/.bashrc

# use seqtk to create random subsets of fastq files
mysub=$1
mysampfq=$2 #just prefix, no extension
myoutput_dir=$3
demultpath=$4
seed=$5

if [ ! -d '$myoutput_dir' ]; then mkdir $myoutput_dir; fi

# -s is random seed
seqtk sample -s$seed $demultpath/$mysampfq.fastq $mysub > $myoutput_dir/$mysampfq$mysub.$seed.fastq
