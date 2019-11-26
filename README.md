# SAIGA: A user-friendly DNA barcoding bioinformatics pipeline for MinION sequencing

Our pipeline is called SAIGA to help bring awareness to Saiga (*Saiga tatarica*) conservation.

If you use our pipeline, please cite:

-----------

# Table of contents
1. [Dependencies](#Dependencies)
2. [Input files](#inputs)
3. [Choose parameters](#params)
4. [Run Saiga](#runpipe)
    1. [Demo data](#demo)
    2. [Your data](#yourdat)

## Software dependencies <a name="Dependencies"></a>
- Guppy v3.1.5+781ed575
- NanoPlot v1.21.0
- NanoFilt v2.5.0
- qcat v1.1.0
- MiniBar v0.21
- seqtk v1.3-r106
- isONclust v0.0.4
- spoa v3.0.1
- cd-hit-est v4.8.1
- medaka v0.10.0
- NCBI blast v2.8.1+

See `SoftwareInstallREADME.md` for advice on software installations. Note that this pipeline relies on certain software being called via `source ~/.bashrc`.

## Input file formatting <a name="inputs"></a>
- *Move MinKNOW files to 0_MinKNOW_rawdata folder.* The files for a given dataset should be in their own folder within the 0_MinKNOW_rawdata folder.
- *Create sample list text file, save it in the 2a_samp_lists folder.* The file must be named with `[year][month][day]_sample_list.txt`, where the date info is the day of the sequencing run (you could name it whatever you want, but my scripts use this label to keep track of files from different sequence runs). The file is tab-delimited. It requires the sample name, barcoding gene, amplicon length, and ONT index. One line per sample.
- *Create a fasta file with your Sanger sequences, save it in the Blast_resources folder.* Each sequence header should have the sample name, species identifier, and barcoding gene. This is for the blast step.

## Picking parameters <a name="params"></a>

REQUIRED flags:

Flag | Description
--- | ---
--datID | dataset identifer; typically yearmonthdate (e.g., 20190906 for Sept 6, 2019)
--samps | tab-delimited text file of sample names, barcode, barcode length, index name (e.g., 20190906_sample_list.txt)
--rawNP | Option to generate NanoPlots for raw reads. Options: y, n
--demultgo | Option to demultiplex reads. Options: y, n. MiniBar requires --demult, --mbseqs, --mb_idx_dist, --mb_pr_dist. Qcat requires --qcat_minscore, --ONTbarcodekit flags
--filt | Option to filter demultiplexed reads. Options: y, n. Requires --qs, --buffer flags
--subgo | Option to make random data subsets. Options: y, n. Requires --subset flag
--clust | Option to cluster and Blast. Options: y, n. Requires --demult, --subset, --perthresh, --db flags

Additional flags:

Flag | Description
--- | ---
--demult | Options: qcat, minibar
--mbseqs | For MiniBar demultiplexing, input barcode and primer seqs file (e.g., 20190906_primerindex.txt)
--mb_idx_dist | MiniBar index edit distance (e.g., 2)
--mb_pr_dist | MiniBar primer edit distance (e.g., 11)
--qcat_minscore | qcat minimum alignment score (0-100 scale)
--ONTbarcodekit | ONT barcode kit (e.g., PBC001)
--qs | Phred quality score threshold to filter reads by
--buffer | Buffer length +/- amplicon length to filter reads by
--subset | Options: none OR integer subset of reads to be randomly selected (e.g., 500)
--perthresh | Percent read threshold for keeping isONclust clusters (e.g., 0.1 for keeping clusters with >= 10% of reads)
--cdhitsim | Sequence similarity threshold for cd-hit-est to cluster reads by (e.g., 0.8 for clustering reads with at least 80% similarity)
--db | Blast reference database fasta file






## Run Saiga! <a name="runpipe"></a>
1. Download this Github repository.
1. Set up directories
```
python setuppipe.py
```

### Run demo data <a name="demo"></a>
1. Go to `Demo/` for input files. The demo files need to be moved to correct pipeline directories:
  - Download demo files
  - Move the entire `demo_guppybasecallouts` directory to `1_basecalled`
  - Move `demo_primerindex.txt` and `demo_sample_list.txt` to `2a_samp_lists`
  - Move `demo.fasta` to `Blast_resources`

2. Run pipeline:
  - Open the `pipe_batcher.sh` script. Edit python command as needed for script options. Demo dataset commands are at the top.
  - Run: `bash pipe_batcher.sh`

3. Check output results:
  - Outputs from Blast search are in `4_spID` (`allsamps_parsedout.txt` files)

### Run your data <a name="yourdat"></a>
1. Add your data input files.

2. Basecall MinKNOW files.
```
cd Pipeline_scripts
bash guppy_basecalling_wrapper.sh [MinKNOW dat dir] [output dir] [Pipeline home path]
```
3. Run rest of pipeline.
- *Edit `pipe_batcher.sh`:*
    - This is the script that runs through all the pipeline steps. You need to comment out the demo version commands (add ‘#’ to the beginning of the lines).
    - Then edit the python command `--` flags with appropriate dataset name, files, and parameter values. You need to set the following flags to `y` or `n` to tell the pipeline whether to:
      - `--rawNP`: concatenate raw basecalled fastq files, output NanoPlot stats
      - `--demultgo`: demultiplex reads
      - `--filt`: filter reads
      - `--subgo`: create subsets
      - `--clust`: cluster reads, generate consensus, blast to reference database
     - If you've run the top steps, and want to rerun the later steps, just switch the top ones to `n`. However, all these steps have to be run at least once!
```
bash pipe_batcher.sh
```

4. Check your results! :tada:
