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


