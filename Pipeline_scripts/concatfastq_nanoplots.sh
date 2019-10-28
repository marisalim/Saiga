#!/usr/bin/env bash
# ---------------------------------------------
# Marisa Lim
# Wrapper script for concatenating basecalled fastq files and running NanoPlot to check
# read length and quality distributions
# Nanopore Minion sequence data
#
# Primary use is for running single dataset with one command:
#   example: bash concatenate_fastq_NanoPlot.sh ./Basecall_guppy_outs/20171228_guppybasecallouts/ 20171228 20171228_raw_filt_NanoPlots 20171228_raw <return>
#
# Dependency:
#   NanoPlot v 1.21.0
# https://github.com/wdecoster/NanoPlot
# March 2019
# ---------------------------------------------

basecallout_path=$1
cat_output_name=$2
NanoPlot_output_path=$3
NanoPlot_output_name=$4

# Concatenate all the fastq output files from guppy_basecaller into a single fastq file
cd $basecallout_path/
echo 'Concatenating Guppy basecalled fastq files...'
cat *.fastq > $cat_output_name.fastq
# Then run NanoPlot on raw data to look at length and quality distributions
# it will make the output dir
echo 'Running NanoPlot...'
NanoPlot --fastq_rich $cat_output_name.fastq -o $NanoPlot_output_path -p $NanoPlot_output_name --plots kde
