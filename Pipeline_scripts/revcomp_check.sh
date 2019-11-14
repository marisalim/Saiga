#!/usr/bin/env bash

source ~/.bashrc

clstr_file=$1
cdhit_out=$2

# note, -c must be >= 0.8
cd-hit-est -i $clstr_file -o $cdhit_out -c 0.8
