# ---------------------------------------------
# Marisa Lim
#

# user inputs go into command instead of asking user throughout script
# this is developer version, not as user-friendly as .py wrapper with user input throughout script

# Steps:
# 1. Basecall # let's run this outside of the script for now, since it takes so long. Here, just run the cat function
#   and Nanoplot raw reads
# 2. Demultiplex - qcat vs. MiniBar
# 3. NanoFilt by quality and length
# 4. Build subsets - set flag for this,
#     - options: none (will analyze full dataset demult reads), int (will build subsets using this num of reads)
#     - if int, then decide whether you want a nested vs. random subset.
# 5. NanoPlot demult and filtered reads
# 6. Generate clusters, count reads per cluster
# 7. Make consensus sequence from clusters
# 8. Check for reverse complement
# 9. Error correct consensus
# 10. Check species ID

# Dependencies:
# - Guppy v3.1.5+781ed575
# - NanoPlot v1.21.0
# - NanoFilt v2.2.0
# - qcat v1.1.0
# - MiniBar v0.21
# - seqtk v1.3-r106
# - isONclust v0.0.4
# - spoa v3.0.1
# - cd-hit-est v4.8.1
# - medaka v0.10.0
# - NCBI blast v2.8.1+

# October/November 2019
# ---------------------------------------------

# load packages
import os, sys, argparse
import time
import datetime
import pandas as pd

