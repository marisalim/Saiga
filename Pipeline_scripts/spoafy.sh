#!/usr/bin/env bash

# ------------------------------------------------------------
# Nov 2019 Marisa Lim
# generate spoa consensus sequences, format file name
# ------------------------------------------------------------

source ~/.bashrc

clstr_file=$1

# make consensus
spoa $clstr_file > $clstr_file.spoa

# rename file and fasta header
awk -v var=">clstr$(echo $clstr_file.spoa | rev | cut -f1 -d/ |rev |cut -f1 -d.)" 'NR==1{print var "|" $0;}END{print $0" "}' $clstr_file.spoa > $(echo $clstr_file.spoa | rev | cut -f3 -d. | rev)_spoa.fasta

rm $clstr_file.spoa

# old - use if you want to run spoa on all fastq files within a $clstr_path directory
# for file in $clstr_path/*.fastq; do echo $file; spoa $file > $file.spoa; done
# for file in $clstr_path/*.spoa; do awk -v var=">clstr$(echo $file | rev | cut -f1 -d/ |rev |cut -f1 -d.)" 'NR==1{print var "|" $0;}END{print $0" "}' $file > $(echo $file | cut -f1 -d.)_spoa.fasta; done
