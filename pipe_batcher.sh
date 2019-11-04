#!/usr/bin/env bash

## batcher for all the datasets/demultiplex trials/subsets

## need to run each dataset 1x for the raw read nanoplots
## --demult, --samps, --db flags won't be used here, but have to include them since I made them required
# python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190909 --demult qcat --samps 20190909_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190911 --demult qcat --samps 20190911_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190913 --demult qcat --samps 20190913_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

## 1x for each qcat and minibar + filtering + demult nanoplots (full dat)
## --db flag won't be used here, but have to include it since I made it required
# python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --mbseqs 20190906_primerindex.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --mbseqs 20190909_primerindex.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --mbseqs 20190911_primerindex.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --mbseqs 20190913_primerindex.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
#
# python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190909 --demult qcat --samps 20190909_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190911 --demult qcat --samps 20190911_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
# python devo_wrapper.py --datID 20190913 --demult qcat --samps 20190913_sample_list.txt --subset none --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

## then the subset versions starting from build subsets through stats parsing
## this set finally uses all the flags!
# python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --mbseqs 20190906_primerindex.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --mbseqs 20190909_primerindex.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --mbseqs 20190911_primerindex.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --mbseqs 20190913_primerindex.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --mbseqs 20190906_primerindex.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --mbseqs 20190909_primerindex.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --mbseqs 20190911_primerindex.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --mbseqs 20190913_primerindex.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --mbseqs 20190906_primerindex.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190909 --demult minibar --samps 20190909_sample_list.txt --mbseqs 20190909_primerindex.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190911 --demult minibar --samps 20190911_sample_list.txt --mbseqs 20190911_primerindex.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190913 --demult minibar --samps 20190913_sample_list.txt --mbseqs 20190913_primerindex.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190909 --demult qcat --samps 20190909_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190911 --demult qcat --samps 20190911_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190913 --demult qcat --samps 20190913_sample_list.txt --subset 100 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190909 --demult qcat --samps 20190909_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190911 --demult qcat --samps 20190911_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190913 --demult qcat --samps 20190913_sample_list.txt --subset 500 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta

python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190909 --demult qcat --samps 20190909_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190911 --demult qcat --samps 20190911_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
python devo_wrapper.py --datID 20190913 --demult qcat --samps 20190913_sample_list.txt --subset 5000 --perthresh 0.1 --db Sept2019_Sanger_cytb.fasta
