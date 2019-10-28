# SP2019_pipe
new pipeline Oct/Nov 2019 for MinION barcoding

## New installations

### Spoa
- spoa builds consensus sequences - this is replacing the step of choosing a representative sequence from isONclust
- install:
```
cd SPpipe2019

git clone --recursive https://github.com/rvaser/spoa spoa
cd spoa
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -Dspoa_build_executable=ON ..
make
```
- add spoa to `bashrc` paths
```
nano ~/.bashrc
# add /Users/marisalim/Desktop/SPpipe2019/spoa/build/bin
source ~/.bashrc # to run
```

### Medaka
- Medaka is an ONT error correction software - this is replacing racon
- install:
```
conda create -n medaka -c conda-forge -c bioconda medaka
```
- creates its own conda environment, which means you have to activate/deactivate the environment to run medaka
```
conda activate medaka
conda deactivate
```

- if you get this error, you need to change `openblas` version (see https://github.com/numpy/numpy/issues/14165)
```
Traceback (most recent call last):
  File "/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/__init__.py", line 16, in <module>
    from . import multiarray
  File "/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/multiarray.py", line 12, in <module>
    from . import overrides
  File "/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/overrides.py", line 6, in <module>
    from numpy.core._multiarray_umath import (
ImportError: dlopen(/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/_multiarray_umath.cpython-36m-darwin.so, 2): Library not loaded: @rpath/libopenblas.dylib
  Referenced from: /anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/_multiarray_umath.cpython-36m-darwin.so
  Reason: image not found

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/anaconda3/envs/medaka/bin/medaka", line 7, in <module>
    from medaka.medaka import main
  File "/anaconda3/envs/medaka/lib/python3.6/site-packages/medaka/medaka.py", line 7, in <module>
    import numpy as np
  File "/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/__init__.py", line 142, in <module>
    from . import core
  File "/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/__init__.py", line 47, in <module>
    raise ImportError(msg)
ImportError: 

IMPORTANT: PLEASE READ THIS FOR ADVICE ON HOW TO SOLVE THIS ISSUE!

Importing the multiarray numpy extension module failed.  Most
likely you are trying to import a failed build of numpy.
Here is how to proceed:
- If you're working with a numpy git repository, try `git clean -xdf`
  (removes all files not under version control) and rebuild numpy.
- If you are simply trying to use the numpy version that you have installed:
  your installation is broken - please reinstall numpy.
- If you have already reinstalled and that did not fix the problem, then:
  1. Check that you are using the Python you expect (you're using /anaconda3/envs/medaka/bin/python),
     and that you have no directories in your PATH or PYTHONPATH that can
     interfere with the Python and numpy versions you're trying to use.
  2. If (1) looks fine, you can open a new issue at
     https://github.com/numpy/numpy/issues.  Please include details on:
     - how you installed Python
     - how you installed numpy
     - your operating system
     - whether or not you have multiple versions of Python installed
     - if you built from source, your compiler versions and ideally a build log

     Note: this error has many possible causes, so please don't comment on
     an existing issue about this - open a new one instead.

Original error was: dlopen(/anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/_multiarray_umath.cpython-36m-darwin.so, 2): Library not loaded: @rpath/libopenblas.dylib
  Referenced from: /anaconda3/envs/medaka/lib/python3.6/site-packages/numpy/core/_multiarray_umath.cpython-36m-darwin.so
  Reason: image not found
```
  - change version of openblas:
  ```
  conda install openblas=0.3.6
  medaka_consensus # now shows the medaka_consensus options
  ```
  
# Run pipeline

1. Set up directories
```
python setuppipe.py
```
2. Basecall
```
cd Pipeline_scripts
bash guppy_basecalling_wrapper.sh [MinKNOW dat dir] [output dir] [Pipeline home path]
```
3. Run rest of pipeline with devo_wrapper.py
```
# qcat version
python devo_wrapper.py --datID 20190906 --demult qcat --samps 20190906_sample_list.txt 

# minibar version
python devo_wrapper.py --datID 20190906 --demult minibar --samps 20190906_sample_list.txt --mbseqs 20190906_primerindex.txt 

```
