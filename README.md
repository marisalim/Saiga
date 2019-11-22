# SAIGA: A user-friendly DNA barcoding bioinformatics pipeline for MinION sequencing

Our pipeline is called SAIGA to help bring awareness to Saiga (*Saiga tatarica*) conservation. 

If you use our pipeline, please cite: 

-----------

# Dependencies:
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
bash pipe_batcher.sh
```
4. Generate MS figures/tables with ClstrfqFigsTables.rmd


