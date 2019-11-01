#!/usr/bin/env python3
# ---------------------------------------------
# Marisa Lim
# Parsing the isONclust cluster files to
# create a table of reads/cluster from isONclust, isONclust cluster ID, and % reads/cluster
#
# Oct 2019
# ---------------------------------------------

import os, argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description='''Parse cluster outputs from isONclust and cd-hit.
    Make table.''',
    epilog='''Example: python isonclust_parser.py
    --sampID feather1
    --perthresh .1
    --isocount ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/reads_per_cluster.text
    --scripthome ./Pipeline_scripts
    --output_dir ./3_readclustering/20190909_minibar100readclstrs/feather1_clstrs/'''
)

parser.add_argument('--sampID', help='Sample ID name', required=True)
parser.add_argument('--perthresh', help='Filter out clusters with fewer percent reads than this threshold')
parser.add_argument('--isocount', help='isONclust reads per cluster tally text file', required=True)
parser.add_argument('--scripthome', help='provide path for spoafy.sh', required=True)
parser.add_argument('--output_dir', help='Output directory', required=True)
args=parser.parse_args()
arg_dict=vars(args)

print('Tally of isONclust reads per cluster...')
isonclstcount = pd.read_csv(str(arg_dict['isocount']), sep=' ', header=None)
isonclstcount.columns = ['NumReads', 'IsoID']
isonclstcount['PerReads'] = round(isonclstcount['NumReads']/sum(isonclstcount['NumReads']), 2)
isonclstcount['CumSum'] = pd.Series(isonclstcount['PerReads']).cumsum()
print(isonclstcount)

print('Only keep clusters with >= percent reads/cluster threshold you chose...')
subsetdf = isonclstcount.loc[isonclstcount['PerReads'] >= float(arg_dict['perthresh']),]
print(subsetdf)

myclstrIDsforspoa = subsetdf['IsoID'].tolist()
print('Cluster IDs to generate spoa consensus sequences from: ', myclstrIDsforspoa)

# Run spoa from here --
print('Make spoa consensus sequence for majority read isONclust clusters...')
for clstr in myclstrIDsforspoa:
    spoainput = arg_dict['output_dir'] + 'clstr_fqs/' + str(clstr) + '.fastq'
    commands = """
    echo 'spoa-fying: {1}'
    bash {0}/spoafy.sh {1}
    """.format(arg_dict['scripthome'], spoainput)
    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)
