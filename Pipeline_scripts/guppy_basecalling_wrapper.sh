#!/usr/bin/env bash
# ---------------------------------------------
# Marisa Lim
# Wrapper script for running Nanopore Guppy software for basecalling
# Nanopore Minion sequence data
#
# Primary use is for running single dataset with one command:
#   example: bash guppy_basecalling_wrapper.sh /20180206_1431_1DNB_FISHCOI_6Feb2018/fast5 20180206 FLO-MIN106 SQK-LSK109 20180206_guppybasecallouts
#
# Dependency:
#   Guppy v 2.3.7 (download from Nanopore software page)
# March 2019
# ---------------------------------------------

# Source path for guppy
source ~/.bashrc

myseqdatpath=$1
myoutput_dir=$2
mytoppath=$3

# Set up directory paths for input and output
myinput_dir=$mytoppath/0_MinKNOW_rawdata/$myseqdatpath
# Make output directory for specific datasets
# check if directory exists, if not, then mkdir
if [ ! -d '$mytoppath/1_basecalled/$myoutput_dir' ]; then mkdir $mytoppath/1_basecalled/$myoutput_dir; fi

# Run guppy basecalling software
# --input = input directory
# --save_path = output directory
# -c basecalling model, set to run r9.4.1 'fast' flip-flop model
# --min_qscore = the minimum qscore a read must attain to pass qscore_filtering
# --recursive = search for files in any directories within fast5/ (this minKNOW fast5 format only applies to old datasets e.g., 2017-2018, 2019 version outputs all fast5 files directly to fast5/)
guppy_basecaller --input $myinput_dir --save_path $mytoppath/1_basecalled/$myoutput_dir -c dna_r9.4.1_450bps_fast.cfg --min_qscore 7 --recursive
