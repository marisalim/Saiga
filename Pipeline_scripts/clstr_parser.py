#!/usr/bin/env python3
# ---------------------------------------------
# Marisa Lim
# Parsing the isONclust and cd-hit cluster files to
# create a table of reads/cluster from isONclust, isONclust cluster ID, and cluster org from cd-hit
# use this table to check for reverse complement sequences
# and what to use for reference in Medaka
#
# Oct 2019
# ---------------------------------------------

import argparse
import pandas as pd
from Bio import SeqIO

parser = argparse.ArgumentParser(
    description='''Parse cluster outputs from isONclust and cd-hit.
    Make table.''',
    epilog='''Example: python clstr_parser.py
    --sampID feather1
    --isocount ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/reads_per_cluster.text
    --cdhitclstrs ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/cdhit_feather1.fasta.clstr
    --output_dir ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/'''
)

parser.add_argument('--sampID', help='Sample ID name', required=True)
parser.add_argument('--isocount', help='isONclust reads per cluster tally text file', required=True)
parser.add_argument('--cdhitclstrs', help='cd-hit cluster file', required=True)
parser.add_argument('--output_dir', help='Output directory', required=True)
args=parser.parse_args()
arg_dict=vars(args)

print('Tally of isONclust reads per cluster...')
isonclstcount = pd.read_csv(str(arg_dict['isocount']), sep=' ', header=None)
isonclstcount.columns = ['NumReads', 'ClstrID']
isonclstcount.ClstrID.astype(str)
print(isonclstcount)
print('--------------------------------------------------')

print('Tally reads in majority cluster...(cd-hit >Cluster_0)')
fasta_sequences = SeqIO.parse(open(str(arg_dict['cdhitclstrs'])),'fasta')
clstr_counter = 0
cdhit_name = []
cdhit_clstrs = []
for fasta in fasta_sequences:
    name, sequence = fasta.id, str(fasta.seq)
    name2 = name + '_' + str(clstr_counter)
    cdhit_name.append(name2)
    cdhit_clstrs.append(sequence)
    clstr_counter += 1
cdhit_df = pd.DataFrame(list(zip(cdhit_name, cdhit_clstrs)),
               columns =['cdhit_clstr_IDs', 'iso_clstr_IDs'])
print(cdhit_df)
print('--------------------------------------------------')
print('Now, extract the isONclust clstr IDs from the cd-hit output...')
myls = []
myls2 = []
for i in cdhit_df.index:
    mycdhit = cdhit_df.at[i, 'cdhit_clstr_IDs']
    myiso = cdhit_df.at[i, 'iso_clstr_IDs']
    # print(myiso)
    for j in range(0, myiso.count('>')):
        clstrID = myiso.split('|Consensus...')[j].split('>clstr')[1]
        # print(clstrID
        myls.append(clstrID)
        myls2.append(mycdhit)
cdhit_df2 = pd.DataFrame(list(zip(myls, myls2)), columns=['ClstrID', 'cdhit'])
cdhit_df2.ClstrID.astype(str)
print(cdhit_df2)

df = pd.merge(isonclstcount, cdhit_df2, on='ClstrID')
print(df)

----------------------------------------------------------------------
START HERE -- run below to test this code
cd /Users/marisalim/Desktop/SPpipe2019/3_readclustering/20190906_qcat100readclstrs/FFPEqleo_clstrs
python ../../../Pipeline_scripts/clstr_parser.py --sampID FFPEqleo --isocount reads_per_cluster.txt --cdhitclstrs cdhit_FFPEqleo.fasta.clstr --output_dir ./

have this error from the pd.merge():
ValueError: You are trying to merge on int64 and object columns. If you wish to proceed you should use pd.concat
----------------------------------------------------------------------



# maybe use the top spoa consensus sequences and build a master consensus for Medaka?
