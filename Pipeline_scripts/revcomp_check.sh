#!/usr/bin/env bash

source ~/.bashrc

clstr_file=$1
cdhit_out=$2

cd-hit-est -i $clstr_file -o $cdhit_out
