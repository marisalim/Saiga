#!/usr/bin/env bash

source ~/.bashrc

# use seqtk to create random subsets of fastq files
mydat=$1
mysub=$2
mysampfq=$3 #just prefix, no extension
myoutput_dir=$4
demultpath=$5

if [ ! -d '$myoutput_dir' ]; then mkdir $myoutput_dir; fi

# -s is random seed
seqtk sample -s100 $demultpath/$mysampfq.fastq $mysub > $myoutput_dir/$mydat$mysampfq$mysub.fastq
