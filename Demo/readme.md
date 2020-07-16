# Running SAIGA demo dataset

0. Set up pipeline directories:
- `python setuppipe.py`

1. The demo files need to be moved to correct pipeline directories:
- Download demo files
- Move the entire `demo_guppybasecallouts` directory to `1_basecalled`
  - unzip the fastq files. In bash terminal, you can enter: `for file in *.fastq.gz; do gunzip $file; done`
- Move `demo_primerindex.txt` and `demo_sample_list.txt` to `2a_samp_lists`
- Move `demo.fasta` to `Blast_resources`

2. Run pipeline:
- Open the `run_saiga.sh` script. Edit python command as needed for script options. Demo dataset commands are at the top.
- Run: `bash run_saiga.sh`

3. Check output results:
- Outputs from Blast search are in `4_spID`, as [ ]_allsamps_parsedout.txt files

# Example outputs

Demo data uses first 20 basecalled fastq files of the 9/6/2019 dataset. Results are copied from _allsamps_parsedout.txt files from FinalResults/ folder. See SAIGA_demo_results.txt for demo results (demultiplexed with qcat or MiniBar, full demo data or 500 read subset).

# Example commands from demo data

```
# qcat, full demo dataset
SAIGA command:	python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100 --subset none --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta

# minibar, full demo dataset
SAIGA command:	python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs demo_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset none --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta

# qcat, 500 read subsets
SAIGA command:	python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001 --qs 7 --buffer 100 --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta

# minibar, 500 read subsets
SAIGA command:	python saiga_wrapper.py --dat demo --samps demo_sample_list.txt --rawNP y --demultgo y --filt y --subgo y --clust y --demult minibar --mbseqs demo_primerindex.txt --mb_idx_dist 2 --mb_pr_dist 11 --qs 7 --buffer 100 --subset 500 --subseed 100 --perthresh 0.1 --cdhitsim 0.8 --db demo.fasta
```
