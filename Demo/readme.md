# Running SAIGA demo dataset

0. Set up pipeline directories:
- `python setuppipe.py`

1. The demo files need to be moved to correct pipeline directories:
- Download demo files
- Move the entire `demo_guppybasecallouts` directory to `1_basecalled`
- Move `demo_primerindex.txt` and `demo_sample_list.txt` to `2a_samp_lists`
- Move `demo.fasta` to `Blast_resources`

2. Run pipeline:
- Open the `run_saiga.sh` script. Edit python command as needed for script options. Demo dataset commands are at the top.
- Run: `bash run_saiga.sh`

3. Check output results:
- Outputs from Blast search are in `4_spID`, as [ ]_allsamps_parsedout.txt files


