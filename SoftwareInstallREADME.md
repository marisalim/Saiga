# Advice for SAIGA software installation

One of the easiest ways to install python libraries (and other software) is to use conda install from Anaconda.
- Download Anaconda3: https://www.anaconda.com/distribution/. We want Anaconda3 so that it downloads Python3. Follow installation instructions from website.
- Once you have anaconda, configure the conda command to tell it where to look online for software. It does not matter what directory you’re in. 
  - `conda config --add channels bioconda`
  - `conda config --add channels conda-forge`

## Basecall: Guppy
https://community.nanoporetech.com/downloads
-	I downloaded Mac OSX version

The downloaded file is zipped and must be unzipped to use:
- `unzip ont-guppy-cpu_2.3.1_osx64.zip`
- Add guppy to bashrc path (`export PATH=$PATH:[your path]/ont-guppy-cpu/bin`)

## Read filtering: Nanofilt
https://github.com/wdecoster/nanofilt

- Use conda to install, enter:
  - `conda install -c bioconda nanofilt`
- Runs as NanoFilt <flags>
  - this was originally having problem before I added bioconda channel to conda
 
## Read stats: NanoPlot
https://github.com/wdecoster/NanoPlot

- Download the zipped folder of the github repository from green button that says ‘Clone or download’
- Unzip folder: `unzip NanoPlot-master.zip`
- Set up NanoPlot:
  - `cd ./NanoPlot-master`
  - `python setup.py develop`
- Runs as NanoPlot <inputs>
  - Pip and conda installation commands both timed out – not sure if the enSilo protection is blocking installation (it says it blocks python3.6 process). So used above steps as work-around

## Demultiplex: Qcat
https://github.com/nanoporetech/qcat
- downloaded via git clone option (v1.1.0)
- Add qcat to bashrc path (`export PATH=$PATH:[your path]/qcat`)

## Demultiplex: MiniBar
https://github.com/calacademy-research/minibar

- Download MiniBar: `curl https://raw.githubusercontent.com/calacademy-research/minibar/master/minibar.py`
- Permit execution of MiniBar’s python script: `chmod 775 minibar.py`
- minibar.py needs python library called edlib. Note that this differs from edlib, which is a command line version that works in Unix/Linux environment rather than Python.
  - `conda install -c bioconda python-edlib`
- Add MiniBar to bashrc path (`export PATH=$PATH:[your path]/MiniBar/`)
 
## Generate data subsets: seqtk
https://github.com/lh3/seqtk

- follow github installation instructions
- Add to bashrc path (`export PATH=$PATH:[your path]/seqtk`)
 
## Cluster reads: isONclust
https://github.com/ksahlin/isONclust

- download: `pip install isONclust`
 
## Generate consensus sequence from isONclust read clusters: Spoa
https://github.com/rvaser/spoa

- `git clone --recursive https://github.com/rvaser/spoa spoa`
- `cd spoa`
- `mkdir build`
- `cd build`
- `cmake -DCMAKE_BUILD_TYPE=Release -Dspoa_build_executable=ON ..`
- `make`
- Add spoa to bashrc path (`export PATH=$PATH:[your path]/spoa/build/bin/`)
 
## Cluster spoa consensus sequences: cd-hit-est
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

## Error correcton: Medaka
https://github.com/nanoporetech/medaka

- `conda create -n medaka -c conda-forge -c bioconda medaka`
- Medaka now has its own conda environment, which means you have to activate/deactivate the environment to run medaka:
  - `conda activate medaka`
  - `conda deactivate`
- if you get an error about numpy, I had to roll back the version of a library called openblas.
  - `conda install openblas=0.3.6`
- Runs as `medaka_consensus`

## Species ID check: Blast search
https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download

- Follow download instructions from NCBI
- Add ncbi-blast to bashrc path (`export PATH=$PATH:[your path]/ncbi-blast-2.8.1+/bin`)

## Map reads to references: Minimap2
https://github.com/lh3/minimap2

- Download from github: `git clone https://github.com/lh3/minimap2`
- Compile code: `cd minimap2 && make`
- Add minimap2 path to bashrc path (`export PATH=$PATH:[your path]/minimap2`)



