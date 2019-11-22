#!/usr/bin/env bash

# ------------------------------------------------------------
# Nov 2019 Marisa Lim
# generate a file of just the fasta file headers
# used to check sp ID for Blast outputs
# ------------------------------------------------------------

cut -d ' ' -f 1,2,3 | sed 's/>//g' | awk '{print $1, $2"_"$3}'
