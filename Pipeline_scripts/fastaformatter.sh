#!/usr/bin/env bash

input=$1
output=$2

awk '{if(NR==1) {print $0} else {if($0 ~ /^>/) {print "\n"$0} else {printf $0}}}' $input > $output
rm $input
