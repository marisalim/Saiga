#!/usr/bin/env bash

## DEMO version
python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP n --demultgo n --filt n --subgo n --clust y --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100 --subset none --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta
#python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --mbseqs demo_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset none --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta



## batcher cmds for all the datasets/demultiplex trials/subsets for MinION manuscript
## 1. Raw read NanoPlots
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP y --demultgo n --filt n --subgo n --clust n

## 2. Demultiplex and filter
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100
#
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190906_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190909_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190911_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo y --filt y --subgo n --clust n --demult minibar --mbseqs 20190913_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100

## 3. Subset and cluster
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult qcat --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 100 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
#
# python saiga_wrapper.py --dat 20190906 --samps 20190906_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190909 --samps 20190909_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190911 --samps 20190911_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
# python saiga_wrapper.py --dat 20190913 --samps 20190913_sample_list.txt --rawNP n --demultgo n --filt n --subgo y --clust y --demult minibar --subset 5000 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta
