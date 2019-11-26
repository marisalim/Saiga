# SAIGA: A user-friendly DNA barcoding bioinformatics pipeline for MinION sequencing

Our pipeline is called SAIGA to help bring awareness to Saiga (*Saiga tatarica*) conservation.

If you use our pipeline, please cite:

-----------
[top](#top)
# Table of contents
1. [Dependencies](#Dependencies)
    1. [Software installation advice](#installadvice)
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

<a href="#top">Back to top</a>

### Software installation advice <a name="installadvice"></a>
One of the easiest ways to install python libraries (and other software) is to use conda install from Anaconda.
- Download Anaconda3: https://www.anaconda.com/distribution/. We want Anaconda3 so that it downloads Python3. Follow installation instructions from website.
- Once you have anaconda, configure the conda command to tell it where to look online for software. It does not matter what directory you’re in.
  - `conda config --add channels bioconda`
  - `conda config --add channels conda-forge`

Note that this pipeline relies on certain software being called via `source ~/.bashrc`.

#### Basecall: Guppy
https://community.nanoporetech.com/downloads
-	I downloaded Mac OSX version

The downloaded file is zipped and must be unzipped to use:
- `unzip ont-guppy-cpu_2.3.1_osx64.zip`
- Add guppy to bashrc path (`export PATH=$PATH:[your path]/ont-guppy-cpu/bin`)

#### Read filtering: Nanofilt
https://github.com/wdecoster/nanofilt

- Use conda to install, enter:
  - `conda install -c bioconda nanofilt`
- Runs as NanoFilt <flags>
  - this was originally having problem before I added bioconda channel to conda

#### Read stats: NanoPlot
https://github.com/wdecoster/NanoPlot

- Download the zipped folder of the github repository from green button that says ‘Clone or download’
- Unzip folder: `unzip NanoPlot-master.zip`
- Set up NanoPlot:
  - `cd ./NanoPlot-master`
  - `python setup.py develop`
- Runs as NanoPlot <inputs>
  - Pip and conda installation commands both timed out – not sure if the enSilo protection is blocking installation (it says it blocks python3.6 process). So used above steps as work-around

#### Demultiplex: Qcat
https://github.com/nanoporetech/qcat
- downloaded via git clone option (v1.1.0)
- Add qcat to bashrc path (`export PATH=$PATH:[your path]/qcat`)

#### Demultiplex: MiniBar
https://github.com/calacademy-research/minibar

- Download MiniBar: `curl https://raw.githubusercontent.com/calacademy-research/minibar/master/minibar.py`
- Permit execution of MiniBar’s python script: `chmod 775 minibar.py`
- minibar.py needs python library called edlib. Note that this differs from edlib, which is a command line version that works in Unix/Linux environment rather than Python.
  - `conda install -c bioconda python-edlib`
- Add MiniBar to bashrc path (`export PATH=$PATH:[your path]/MiniBar/`)

#### Generate data subsets: seqtk
https://github.com/lh3/seqtk

- follow github installation instructions
- Add to bashrc path (`export PATH=$PATH:[your path]/seqtk`)

#### Cluster reads: isONclust
https://github.com/ksahlin/isONclust

- download: `pip install isONclust`

#### Generate consensus sequence from isONclust read clusters: Spoa
https://github.com/rvaser/spoa

- `git clone --recursive https://github.com/rvaser/spoa spoa`
- `cd spoa`
- `mkdir build`
- `cd build`
- `cmake -DCMAKE_BUILD_TYPE=Release -Dspoa_build_executable=ON ..`
- `make`
- Add spoa to bashrc path (`export PATH=$PATH:[your path]/spoa/build/bin/`)

#### Cluster spoa consensus sequences: cd-hit-est
https://github.com/weizhongli/cdhit/wiki/2.-Installation

- cd-hit-est needs gcc: `brew install gcc`
- download tar.gz file
- `tar xvf cd-hit-v4.6.6-2016-0711.tar.gz --gunzip`
- `cd cd-hit-v4.8.1-2019-0228`
- `make CC=/usr/local/Cellar/gcc/9.1.0/bin/g++-9`
- `make`
- `cd cd-hit-auxtools/`
- `make`
- Add cd-hit to bashrc path (`export PATH=$PATH:[your path]/cd-hit-v4.8.1-2019-0228`)

#### Error correcton: Medaka
https://github.com/nanoporetech/medaka

- `conda create -n medaka -c conda-forge -c bioconda medaka`
- Medaka now has its own conda environment, which means you have to activate/deactivate the environment to run medaka:
  - `conda activate medaka`
  - `conda deactivate`
- if you get an error about numpy, I had to roll back the version of a library called openblas.
  - `conda install openblas=0.3.6`
- Runs as `medaka_consensus`

#### Species ID check: Blast search
https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download

- Follow download instructions from NCBI
- Add ncbi-blast to bashrc path (`export PATH=$PATH:[your path]/ncbi-blast-2.8.1+/bin`)

<a href="#top">Back to top</a>

## Formatting input files <a name="inputs"></a>
- See `Demo/` for example input files.
- *Move MinKNOW files to 0_MinKNOW_rawdata folder.* The files for a given dataset should be in their own folder within the 0_MinKNOW_rawdata folder.
- *Create sample list text file, save it in the 2a_samp_lists folder.* The file must be named with `[year][month][day]_sample_list.txt`, where the date info is the day of the sequencing run (you could name it whatever you want, but my scripts use this label to keep track of files from different sequence runs). The file is tab-delimited. It requires the sample name, barcoding gene, amplicon length, and ONT index. One line per sample.
- *Create a fasta file with your Sanger sequences, save it in the Blast_resources folder.* Each sequence header should have the sample name, species identifier, and barcoding gene. This is for the blast step.

<a href="#top">Back to top</a>

## Picking parameters <a name="params"></a>
The pipeline is written to allow you to run different steps without rerunning certain analyses over and over. The first time the pipeline is run, you'll need to analyze the raw basecalled files with `--rawNP`, demultiplex samples with `--demultgo`, and filter reads with `--filt`.

Saiga was written to implement demultiplexing by either qcat (`--demult qcat`) or MiniBar (`--demult minibar`). To run qcat, you must set the `--min_score` and `--ONTbarcodekit` flags. To run MiniBar, you must set the `--mbseqs`, `--mb_idx_dist`, and `--mb_pr_dist` flags. Descriptions below.

The pipeline filters reads by read quality Phred score with the `--qs` flag. Read length is filtered with the `--buffer` length you set around the amplicon length provided in your input `sample_list.txt` file.

Next, you can choose to analyze the full dataset (`--subgo y --subset none`) or subsets of the data (`--subgo y --subset 500` for 500 read sample of the data).

To complete the pipeline analysis, use the `--clust` flag. You need to specify the demultiplexer (`--demult`), the subset (`--subset`), a threshold for the minimum number of reads per cluster (`--perthresh`), a minimum cluster similarity threshold (`--cdhitsim`), and a fasta file with sequences you'd like to compare consensus sequences to (`--db`).

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

<a href="#top">Back to top</a>

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

<a href="#top">Back to top</a>

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

<a href="#top">Back to top</a> :fireworks:
