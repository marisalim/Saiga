#!/usr/bin/env bash
# ---------------------------------------------
# Marisa Lim
# Wrapper script for running MiniBar to demultiplex
# Nanopore Minion sequence data
#
# Primary use is for running single datasets with one command
#   example: bash {script_path}/minibar_demultiplexing_wrapper.sh {mydat} {mytoppath}/2a_Format_minibarinput/{indexprimer_seq_file} {mytoppath}/1_Guppy_basecalled/{mydat}_guppybasecallouts/{myfastqfile} {index_editdist} {primer_editdist} {mydat}_demultiplexouts
#
# Dependency:
#   MiniBar v0.21
# https://github.com/calacademy-research/minibar
# Oct 2019
# ---------------------------------------------

source ~/.bashrc

mydatasetID=$1
mysample_indexfile=$2 # Use revcomp.py to create this file
myfastqfile=$3 # concatenated, filtered fastq file
index_edit_distance=$4 #default 4
primer_edit_distance=$5 #default 11
myoutput_dir=$6
bascallpath=$7

cd 2b_demultiplexed
if [ ! -d '$myoutput_dir' ]; then mkdir $myoutput_dir; fi

# Run MiniBar
# -T = trims barcode and primer from each end of the sequence, then outputs record
# -P = requires <str> if -F, <str> is prefix for individual files, followed by sample ID. (default: sample_)
# -F = create individual sample files for sequences with -S or -C output (default: False)

cd $myoutput_dir
minibar.py $mysample_indexfile $bascallpath/$myfastqfile -T -F -P $mydatasetID -e $index_edit_distance -E $primer_edit_distance
