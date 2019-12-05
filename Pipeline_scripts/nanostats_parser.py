#!/usr/bin/env python3
# ---------------------------------------------
# Marisa Lim
# Parsing NanoPlot read stats from full
# datasets (not subsets), make table
#
# Nov 2019
# ---------------------------------------------

import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser(
    description='''Parse NanoPlot NanoStats.txt files. Make table.''',
    epilog='''Example: python nanostats_parser.py
    --dat 20190909
    --demult minibar
    --npdir ./2b_demultiplexed/20190909_demultiplexed_NanoPlots/
    --output_dir ./2b_demultiplexed/'''
)
parser.add_argument('--dat', help='dataset ID')
parser.add_argument('--demult', help='the demultiplexing software used')
parser.add_argument('--filtstat', help='filtered or not. Options: y, n', required=True)
parser.add_argument('--npdir', help='Directory path with NanoStats.txt files', required=True)
parser.add_argument('--output_dir', help='Output directory', required=True)
args=parser.parse_args()
arg_dict=vars(args)

# extract the top lines with stats
# formulate into table

if arg_dict['filtstat'] == 'y':
    nanostat_list = []
    for nanostat in Path(arg_dict['npdir']).rglob('*_filtered_demNanoStats.txt'):
        # print(nanostat)
        thesamp = str(nanostat).split('_filtered_demNanoStats.txt')[0].split('/')[-1]
        # print(thesamp)
        thedemult = str(nanostat).split('_filtered_demNanoStats.txt')[0].split('_demultiplexouts')[0].split('_')[-1]
        print(thedemult)
        df = pd.read_csv(nanostat, sep=':').iloc[:7,]
        df.columns=['GeneralSummary', 'Value']
        df2 = df.set_index('GeneralSummary').transpose()
        df2['SampID'] = thesamp
        df2['Demult'] = thedemult
        # print(df2)
        nanostat_list.append(df2)
    nanostat_concat = pd.concat(nanostat_list, axis=0, sort=False)
    print(nanostat_concat)
    nanostat_concat.to_csv(arg_dict['output_dir']+arg_dict['dat']+'_'+arg_dict['demult']+'_allsamps_filtnanostats.txt', sep='\t', index=False)
elif arg_dict['filtstat'] == 'n':
    nanostat_list = []
    for nanostat in Path(arg_dict['npdir']).rglob('*_demNanoStats.txt'):
        # print(nanostat)
        thesamp = str(nanostat).split('_demult_demNanoStats.txt')[0].split('/')[-1]
        # print(thesamp)
        thedemult = str(nanostat).split('_demult_demNanoStats.txt')[0].split('_demultiplexouts')[0].split('_')[-1]
        print(thedemult)
        df = pd.read_csv(nanostat, sep=':').iloc[:7,]
        df.columns=['GeneralSummary', 'Value']
        df2 = df.set_index('GeneralSummary').transpose()
        df2['SampID'] = thesamp
        df2['Demult'] = thedemult
        # print(df2)
        nanostat_list.append(df2)
    nanostat_concat = pd.concat(nanostat_list, axis=0, sort=False)
    print(nanostat_concat)
    nanostat_concat.to_csv(arg_dict['output_dir']+arg_dict['dat']+'_'+arg_dict['demult']+'_allsamps_demultnanostats.txt', sep='\t', index=False)
