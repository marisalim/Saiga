# ---------------------------------------------
# Marisa Lim
# this is developer version. user-friendly features in progress! logs would be nice..

# Steps:
# 1. Basecall # run this outside of the script, since it takes so long. Here, just run the cat function for guppy output fastq files.
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
# - NanoFilt v2.5.0
# - qcat v1.1.0
# - MiniBar v0.21
# - seqtk v1.3-r106
# - isONclust v0.0.4
# - spoa v3.0.1
# - cd-hit-est v4.8.1
# - medaka v0.10.0
# - NCBI blast v2.8.1+

# November 2019
# ---------------------------------------------

# load packages
import os, sys, argparse
import time
import datetime
import pandas as pd
from pathlib import Path
import glob

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

    print('Done plotting NanoPlots.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('Take a look at the read length and read quality distributions.')
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

    print('Rename demultiplexed files according to sample name instead of index name.')
    index_samp_dict = dict(zip(samp_files.indexID, samp_files.sampleID))
    # print(index_samp_dict)
    for files in os.listdir(demultiplexed_path):
        filename = files.split('.')[0]
        if filename in index_samp_dict:
            newfilename = index_samp_dict[filename]
            print('Old file name:', filename, '; New file name:', newfilename)
            os.rename(demultiplexed_path + files, demultiplexed_path + datasetID + newfilename+'.fastq')
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

    print('MiniBar splits up ONT indexed samples into 2 files for some reason. Need to concatenate.')
    for i in samp_files.index:

        mysamps = samp_files.loc[i, 'sampleID']
        # print(mysamps)

        commands2="""
        cat {0}{1}{2}*fastq > {0}{1}{2}.fastq.concat
        echo 'Printing line counts per fastq file...'
        for file in {0}{1}{2}*; do echo $file; grep '^@' $file | wc -l; done
        rm {0}{1}{2}*.fastq
        echo 'Use NanoFilt to remove any empty read lines. Otherwise, these will give TypeError when'
        echo 'you try to filter by both quality and read length'
        cat {0}{1}{2}.fastq.concat | NanoFilt -l 10 > {0}{1}{2}.fastq
        rm {0}{1}{2}.fastq.concat
        """.format(demultiplexed_path, datasetID, mysamps)

        command_list2 = commands2.split('\n')
        for cmd in command_list2:
            os.system(cmd)

    print('Done demultiplexing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

# 3. NanoFilt by quality and length
def filter_demultiplexed_reads(demultiplexed_path, datasetID, samp_files, min_filter_quality, read_len_buffer):
    print('######################################################################')
    print('Filter demultiplexed reads with NanoFilt.')
    print('This step is to remove low quality reads and any adapters, reads')
    print('that got trimmed too short after indexes/primers removed,')
    print('and any chimeric reads that are too long')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_files.index:
        myfastqfile = demultiplexed_path + datasetID + samp_files.at[i,'sampleID'] + '.fastq'
        filteredfilename = demultiplexed_path + datasetID + samp_files.at[i,'sampleID'] + '_filtered.fastq'

        # print(myfastqfile)
        # print(filteredfilename)

        gene_length = samp_files.at[i, 'gene_len'].item() # the .item() is to make numpy int a native py int to match type() of read_len_buffer
        min_filter_len = gene_length - int(read_len_buffer)
        max_filter_len = gene_length + int(read_len_buffer)

        log_name = demultiplexed_path + datasetID + samp_files.at[i,'sampleID'] + '.log'

        rawfq_counter = 0
        for line in open(myfastqfile, 'r'):
            rawfq_counter += 1
        raw_reads = rawfq_counter/4

        # note: renaming unk.fastq and non.fastq files so they work with script for NanoPlot (need the '_' because used as a delimiter)
            # want to see read stats for the uncategorized reads
        commands = """
        echo '-------------------------'
        echo 'For demultiplexed files in: {0}'
        echo 'Filtering: {1}'
        echo 'Quality score: {3}'
        echo 'Min length: {4}'
        echo 'Max length: {5}'
        echo 'Log file name: {6}'
        cat {1} | NanoFilt -q {3} -l {4} --maxlength {5} --logfile {6} > {2}
        echo 'Renaming uncategorized read files...'
        if [ -f '{0}{7}unk.fastq' ]; then mv {0}{7}unk.fastq {0}{7}unk_notfiltered.fastq; fi
        if [ -f '{0}none.fastq' ]; then mv {0}none.fastq {0}none_notfiltered.fastq; fi
        """.format(demultiplexed_path, myfastqfile, filteredfilename, min_filter_quality, min_filter_len, max_filter_len, log_name, datasetID)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)

        # count reads in raw vs. filtered
        # calculate reads retained vs. lost after filtering
        print('How many reads were lost after filtering?')
        filteredfq_counter = 0
        for line in open(filteredfilename, 'r'):
            filteredfq_counter += 1
        filtered_reads = filteredfq_counter/4
        print('Raw reads: ', raw_reads)
        print('Filtered reads: ', filtered_reads)

        lost_reads = raw_reads - filtered_reads
        percent_lost = round((lost_reads/raw_reads)*100, 3)
        percent_retained = round((1-(lost_reads/raw_reads))*100, 3)
        print('% reads lost: ', percent_lost)
        print('% reads retained: ', percent_retained)

    print('Done filtering demultiplexed reads.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

# 4. Build subsets
#     - options: none (will analyze full dataset demult reads), int (will build random subsets using this num of reads)
def build_subs(scripthome, demultiplexed_path, datasetID, samp_files, mysub, subdir):
    print('######################################################################')
    print('Create data subset for each sample')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_files.index:
        myfastqfile = datasetID + samp_files.at[i,'sampleID'] + '_filtered'

        commands="""
        echo 'Running script: {0}/seqtk_subsetter.sh'
        echo 'Subsetting from: {4}{1}'
        echo 'Output directory: {3}'
        echo '-------------------------------------------------------------'
        bash {0}/seqtk_subsetter.sh {2} {1} {3} {4}
        echo '-------------------------------------------------------------'
        """.format(scripthome, myfastqfile, mysub, subdir, demultiplexed_path)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)

        print('######################################################################')

# 5. NanoPlot demult and filtered reads
def demultiplexed_nanoplots(toplotpath, NanoPlot_demultiplexedout_path):
        print('######################################################################')
        print('Create NanoPlots for all demultiplexed sample fastq files')
        print('(before filtering) for full datasets. Does not make sense to')
        print('plot demultiplexed but not filtered stats for subsets since')
        print('subsets generated after filtering reads.')
        print('######################################################################')
        sys.stdout.flush()
        time.sleep(1.0)

        for thefastqs in os.listdir(toplotpath):
            if '_filtered.fastq' not in thefastqs:
                mysampname = thefastqs.split('.')[0]

                commands = """
                echo 'For demultiplexed files in: {0}'
                echo 'Plotting NanoPlot for sample: {2}.fastq'
                echo 'NanoPlot outputs: {1}'
                echo 'NanoPlot outputs ID: {2}_dem'
                echo '-------------------------------------------------------------'
                NanoPlot --fastq {0}/{2}.fastq -o {1} -p {2}_dem --plots kde
                """.format(toplotpath, NanoPlot_demultiplexedout_path, mysampname)

                command_list = commands.split('\n')
                for cmd in command_list:
                    os.system(cmd)

        print('Done plotting NanoPlots.')
        sys.stdout.flush()
        time.sleep(0.5)
        print('Take a look at the read length, read quality distributions, and number of reads per sample.')
        sys.stdout.flush()
        time.sleep(0.5)
        print('######################################################################')

def filtered_nanoplots(toplotpath, NanoPlot_filteredout_path):
    print('######################################################################')
    print('Create NanoPlots for all filtered demultiplexed sample fastq files.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for thefastqs in os.listdir(toplotpath):
        if '_filtered.fastq' in thefastqs:
            mysampname = thefastqs.split('.')[0]

            commands = """
            echo 'For demultiplexed files in: {0}'
            echo 'Plotting NanoPlot for sample: {2}.fastq'
            echo 'NanoPlot outputs: {1}'
            echo 'NanoPlot outputs ID: {2}_dem'
            echo '-------------------------------------------------------------'
            NanoPlot --fastq {0}/{2}.fastq -o {1} -p {2}_dem --plots kde
            """.format(toplotpath, NanoPlot_filteredout_path, mysampname)

            command_list = commands.split('\n')
            for cmd in command_list:
                os.system(cmd)

    print('Done plotting NanoPlots.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('Take a look at the read length, read quality distributions, and number of reads per sample.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

def fulldat_nanostats(scripthome, demultiplexed_path, datasetID, thedemult, toppath):
    print('######################################################################')
    print('Extract Nano Stats for full datasets from NanoPlot outputs:')
    print('number of demultiplexed reads, avg quality and length')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    commands="""
    echo '-------------------------------------------------------------'
    python {0}/nanostats_parser.py \
    --npdir {1}/{2}_demultiplexed_NanoPlots/ \
    --output_dir {4}/2b_demultiplexed/ \
    --dat {2} --demult {3} --filtstat n
    echo '-------------------------------------------------------------'
    python {0}/nanostats_parser.py \
    --npdir {1}/{2}_filtered_NanoPlots/ \
    --output_dir {4}/2b_demultiplexed/ \
    --dat {2} --demult {3} --filtstat y
    """.format(scripthome, demultiplexed_path, datasetID, thedemult, toppath)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)

    print('######################################################################')

# 6. Generate clusters, count reads per cluster
def read_clstr_cons(scripthome, toppath, demultiplexed_path, datasetID, samp_files, thesub, thedemult, myperthresh, cdhit_seqsim_thresh):
    print('######################################################################')
    print('Read clustering with isONclust, consensus seq with spoa,')
    print('check reverse comp with cd-hit-est, and error correct with Medaka.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_files.index:

        mysamp = samp_files.at[i, 'sampleID']
        if thesub == 'none':
            fastqfile = demultiplexed_path + datasetID + samp_files.at[i, 'sampleID']+ '_filtered.fastq'
            # print(fastqfile)
        else:
            fastqfile = demultiplexed_path + datasetID + '_' + str(thesub) + 'sub/' + datasetID + samp_files.at[i, 'sampleID']+ '_filtered' + str(thesub) + '.fastq'
            # print(fastqfile)

        commands = """
        if [ ! -d '{1}/3_readclustering/{2}_{3}{4}readclstrs' ]; \
        then mkdir {1}/3_readclustering/{2}_{3}{4}readclstrs; fi
        echo 'Input fastq: {5}'
        echo 'Output folder: {1}/3_readclustering/{2}_{3}{4}readclstrs'
        echo '-------------------------------------------------------------'
        echo 'Clustering...'
        isONclust --fastq {5} --ont --outfolder {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/
        echo 'Writing isONclust cluster fastqs...'
        isONclust write_fastq --clusters {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/final_clusters.csv \
        --fastq {5} --outfolder {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/clstr_fqs/ --N 1
        echo 'Count reads per cluster...(also, remove space in front of number of reads)'
        cut -f 1 {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/final_clusters.csv | sort -n | uniq -c | sort -rn | sed 's/^[ \t]*//;s/[ \t]*$//' > {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/reads_per_cluster.txt
        python {0}/isonclust_parser.py --sampID {6} --perthresh {7} \
        --isocount {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/reads_per_cluster.txt \
        --scripthome {0} \
        --output_dir {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/
        echo '-------------------------------------------------------------'
        """.format(scripthome, toppath, datasetID, thedemult, str(thesub), fastqfile, mysamp, myperthresh, cdhit_seqsim_thresh)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)

        # if spoa files exist, move on, otherwise, move on to next sample with error
        spoa_path = toppath + '/3_readclustering/' + datasetID + '_' + thedemult+str(thesub)+'readclstrs/'+mysamp +'_clstrs/clstr_fqs/'
        if len(glob.glob(spoa_path + '*_spoa.fasta')) != 0:
            commands2 = """
            echo 'Make combined consensus seq file...'
            cat {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/clstr_fqs/*_spoa.fasta > {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/all_clstr_conseqs.fasta
            echo '-------------------------------------------------------------'
            echo 'Check for reverse/complement...'
            bash {0}/revcomp_check.sh {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/all_clstr_conseqs.fasta {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/cdhit_{6}.fasta {8}
            python {0}/clstr_parser.py --sampID {6} \
            --isocount {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/reads_per_cluster.txt \
            --cdhitclstrs {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/cdhit_{6}.fasta.clstr \
            --spoaseqs {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/all_clstr_conseqs.fasta \
            --output_dir {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/
            """.format(scripthome, toppath, datasetID, thedemult, str(thesub), fastqfile, mysamp, myperthresh, cdhit_seqsim_thresh)

            command_list2 = commands2.split('\n')
            for cmd in command_list2:
                os.system(cmd)

            # if subset clstr file exists, move on, otherwise move to next sample after error msg
            if glob.glob(toppath + '/3_readclustering/'+datasetID + '_' + thedemult+str(thesub)+'readclstrs/'+mysamp +'_clstrs/final_clusters_subset.csv') != 0:
                commands3 = """
                echo 'Next, generate new write_fastq file as input for Medaka...'
                isONclust write_fastq --clusters {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/final_clusters_subset.csv \
                --fastq {5} --outfolder {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/readsformedaka --N 1
                echo 'Make fasta sequential instead of interleaved...'
                bash {0}/fastaformatter.sh \
                {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/formedaka.fasta \
                {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/formedaka_singleline.fasta
                echo '-------------------------------------------------------------'
                echo 'Error correction with Medaka...'
                bash {0}/medaka_corr.sh {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/readsformedaka/0.fastq {1}/3_readclustering/{2}_{3}{4}readclstrs/{6}_clstrs/formedaka_singleline.fasta {1}/4_spID/{2}_{3}{4}_spID/mk_{6}
                """.format(scripthome, toppath, datasetID, thedemult, str(thesub), fastqfile, mysamp, myperthresh, cdhit_seqsim_thresh)

                command_list3 = commands3.split('\n')
                for cmd in command_list3:
                    os.system(cmd)

            elif glob.glob(toppath + '/3_readclustering/'+datasetID + '_' + thedemult+str(thesub)+'readclstrs/'+mysamp +'_clstrs/final_clusters_subset.csv') == 0:
                print('WARNING! Read cd-hit threshold too high, no clusters. Please adjust the cdhitsim parameter (but must be >= 0.8).')
                print('Check results for: ', mysamp)
                pass

        elif glob.glob(spoa_path + '*_spoa.fasta') == 0:
            print('WARNING! Read clusters are smaller than your threshold. Please adjust the perthresh parameter. No spoa files made.')
            print('Check results for: ', mysamp)
            pass

    print('Done with read clustering, consensus building, & error correcting.')
    print('######################################################################')

# 7. Check species ID
def blastoff(scripthome, toppath, datasetID, samp_files, thesub, thedemult, blastdb):
    print('######################################################################')
    print('Check species ID of Medaka consensus sequence via Blast')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_files.index:
        mysamp = samp_files.at[i, 'sampleID']

        commands="""
        echo 'Blast database: {6}'
        echo 'Blast searching...'
        bash {0}/blast_local_wrapper.sh \
        {6} \
        {1}/4_spID/{2}_{3}{4}_spID/mk_{5}/consensus.fasta \
        {1}/4_spID/{2}_{3}{4}_spID/mk_{5}/{5}blastout
        """.format(scripthome, toppath, datasetID, thedemult, str(thesub), mysamp, blastdb)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)
    print('######################################################################')

# Parse outputs...
def stat_parse(scripthome, toppath, basecallout_path, demultiplexed_path, datasetID, samp_files, thesub, thedemult, blastdb):
    print('######################################################################')
    print('Parse outputs, calculate ID stats.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    header_commands = """
    echo 'Make blast db header file if does not exist'
    if [ ! -d '{0}HEADERS.txt' ]; then grep '>' {0} | bash {1}/blast_header.sh > {0}HEADERS.txt; fi
    """.format(blastdb, scripthome)

    header_list = header_commands.split('\n')
    for cmd in header_list:
        os.system(cmd)

    for i in samp_files.index:
        mysamp = samp_files.at[i, 'sampleID']

        commands = """
        echo '-------------------------------------------------------------'
        echo 'Running script: {0}/stat_parser.py'
        echo '-------------------------------------------------------------'
        echo 'Parsing data...'
        python {0}/stat_parser.py \
        --sampID {5} \
        --blastout {1}/4_spID/{4}_{6}{7}_spID/mk_{5}/{5}blastout.sorted \
        --blastdbheaders {8}HEADERS.txt \
        --rawfq {2}/{4}.fastq \
        --demultfq {3}/{4}_{7}sub/{4}{5}_filtered{7}.fastq \
        --isocount {1}/3_readclustering/{4}_{6}{7}readclstrs/{5}_clstrs/reads_per_cluster.txt \
        --cdhitclstrs {1}/3_readclustering/{4}_{6}{7}readclstrs/{5}_clstrs/cdhit_{5}.fasta.clstr \
        --mkout {1}/4_spID/{4}_{6}{7}_spID/mk_{5}/consensus.fasta \
        --output_dir {1}/4_spID/{4}_{6}{7}_spID/mk_{5}/
        """.format(scripthome, toppath, basecallout_path, demultiplexed_path, datasetID, mysamp, thedemult, thesub, blastdb)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)

    # create a concatenated file for all the final_parsed_output files
    # this will be the single input with read count info to R script for
    # making the sequence run summary report with markdown
    filelist = []
    for parsed_out in Path(toppath+'/4_spID/'+datasetID+'_'+thedemult+thesub+'_spID/').rglob('*_finalparsed_output.txt'):
        df = pd.read_csv(parsed_out, header=0, sep='\t')
        filelist.append(df)
    frame = pd.concat(filelist, axis=0, sort=False)
    frame.drop('Unnamed: 0', axis='columns').to_csv(toppath+'/FinalResults/'+datasetID+'_'+thedemult+thesub+'_allsamps_parsedout.txt', sep='\t', index=False)

    print('Done parsing, check outputs!')
    print('######################################################################')

def stat_parse_fulldat(scripthome, toppath, basecallout_path, demultiplexed_path, datasetID, samp_files, thesub, thedemult, blastdb):
        print('######################################################################')
        print('Parse outputs, calculate ID stats.')
        print('######################################################################')
        sys.stdout.flush()
        time.sleep(1.0)

        header_commands = """
        echo 'Make blast db header file if does not exist'
        if [ ! -d '{0}HEADERS.txt' ]; then grep '>' {0} | bash {1}/blast_header.sh > {0}HEADERS.txt; fi
        """.format(blastdb, scripthome)

        header_list = header_commands.split('\n')
        for cmd in header_list:
            os.system(cmd)

        for i in samp_files.index:
            mysamp = samp_files.at[i, 'sampleID']

            commands = """
            echo '-------------------------------------------------------------'
            echo 'Running script: {0}/stat_parser.py'
            echo '-------------------------------------------------------------'
            echo 'Parsing data...'
            python {0}/stat_parser.py \
            --sampID {5} \
            --blastout {1}/4_spID/{4}_{6}{7}_spID/mk_{5}/{5}blastout.sorted \
            --blastdbheaders {8}HEADERS.txt \
            --rawfq {2}/{4}.fastq \
            --demultfq {3}{4}{5}_filtered.fastq \
            --isocount {1}/3_readclustering/{4}_{6}{7}readclstrs/{5}_clstrs/reads_per_cluster.txt \
            --cdhitclstrs {1}/3_readclustering/{4}_{6}{7}readclstrs/{5}_clstrs/cdhit_{5}.fasta.clstr \
            --mkout {1}/4_spID/{4}_{6}{7}_spID/mk_{5}/consensus.fasta \
            --output_dir {1}/4_spID/{4}_{6}{7}_spID/mk_{5}/
            """.format(scripthome, toppath, basecallout_path, demultiplexed_path, datasetID, mysamp, thedemult, thesub, blastdb)

            command_list = commands.split('\n')
            for cmd in command_list:
                os.system(cmd)

        # create a concatenated file for all the final_parsed_output files
        # this will be the single input with read count info to R script for
        # making the sequence run summary report with markdown
        filelist = []
        for parsed_out in Path(toppath+'/4_spID/'+datasetID+'_'+thedemult+thesub+'_spID/').rglob('*_finalparsed_output.txt'):
            df = pd.read_csv(parsed_out, header=0, sep='\t')
            filelist.append(df)
        frame = pd.concat(filelist, axis=0, sort=False)
        frame.drop('Unnamed: 0', axis='columns').to_csv(toppath+'/FinalResults/'+datasetID+'_'+thedemult+thesub+'_allsamps_parsedout.txt', sep='\t', index=False)

        print('Done parsing, check outputs!')
        print('######################################################################')

def main():
    print('Run pipeline! To see options, enter: ')
    print('python devo_wrapper.py -h')
    print('######################################################################')

    ## set up args
    parser = argparse.ArgumentParser(
        description='''Developer master MinION barcoding pipeline for species ID script''',
        epilog='''Example: python devo_wrapper.py
        --dat 20190906 --samps 20190906_sample_list.txt
        --rawNP n --demultgo n --filt n --subgo y --clust y
        --demult qcat --qcat_minscore 99 --ONTbarcodekit PBC001
        --qs 7 --buffer 100 --subset 100 --perthresh 0.1 --cdhitsim 0.8 --db Sept2019_Sanger_cytb.fasta''')
    parser.add_argument('--datID', help='dataset identifer; typically yearmonthdate (e.g., 20190906 for Sept 6, 2019)', required=True)
    parser.add_argument('--samps', help='tab-delimited text file of sample names, barcode, barcode length, index name', required=True)
    parser.add_argument('--rawNP', help='Option to generate NanoPlots for raw reads. Options: y, n', required=True)
    parser.add_argument('--demultgo', help='Option to demultiplex reads. Options: y, n. Requires --demult; MiniBar: --mbseqs, --mb_idx_dist, --mb_pr_dist; qcat: --qcat_minscore, --ONTbarcodekit flags', required=True)
    parser.add_argument('--filt', help='Option to filter demultiplexed reads. Options: y, n', required=True)
    parser.add_argument('--subgo', help='Option to make random data subsets. Options: y, n. Requires --subset flag', required=True)
    parser.add_argument('--clust', help='Option to cluster and Blast. Options: y, n. Requires --demult, --subset, --perthresh, and --db flags', required=True)
    parser.add_argument('--demult', help='Options: qcat, minibar')
    parser.add_argument('--mbseqs', help='For MiniBar demultiplexing, input barcode and primer seqs')
    parser.add_argument('--mb_idx_dist', help='MiniBar index edit distance (e.g., 2)')
    parser.add_argument('--mb_pr_dist', help='MiniBar primer edit distance (e.g., 11)')
    parser.add_argument('--qcat_minscore', help='qcat minimum alignment score (0-100 scale)')
    parser.add_argument('--ONTbarcodekit', help='ONT barcode kit (e.g., PBC001). Required for qcat.')
    parser.add_argument('--qs', help='Phred quality score threshold to filter reads by')
    parser.add_argument('--buffer', help='Buffer length +/- amplicon length to filter reads by')
    parser.add_argument('--subset', help='Options: none OR integer subset of reads to be randomly selected (e.g., 500)')
    parser.add_argument('--perthresh', help='Percent read threshold for keeping isONclust clusters (e.g., 0.1 for keeping clusters with >= 10%% of reads)')
    parser.add_argument('--cdhitsim', help='Sequence similarity threshold for cd-hit-est to cluster reads by')
    parser.add_argument('--db', help='Blast reference database fasta file')

    args=parser.parse_args()
    arg_dict=vars(args)

    ## set up commonly used paths and files
    toppath = os.getcwd() #this gets current working directory path
    scripthome = toppath + '/Pipeline_scripts'
    basecallout_path = toppath + '/1_basecalled/' + arg_dict['datID'] + '_guppybasecallouts'
    NanoPlot_basecallout_path = toppath + '/1_basecalled/' + arg_dict['datID'] + '_raw_NanoPlots/'
    demultiplexed_path = toppath + '/2b_demultiplexed/' + arg_dict['datID'] + '_' + arg_dict['demult'] + '_demultiplexouts/'

    samp_files=pd.read_csv(toppath + '/2a_samp_lists/' + str(arg_dict['samps']), sep='\t', header=None)
    if len(samp_files.columns) != 4:
        print('Check sample_list input file. There should be 4 columns.')
        sys.exit()
    elif len(samp_files.columns) == 4:
        samp_files.columns=['sampleID', 'gene', 'gene_len', 'indexID']
        primerindex=toppath + '/2a_samp_lists/' + str(arg_dict['mbseqs'])

        ## Run functions!
        if arg_dict['rawNP'] == 'y':
            raw_read_nanoplots(scripthome, basecallout_path, NanoPlot_basecallout_path, arg_dict['datID'])
        elif arg_dict['rawNP'] == 'n':
            pass # move on to next step

        if arg_dict['demultgo'] == 'y':
            if arg_dict['demult'] == 'qcat':
                barcode_kit = arg_dict['ONTbarcodekit']
                my_qcat_minscore = arg_dict['qcat_minscore']
                print('Input files...')
                print(samp_files)
                Qcat_demultiplexing(scripthome, basecallout_path, demultiplexed_path, arg_dict['datID'], barcode_kit, my_qcat_minscore, samp_files)
            if arg_dict['demult'] == 'minibar':
                myindex_editdist = arg_dict['mb_idx_dist']
                myprimer_editdist = arg_dict['mb_pr_dist']
                print('Input files...')
                print(samp_files)
                if len(pd.read_csv(primerindex, sep='\t').columns) != 11:
                    print('Check minibar primerindex input file. There should be 11 columns.')
                    sys.exit()
                elif len(pd.read_csv(primerindex, sep='\t').columns) == 11:
                    print(pd.read_csv(primerindex, sep='\t'))
                    print(demultiplexed_path)
                    MiniBar_demultiplexing(scripthome, basecallout_path, demultiplexed_path, arg_dict['datID'], myindex_editdist, myprimer_editdist, primerindex, samp_files)
        elif arg_dict['demultgo'] == 'n':
            pass

        if arg_dict['filt'] == 'y':
            read_len_buffer = arg_dict['buffer']
            min_filter_quality = arg_dict['qs']
            filter_demultiplexed_reads(demultiplexed_path, arg_dict['datID'], samp_files, min_filter_quality, read_len_buffer)
        elif arg_dict['filt'] =='n':
            pass

        if arg_dict['subgo'] == 'y':
            if arg_dict['subset'] == 'none':
                print('No subsetting, continuing to next step...')
                NanoPlot_demultiplexedout_path = toppath + '/2b_demultiplexed/' + arg_dict['datID'] + '_' + arg_dict['demult'] + '_demultiplexouts/' + arg_dict['datID'] + '_demultiplexed_NanoPlots/'
                NanoPlot_filteredout_path = toppath + '/2b_demultiplexed/' + arg_dict['datID'] + '_' + arg_dict['demult'] + '_demultiplexouts/' + arg_dict['datID'] + '_filtered_NanoPlots/'
                toplotpath = demultiplexed_path
                demultiplexed_nanoplots(toplotpath, NanoPlot_demultiplexedout_path)
                filtered_nanoplots(toplotpath, NanoPlot_filteredout_path)
                fulldat_nanostats(scripthome, demultiplexed_path, arg_dict['datID'], arg_dict['demult'], toppath)
            else:
                print('Subsetting demultiplexed reads by your subset choice...')
                mysub = int(arg_dict['subset'])
                print('Subset size: ', mysub)
                subdir = demultiplexed_path + arg_dict['datID'] + '_' + str(mysub) + 'sub'
                build_subs(scripthome, demultiplexed_path, arg_dict['datID'], samp_files, mysub, subdir)

                print('Note: currently code does not output NanoPlots for uncategorized reads if you chose to generate data subsets.')
                NanoPlot_filteredout_path = subdir + '/' + arg_dict['datID'] + '_filtered_NanoPlots/'
                toplotpath = subdir + '/'
                filtered_nanoplots(toplotpath, NanoPlot_filteredout_path)
        elif arg_dict['subgo'] == 'n':
            pass

        if arg_dict['clust'] == 'y':
            if arg_dict['subset'] == 'none':
                print('No subsetting, continuing to next step...')
                cdhit_seqsim_thresh = arg_dict['cdhitsim']
                read_clstr_cons(scripthome, toppath, demultiplexed_path, arg_dict['datID'], samp_files, arg_dict['subset'], arg_dict['demult'], arg_dict['perthresh'], cdhit_seqsim_thresh)

                blastdb=toppath + '/Blast_resources/' + str(arg_dict['db'])
                blastoff(scripthome, toppath, arg_dict['datID'], samp_files, arg_dict['subset'], arg_dict['demult'], blastdb)

                stat_parse_fulldat(scripthome, toppath, basecallout_path, demultiplexed_path, arg_dict['datID'], samp_files, arg_dict['subset'], arg_dict['demult'], blastdb)
            else:
                print('Using demultiplexed reads by your subset choice...')
                mysub = arg_dict['subset']
                print('Subset size: ', mysub)
                cdhit_seqsim_thresh = arg_dict['cdhitsim']
                read_clstr_cons(scripthome, toppath, demultiplexed_path, arg_dict['datID'], samp_files, arg_dict['subset'], arg_dict['demult'], arg_dict['perthresh'], cdhit_seqsim_thresh)

                blastdb=toppath + '/Blast_resources/' + str(arg_dict['db'])
                blastoff(scripthome, toppath, arg_dict['datID'], samp_files, arg_dict['subset'], arg_dict['demult'], blastdb)

                stat_parse(scripthome, toppath, basecallout_path, demultiplexed_path, arg_dict['datID'], samp_files, arg_dict['subset'], arg_dict['demult'], blastdb)
        elif arg_dict['clust'] == 'n':
            pass

if __name__ == "__main__":
    main()
