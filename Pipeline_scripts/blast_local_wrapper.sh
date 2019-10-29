#!/usr/bin/env bash

# Blast search
# database = Sanger sequences
# query = Nanopore reads

source ~/.bashrc

mydatabase=$1
myquery=$2
myoutput=$3

# check if this exists, otherwise skip
if [ -e $mydatabase.nhr ]
then
  echo 'database already exists'
  echo 'do blast search'
  blastn -query $myquery -db $mydatabase -evalue 1e-10 -outfmt 6 -out $myoutput.txt
  echo 'sort blast search by highest seq similarity'
  sort -rnk3 $myoutput.txt > $myoutput.sorted
  rm $myoutput.txt

else
  echo 'make database'
  makeblastdb -dbtype nucl -parse_seqids -in $mydatabase
  echo 'do blast search'
  blastn -query $myquery -db $mydatabase -evalue 1e-10 -outfmt 6 -out $myoutput.txt
  echo 'sort blast search by highest seq similarity'
  sort -rnk3 $myoutput.txt > $myoutput.sorted
  rm $myoutput.txt
fi
