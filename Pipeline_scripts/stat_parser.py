#!/usr/bin/env python3
# ---------------------------------------------
# Marisa Lim
# Parsing blast of consensus results from isONclust > minimap2 > racon > blast
# Outputs for each sample:
#   Table with read counts from start to finish of pipeline, blast results for best match, and species ID
# Sample = sequenced sample name
# Raw_count = number of reads in raw fastq file
# Demultiplexed_count = number of reads left for this sample after demultiplexing
# Cluster_count = number of reads in the isONclust clusters and cd-hit clusters
# rep_seq = representative sequence read ID
# genbank = genbank accession ID for best match in consensus to blast db
# per_id = blast % identity of rep seq to NCBI/Sanger ref sequence
# aln_len = blast alignment length of rep seq to NCBI/Sanger ref seq
# num_mismatch = blast number of mismatches between consensus and blast db seq
# evalue = blast e-value (smaller numbers indicate better match)
# bitscore = blast bit score (larger numbers indicate better match)
# sp_name = species name of NCBI/Sanger ref seq for blast match
# consensus_seq = the final consensus sequence from Medaka
# Oct 2019
# ---------------------------------------------

import os, sys, argparse
import pandas as pd
from Bio import SeqIO

parser = argparse.ArgumentParser(
    description='''Parse blast results by # reads, coverage, and % identity to ref seqs.
    Make table.''',
    epilog='''Example: python stat_parser.py
    --sampID feather1
    --blastout ./4_spID/20190909_minibar100_spID/mk_feather1/feather1blastout.sorted
    --blastdbheaders ./Blast_resources/Sept2019_Sanger_cytb.fastaHEADERS.txt
    --rawfq ./1_basecalled/20190909_guppybasecallouts/20190909.fastq
    --demultfq ./2b_demultiplexed/20190909_minibar_demultiplexouts/20190909_100sub/20190909feather1_filtered100.fastq
    --isocount ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/reads_per_cluster.text
    --cdhitclstrs ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/cdhit_feather1.fasta.clstr
    --mkout ./4_spID/20190909_minibar100_spID/mk_feather1/consensus.fasta
    --output_dir ./4_spID/20190909_minibar100_spID/mk_feather1/'''
)

parser.add_argument('--sampID', help='Sample ID name', required=True)
parser.add_argument('--blastout', help='blastout.sorted file from Blast output after medaka', required=True)
parser.add_argument('--blastdbheaders', help='Header file from database used in blast search', required=True)
parser.add_argument('--rawfq', help='raw concatenated reads fastq file', required=True)
parser.add_argument('--demultfq', help='length & quality score filtered demultiplexed read fastq file', required=True)
parser.add_argument('--isocount', help='isONclust reads per cluster tally text file', required=True)
parser.add_argument('--cdhitclstrs', help='cd-hit cluster file', required=True)
parser.add_argument('--mkout', help='Medaka consensus sequence fasta', required=True)
parser.add_argument('--output_dir', help='Output directory', required=True)
args=parser.parse_args()
arg_dict=vars(args)

# 0. Calculate read counts through pipeline
print('Tallying raw data read count...')
raw_count = 0
for line in open(str(arg_dict['rawfq']), 'r'):
    raw_count += 1
raw_count2 = int(raw_count/4)
print('raw read count: ', raw_count2)
print('--------------------------------------------------')

print('Tallying data after demultiplexing and filtering...')
read_counter = 0
for line in open(str(arg_dict['demultfq']), 'r'):
    read_counter += 1
dem_reads = int(read_counter/4)
print('demultiplexed reads: ', dem_reads)
print('--------------------------------------------------')