# 1. Concat basecall files & make NanoPlots
def raw_read_nanoplots(scripthome, basecallout_path, NanoPlot_basecallout_path, datasetID):
    print('######################################################################')
    print('Concatenate basecalled fastq files and check NanoPlots.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    NanoPlot_out_name = datasetID + '_raw'

    commands = """
    echo 'Running script: {0}/concatfastq_nanoplots.sh'
    echo 'For basecalled files in: {1}'
    echo 'Concatenated fastq output file called: {2}.fastq'
    echo 'NanoPlot outputs: {3}'
    echo 'NanoPlot outputs ID: {4}'
    echo '-------------------------------------------------------------'
    bash {0}/concatfastq_nanoplots.sh {1} {2} {3} {4}
    """.format(scripthome, basecallout_path, datasetID, NanoPlot_basecallout_path, NanoPlot_out_name)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)
        # pipe_log_file.write(cmd)
        # pipe_log_file.write('\n')

    print('Done plotting NanoPlots.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('Take a look at the read length and read quality distributions before continuing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

# 2. Demultiplex - qcat vs. MiniBar
def Qcat_demultiplexing(scripthome, basecallout_path, demultiplexed_path, datasetID, barcode_kit, my_qcat_minscore, samp_files):
    print('######################################################################')
    print('Demultiplexing with Qcat.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    myfastqfile = datasetID + '.fastq'

    commands = """
    echo 'Running script: {0}/qcat_demultiplexing_wrapper.sh'
    echo 'Demultiplexing this file: {2}'
    echo 'Output directory: {5}'
    echo 'qcat min-score: {3}'
    echo 'qcat barcode kit: {4}'
    echo '-------------------------------------------------------------'
    bash {0}/qcat_demultiplexing_wrapper.sh {1} {2} {3} {4} {5} {6}
    echo '-------------------------------------------------------------'
    """.format(scripthome, datasetID, myfastqfile, my_qcat_minscore, barcode_kit, demultiplexed_path, basecallout_path)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)
        # pipe_log_file.write(cmd)
        # pipe_log_file.write('\n')

    print('Rename demultiplexed files according to sample name instead of index name.')
    index_samp_dict = dict(zip(samp_files.indexID, samp_files.sampleID))
    # print(index_samp_dict)
    for files in os.listdir(demultiplexed_path):
        filename = files.split('.')[0]
        if filename in index_samp_dict:
            newfilename = index_samp_dict[filename]
            print('Old file name:', filename, '; New file name:', newfilename)
            os.rename(demultiplexed_path + files, demultiplexed_path + newfilename+'.fastq')
        else:
            print(filename, ': this index not used, will not rename file')

    print('Done demultiplexing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

def MiniBar_demultiplexing(scripthome, basecallout_path, demultiplexed_path, datasetID, myindex_editdist, myprimer_editdist, primerindex, samp_files):
    print('######################################################################')
    print('Demultiplexing with MiniBar.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    myfastqfile = datasetID + '.fastq'

    commands = """
    echo 'Running script: {0}/minibar_demultiplexing_wrapper.sh'
    echo 'Index and primer file: {2}'
    echo 'Demultiplexing this file: {3}'
    echo 'Index edit distance: {4}'
    echo 'Primer edit distance: {5}'
    echo 'Output directory: {6}'
    echo '-------------------------------------------------------------'
    bash {0}/minibar_demultiplexing_wrapper.sh {1} {2} {3} {4} {5} {6} {7}
    echo '-------------------------------------------------------------'
    """.format(scripthome, datasetID, primerindex, myfastqfile, myindex_editdist, myprimer_editdist, demultiplexed_path, basecallout_path)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)
        # pipe_log_file.write(cmd)
        # pipe_log_file.write('\n')

    print('MiniBar splits up ONT indexed samples into 2 files for some reason. Need to concatenate.')
    for i in samp_files.index:

        mysamps = samp_files.loc[i, 'sampleID']
        print(mysamps)

        commands2="""
        cat {0}/{1}{2}*fastq > {0}/{1}{2}.fastq.concat
        rm {0}/{1}{2}*.fastq
        mv {0}/{1}{2}.fastq.concat {0}/{1}{2}.fastq
        """.format(demultiplexed_path, datasetID, mysamps)

        command_list2 = commands2.split('\n')
        for cmd in command_list2:
            os.system(cmd)

    print('Done demultiplexing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

# 4. NanoFilt by quality and length

START HERE!!!!



# 5. Build subsets - set flag for this,
#     - options: none (will analyze full dataset demult reads), int (will build subsets using this num of reads)
#     - if int, then decide whether you want a nested vs. random subset.




# 6. NanoPlot demult and filtered reads



# 7. Generate clusters, count reads per cluster




# 8. Make consensus sequence from clusters



# 9. Check for reverse complement



# 10. Error correct consensus



# 11. Check species ID



 # Parse outputs...

 # add logs
 # need to add read count trackers...


def main():
    print('Main function organizer...')

    # set up args
    parser = argparse.ArgumentParser(
        description='''Developer master MinION barcoding pipeline for species ID script''',
        epilog='''Example: python devo_wrapper.py
        --datID 20190906
        --demult minibar
        --samps 20190906_sample_list.txt
        --mbseqs 20190906_primerindex.txt
        --
        '''
)
    parser.add_argument('--datID', help='dataset identifer; typically yearmonthdate (e.g., 20190906 for Sept 6, 2019)', required=True)
    parser.add_argument('--demult', help='Options: qcat, minibar', required=True)
    parser.add_argument('--samps', help='tab-delimited text file of sample names, barcode, barcode length, index name', required=True)
    parser.add_argument('--mbseqs', help='For MiniBar demultiplexing, input barcode and primer seqs')
    # parser.add_argument('--')
    # parser.add_argument()
    # parser.add_argument()

    args=parser.parse_args()
    arg_dict=vars(args)

    # set up commonly used paths
    toppath = os.getcwd() #this gets current working directory path
    scripthome = toppath + '/Pipeline_scripts'
    basecallout_path = toppath + '/1_basecalled/' + arg_dict['datID'] + '_guppybasecallouts'
    NanoPlot_basecallout_path = toppath + '/1_basecalled/' + arg_dict['datID'] + '_raw_filt_NanoPlots/'
    demultiplexed_path = toppath + '/2b_demultiplexed/' + arg_dict['datID'] + '_' + arg_dict['demult'] + '_demultiplexouts/'
    NanoPlot_demultiplexedout_path = toppath + '/2b_demultiplexed/' + arg_dict['datID'] + '_' + arg_dict['demult'] + '_demultiplexouts/' + arg_dict['datID'] + '_demultiplexed_NanoPlots/'

    # Run functions!
    # raw_read_nanoplots(scripthome, basecallout_path, NanoPlot_basecallout_path, arg_dict['datID'])

    if arg_dict['demult'] == 'qcat':
        barcode_kit='PBC001'
        my_qcat_minscore='99'
        samp_files=pd.read_csv(toppath + '/2a_samp_lists/' + str(arg_dict['samps']), sep='\t', header=None)
        samp_files.columns=['sampleID', 'gene', 'gene_len', 'indexID']
        # print('Check input files...')
        # print(samp_files)
        # Qcat_demultiplexing(scripthome, basecallout_path, demultiplexed_path, arg_dict['datID'], barcode_kit, my_qcat_minscore, samp_files)

    if arg_dict['demult'] == 'minibar':
        myindex_editdist='2'
        myprimer_editdist='11'
        samp_files=pd.read_csv(toppath + '/2a_samp_lists/' + str(arg_dict['samps']), sep='\t', header=None)
        samp_files.columns=['sampleID', 'gene', 'gene_len', 'indexID']
        primerindex=toppath + '/2a_samp_lists/' + str(arg_dict['mbseqs'])
        # print('Check input files...')
        # print(samp_files)
        # print(pd.read_csv(primerindex, sep='\t'))
        # print(demultiplexed_path)
        # MiniBar_demultiplexing(scripthome, basecallout_path, demultiplexed_path, arg_dict['datID'], myindex_editdist, myprimer_editdist, primerindex, samp_files)






if __name__ == "__main__":
    main()
