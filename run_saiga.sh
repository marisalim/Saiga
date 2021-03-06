#!/usr/bin/env bash

## DEMO version
python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100 --subset 50 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta
#python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs demo_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 50 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta

