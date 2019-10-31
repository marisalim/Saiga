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
    --spoaseqs ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/all_clstr_conseqs.fasta
    --output_dir ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/'''
)

parser.add_argument('--sampID', help='Sample ID name', required=True)
parser.add_argument('--isocount', help='isONclust reads per cluster tally text file', required=True)
parser.add_argument('--cdhitclstrs', help='cd-hit cluster file', required=True)
parser.add_argument('--spoaseqs', help='concatenated spoa consensus seq fasta', required=True)
parser.add_argument('--output_dir', help='Output directory', required=True)
args=parser.parse_args()
arg_dict=vars(args)

print('Tally of isONclust reads per cluster...')
isonclstcount = pd.read_csv(str(arg_dict['isocount']), sep=' ', header=None)
isonclstcount.columns = ['NumReads', 'ClstrID']
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
        myls2.append(mycdhit.split('Cluster_')[1])
cdhit_df2 = pd.DataFrame(list(zip(myls, myls2)), columns=['ClstrID', 'cdhit'])
# need to convert dtype from object to numeric in order to merge dfs below
cdhit_df2['ClstrID'] = pd.to_numeric(cdhit_df2['ClstrID'])
print(cdhit_df2)

df = isonclstcount.merge(cdhit_df2, on='ClstrID')
print(df)
print('--------------------------------------------------')
print('Great! Now, we will calculate the number of reads that form')
print('majority cluster by both isONclust & cd-hit.')
print('By definition, the first row value for cdhit cluster ID, will')
print('correspond to the isONclust cluster with the greatest number of reads.')
print('Therefore, we can subset all the rows that match the top row cdhit')
print('cluster ID and sum over the NumReads column to get total # reads.')
mycdhitID = df.iloc[0,2]
subsetdf = df.loc[df['cdhit'] == mycdhitID,]
print(subsetdf)
clstrID_ls = subsetdf['ClstrID'].tolist()
# print(clstrID_ls)
print('Total num reads for top clusters: ', sum(subsetdf['NumReads']))

print('Now, we can take the spoa consensus sequences for these top cluster(s)')
print('to create a master consensus sequence for the draft assembly used by Medaka.')
spoa_conseq = SeqIO.parse(open(str(arg_dict['spoaseqs'])),'fasta')
with open(str(arg_dict['output_dir']) + 'formedaka.fasta', 'w') as out_file:
    for fasta in spoa_conseq:
        name, sequence = fasta.id, str(fasta.seq)
        # print(name)
        for clstr in clstrID_ls:
            fullclstrID = 'clstr' + str(clstr) + '|'
            # print(fullclstrID)
            if fullclstrID in name:
                SeqIO.write(fasta, out_file, 'fasta')
print('Great! Now, you can run spoa on the forspoaround2.fasta file and feed that to Medaka!')
