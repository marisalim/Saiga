#!/usr/bin/env bash

# testing out new flags
# allows you to run all in one command
# python devo_wrapper.py --datID 20190502 --samps 20190502_sample_list.txt --mbseqs 20190502_primerindex.txt --demult minibar --subset 100 --perthresh 0.1 --db NCBI_voucher_elasmobranchii_WCS_seqs.fasta --rawNP n --demultgo n --filt n --clust y
python devo_wrapper.py --datID 20190502 --samps 20190502_sample_list.txt --mbseqs 20190502_primerindex.txt --demult minibar --subset none --perthresh 0.1 --db NCBI_voucher_elasmobranchii_WCS_seqs.fasta --rawNP n --demultgo n --filt n --clust y



## batcher for all the datasets/demultiplex trials/subsets for manuscript

## need to run each dataset 1x for the raw read nanoplots
# python devo_wrapper.py --datID 20190906 --samps 20190906_sample_list.txt --rawNP y --demultgo n --filt n --clust n
# python devo_wrapper.py --datID 20190909 --samps 20190909_sample_list.txt --rawNP y --demultgo n --filt n --clust n
# python devo_wrapper.py --datID 20190911 --samps 20190911_sample_list.txt --rawNP y --demultgo n --filt n --clust n
# python devo_wrapper.py --datID 20190913 --samps 20190913_sample_list.txt --rawNP y --demultgo n --filt n --clust n

## 1x for each qcat and minibar + filtering + demult nanoplots (full dat)
# python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --mbseqs 20190906_primerindex.txt --rawNP n --demultgo y --filt y --clust n
# python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --mbseqs 20190909_primerindex.txt --rawNP n --demultgo y --filt y --clust n
# python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --mbseqs 20190911_primerindex.txt --rawNP n --demultgo y --filt y --clust n
# python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --mbseqs 20190913_primerindex.txt --rawNP n --demultgo y --filt y --clust n

# python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt --rawNP n --demult y --filt y --clust n
# python devo_wrapper.py --datID 20190909 --demult qcat --samps 20190909_sample_list.txt --rawNP n --demult y --filt y --clust n
# python devo_wrapper.py --datID 20190911 --demult qcat --samps 20190911_sample_list.txt --rawNP n --demult y --filt y --clust n
# python devo_wrapper.py --datID 20190913 --demult qcat --samps 20190913_sample_list.txt --rawNP n --demult y --filt y --clust n

## then the subset versions starting from build subsets through stats parsing
# python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
#
# python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
#
# python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
#
# python devo_wrapper.py --datID 20190906 --demult qcat--samps 20190906_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190909 --demult qcat--samps 20190909_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190911 --demult qcat--samps 20190911_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190913 --demult qcat--samps 20190913_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
#
# python devo_wrapper.py --datID 20190906 --demult qcat--samps 20190906_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190909 --demult qcat--samps 20190909_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190911 --demult qcat--samps 20190911_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190913 --demult qcat--samps 20190913_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
#
# python devo_wrapper.py --datID 20190906 --demult qcat--samps 20190906_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190909 --demult qcat--samps 20190909_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190911 --demult qcat--samps 20190911_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
# python devo_wrapper.py --datID 20190913 --demult qcat--samps 20190913_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta --rawNP n --demult n --filt n --clust y
