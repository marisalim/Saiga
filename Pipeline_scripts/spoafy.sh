#!/usr/bin/env bash

source ~/.bashrc

clstr_path=$1

# make consensus
for file in $clstr_path/*.fastq; do echo $file; spoa $file > $file.spoa; done

# rename file and fasta header
for file in $clstr_path/*.spoa; do awk 'NR==1{print line">" $0 "|"FILENAME;}END{print $0" "}' $file > $(echo $file | cut -f1 -d.)_spoa.fasta; done
rm $clstr_path/*.fastq.spoa
