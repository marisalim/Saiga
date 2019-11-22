#!/usr/bin/env bash

# ------------------------------------------------------------
# Nov 2019 Marisa Lim
# make fasta seq one line instead of multiple
# ------------------------------------------------------------

input=$1
output=$2

awk '{if(NR==1) {print $0} else {if($0 ~ /^>/) {print "\n"$0} else {printf $0}}}' $input > $output
rm $input
