#!/usr/bin/env bash

## DEMO version
python devo_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100 --subset 50 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta
python devo_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs demo_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 50 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta

## April/May/July/August 2019 datasets
## these datasets used custom indexes, so must use minibar
# python devo_wrapper.py --dat 20190405 --samps 20190405_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190405_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_elasmobranchii_WCS_seqs.fasta
# python devo_wrapper.py --dat 20190411 --samps 20190411_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190411_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_16sanuraElasmobranchiiAmniota_WCS_seqs.fasta
# python devo_wrapper.py --dat 20190418 --samps 20190418_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190418_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_16sanuraElasmobranchiiAmniota_WCS_seqs.fasta
# python devo_wrapper.py --dat 20190424 --samps 20190424_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190424_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_16sanuraElasmobranchiiAmniota_WCS_seqs.fasta
# python devo_wrapper.py --dat 20190502 --samps 20190502_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --mbseqs 20190502_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_elasmobranchii_WCS_seqs.fasta

## 0731 includes a custom index, so demultiplexed with minibar for all
# python devo_wrapper.py --dat 20190729 --samps 20190729_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190729_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_16sanuraElasmobranchiiAmniota_WCS_seqs.fasta
# python devo_wrapper.py --dat 20190731 --samps 20190731_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190731_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_16sanuraElasmobranchiiAmniota_WCS_seqs.fasta
# python devo_wrapper.py --dat 20190806 --samps 20190806_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs 20190806_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db NCBI_voucher_16sanuraElasmobranchiiAmniota_WCS_seqs.fasta

## batcher cmds for all the datasets/demultiplex trials/subsets for MinION manuscript
## 1. Raw read NanoPlots
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n

## 2. Demultiplex and filter
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
#
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190906_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190909_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190911_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190913_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100

## 3. Subset and cluster
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python devo_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
