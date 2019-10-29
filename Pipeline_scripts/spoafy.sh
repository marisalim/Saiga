#!/usr/bin/env bash

source ~/.bashrc

clstr_path=$1

# make consensus
for file in $clstr_path/*.fastq; do echo $file; spoa $file > $file.spoa; done

# rename file
for file in $clstr_path/*.spoa; do mv $file $(echo $file | cut -f1 -d.)_spoa.fasta; done
