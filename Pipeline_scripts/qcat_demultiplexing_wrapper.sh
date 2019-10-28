#!/usr/bin/env bash
# ---------------------------------------------
# Marisa Lim
# Wrapper script for running Qcat to demultiplex
# Nanopore Minion sequence data
#
# Primary use is for running single datasets with one command
#   example: bash {script_path}/qcat_demultiplexing_wrapper.sh {mydatasetID} {myfastqfile} {myminscore} {mybarcodekit} {myoutput} {mytoppath}
#
# Dependency:
#   Qcat - see github page
#
# October 2019
# ---------------------------------------------

source ~/.bashrc

mydatasetID=$1
myfastqfile=$2 # concatenated, filtered fastq file
myminscore=$3 # 0-100 scale
mybarcodekit=$4 #PBC001
myoutput_dir=$5
basecallpath=$6

cd 2b_demultiplexed
if [ ! -d '$myoutput_dir' ]; then mkdir $myoutput_dir; fi

# Run Qcat
cd $myoutput_dir
qcat -f $basecallpath/$myfastqfile -b $myoutput_dir -k $mybarcodekit --min-score $myminscore --trim --epi2me
# --tsv > $myoutput/$datasetID.tsv