print('Tally of isONclust reads per cluster...')
isonclstcount = pd.read_csv(str(arg_dict['isocount']), sep=' ', header=None)
isonclstcount.columns = ['NumReads', 'IsoID']
isonclstcount['PerReads'] = round(isonclstcount['NumReads']/sum(isonclstcount['NumReads']), 2)
isonclstcount['CumSum'] = pd.Series(isonclstcount['PerReads']).cumsum()
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
# print(cdhit_df)
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
cdhit_df2 = pd.DataFrame(list(zip(myls, myls2)), columns=['IsoID', 'cdhit'])
# need to convert dtype from object to numeric in order to merge dfs below
cdhit_df2['IsoID'] = pd.to_numeric(cdhit_df2['IsoID'])
# print(cdhit_df2)

df = isonclstcount.merge(cdhit_df2, on='IsoID')
print(df)
print('--------------------------------------------------')
print('Great! Now, we will calculate the number of reads that form')
print('majority cluster by both isONclust & cd-hit.')
print('By definition, the first row value for cdhit cluster ID, will')
print('correspond to the isONclust cluster with the greatest number of reads.')
print('Therefore, we can subset all the rows that match the top row cdhit')
print('cluster ID and sum over the NumReads column to get total # reads.')
mycdhitID = df.iloc[0,4]
subsetdf = df.loc[df['cdhit'] == mycdhitID,]
print(subsetdf)
clstrID_ls = subsetdf['IsoID'].tolist()
# print(clstrID_ls)
clstr_sum = sum(subsetdf['NumReads'])
print('Total num reads for top clusters: ', clstr_sum)

prop_reads = round(clstr_sum/dem_reads, 4)

readcount_dict = {'Sample': str(arg_dict['sampID']),
'Raw_count':int(raw_count2),
'Demultiplexed_count':int(dem_reads),
'isONclust_count':int(clstr_sum),
'prop_demreads_inclstr':float(prop_reads)
}
readcount_df=pd.DataFrame(readcount_dict, index=[0])
print(readcount_df)
print('--------------------------------------------------')

# 0. extract Medaka consensus sequence
medaka_cons = SeqIO.parse(open(str(arg_dict['mkout'])),'fasta')
medaka_seqs = []
for fasta in medaka_cons:
    name, sequence = fasta.id, str(fasta.seq)
    medaka_seqs.append(sequence)
print('Consensus sequence list (currently, should only be 1 sequence!): ', medaka_seqs)
print('----------------------------------------------------------------------------------')

# 1. extracted all headers from blastdb file and create dataframe with accession number and species name
header_dat = pd.read_csv(str(arg_dict['blastdbheaders']), sep=' ', header=None)
header_dat.columns = ['genbank', 'db_sp_name']
print(header_dat.head(5))
print('--------------------------------------------------')

# 2. Parse blast info
# check if file is empty
if os.stat(arg_dict['blastout']).st_size != 0:
    blastdat = pd.read_csv(arg_dict['blastout'], sep='\t', header=None)
    blastdat.columns = ['query', 'genbank', 'per_id', 'aln_len', 'num_mismatch', 'gap_open', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    print(blastdat)

    # sort by bitscore to get the top hit (should get result with top %ID, length, evalue)
    # retain all blast output information
    print('Sorting blast results by highest bitscore... keeping top 5 results ...')
    top_hit = blastdat.sort_values(by=['bitscore'], ascending=False)[0:5]
    print('Sorting blast results by lowest number of mismatches... keeping top result ...')
    top_hit2 = top_hit.sort_values(by=['num_mismatch'], ascending=True)[0:1]
    print(top_hit2)

    # 3. Add species name information to blast output
    # match up with accession number in blast output
    df = pd.merge(top_hit2, header_dat, on='genbank')
    print(df)

    # 4. Add in the count info & consensus sequence
    df2 = pd.concat([readcount_df, df], axis=1)
    df2['MkConsSeq'] = medaka_seqs[0]
    print(df2)
    df2.to_csv(arg_dict['output_dir']+arg_dict['sampID']+'_finalparsed_output.txt', sep='\t')
    print('_finalparsed_output.txt is the final parsed output file.')
    print('--------------------------------------------------')

# if file is empty
elif os.stat(arg_dict['blastout']).st_size == 0:
    print('Empty file. No blast results to parse.')
