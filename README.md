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


## Picking parameters <a name="params"></a>

## Run Saiga! <a name="runpipe"></a>
1. Download this Github repository.
1. Set up directories
```
python setuppipe.py
```

## Run demo data <a name="demo"></a>
Go to `Demo/` for instructions.

## Run your data <a name="yourdat"></a>
1. Set up data inputs.
  - *Move MinKNOW files to 0_MinKNOW_rawdata folder.* The files for a given dataset should be in their own folder within the 0_MinKNOW_rawdata folder.
  - *Create sample list text file, save it in the 2a_samp_lists folder.* The file must be named with `[year][month][day]_sample_list.txt`, where the date info is the day of the sequencing run (you could name it whatever you want, but my scripts use this label to keep track of files from different sequence runs). The file is tab-delimited. It requires the sample name, barcoding gene, amplicon length, and ONT index. One line per sample.
  - *Create a fasta file with your Sanger sequences, save it in the Blast_resources folder.* Each sequence header should have the sample name, species identifier, and barcoding gene. This is for the blast step.

2. Basecall
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
