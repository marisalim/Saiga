# run pipeline top to bottom!
# currently don't have a way to go back and rerun something within the script
# you'd have to close the script and then start over, but you can
# skip steps that you've already run

# Things that must be done before running pipeline:
# - move minknow fast5 files to 0_MinKNOW_rawdata/
# - add primer sequences and index sequence to minibar_input_config.py
    # - had thought about adding sampleID too, but
    # automating input file for MiniBar is hard
    # because it depends on # samples, which primers are being used, which index pairs are being used
    # - for now, the user just has to make this separately
# - create a sample list text file that just has single column with sample names
    # - these names are the same as those used for MiniBar input file

import os, sys
import time
import datetime
import pandas as pd

print('---------------------------------------------------------------------')
print('      <{{{<  ~~~           <(((< ~~~')
print('                                 ~~~    >)))>')
print('                                                      ~~~     >}}}>')
print('            Welcome to our prototype barcoding pipeline!')
print('                        Oct/Nov NEW pipeline')
print('Read clustering de novo reference pipeline with isONclust (single samples)')
print('      devo by Stefan Prost; this script by Marisa Lim 2019')
print('---------------------------------------------------------------------')
sys.stdout.flush()
time.sleep(0.5)

# set up global variables
toppath = os.getcwd() #this gets current working directory path
scripthome = toppath + '/Pipeline_scripts'

print('Fun name coming eventually - got any ideas?')
sys.stdout.flush()
time.sleep(0.5)
print('You do? Excellent.')
pipe_name=input('What is your brilliant pipeline name idea? ')
sys.stdout.flush()
time.sleep(0.5)
print('\n')
print('---------------------------------------------------------------------')
print('Thanks! Ok back to business. Before we start, I need some information.')
sys.stdout.flush()
time.sleep(0.5)
project_description = input('Please enter a SHORT description of this project (e.g., Minion 1D sequence to check sp ID of mystery shark fins): ')
datasetID = input('Enter dataset ID name (e.g., 20180206): ')

# kit details
flowcell = input('Enter the flowcell you used (e.g., FLO-MIN106): ')
kit = input('Enter the library kit ID you used (e.g., SQK-LSK109): ')

print('What filter parameter values would you like to use for minimum average base quality?')
min_filter_quality = input('Enter minimum avg read quality (e.g., 7): ')
barcode_kit = input('Enter barcode kit (e.g., PBC001): ')
my_qcat_minscore = input('Enter the minimum barcode alignment score for qcat (default: 58, e.g., 99): ')

print('We will filter read length by the gene length +/- a buffer length.')
print('For example, if your gene is 250 bp and you choose a buffer of 100bp,')
print('the reads will be filtered to be between 150 and 350bp.')
read_len_buffer = input('Enter buffer for read length filter (e.g., 100): ')

# set global paths
basecallout_path = toppath + '/1_Guppy_basecalled/' + datasetID + '_guppybasecallouts/'
NanoPlot_basecallout_path = toppath + '/1_Guppy_basecalled/' + datasetID + '_raw_filt_NanoPlots/'
demultiplexed_path = toppath+'/2b_Qcat_demultiplexed/'+datasetID+'_demultiplexouts/'
NanoPlot_demultiplexedout_path = toppath + '/2b_Qcat_demultiplexed/' + datasetID + '_demultiplexouts/' + datasetID + '_demultiplexed_NanoPlots/'

# define functions and call based on user input - e.g.
# do you want to run e.g., basecall()? y/n - if y, then basecall() if n, continue to next line
def setup(toppath):
    # create the directory structure
    print('Setting up output directories... ')

    commands = """
    echo 'Making directories'
    cd {0}
    if [ ! -d '{0}/0_MinKNOW_rawdata' ]; then mkdir {0}/0_MinKNOW_rawdata; fi
    if [ ! -d '{0}/1_Guppy_basecalled' ]; then mkdir {0}/1_Guppy_basecalled; fi
    if [ ! -d '{0}/2a_samp_lists' ]; then mkdir {0}/2a_samp_lists; fi
    if [ ! -d '{0}/2b_Qcat_demultiplexed' ]; then mkdir {0}/2b_Qcat_demultiplexed; fi
    if [ ! -d '{0}/3_isONclust_readclustering' ]; then mkdir {0}/3_isONclust_readclustering; fi
    if [ ! -d '{0}/4_spoamedaka_consensusblast' ]; then mkdir {0}/4_spoamedaka_consensusblast; fi
    if [ ! -d '{0}/Pipeline_logfiles' ]; then mkdir {0}/Pipeline_logfiles; fi
    """.format(toppath)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)

def basecall(scripthome, toppath, minknowdat, datasetID):
    print('######################################################################')
    print('Basecalling with Guppy.')
    print('Note: this step will take a REALLY long time to run')
    print('Advice: if your dataset is >400k, you may wish to split the data')
    print('to basecall in batches or basecall on a server.')
    print('(Processes ~100mil bases/hr)')
    print('ONT has improved basecalling speed with the recent fast basecall model.')
    print('Below are estimates given the model in v3.1.5:')
    print('For COI, fragment is ~790bp, this translates to ~180k reads/hr')
    print('For 16s, fragment is ~420bp, this translates to ~248k reads/hr')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    commands = """
    echo 'Running Guppy to call bases...'
    echo 'Running script: {0}/guppy_basecalling_wrapper.sh'
    echo 'For this dataset: {2}'
    echo 'File outputs will be labeled with: {3}'
    echo 'Output directory: {3}_guppybasecallouts'
    echo '-------------------------------------------------------------'
    bash {0}/guppy_basecalling_wrapper.sh {2} {3}_guppybasecallouts {1}
    """.format(scripthome, toppath, minknowdat, datasetID)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)
        pipe_log_file.write(cmd)
        pipe_log_file.write('\n')

    print('Done calling bases!')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

def raw_read_nanoplots(scripthome, basecallout_path, NanoPlot_basecallout_path, datasetID):
    print('######################################################################')
    print('Concatenate Guppy fastq files and check NanoPlots.')
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
        pipe_log_file.write(cmd)
        pipe_log_file.write('\n')

    print('Done plotting NanoPlots.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('Take a look at the read length and read quality distributions before continuing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

def demultiplexing(scripthome, toppath, datasetID, barcode_kit, my_qcat_minscore):
    print('######################################################################')
    print('Demultiplexing with Qcat.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    myfastqfile = datasetID + '.fastq'

    commands = """
    echo 'Running script: {0}/qcat_demultiplexing_wrapper.sh'
    echo 'Demultiplexing this file: {2}'
    echo 'Output directory: {1}_demultiplexouts'
    echo 'qcat min-score: {3}'
    echo 'qcat barcode kit: {4}'
    echo '-------------------------------------------------------------'
    bash {0}/qcat_demultiplexing_wrapper.sh {1} {2} {3} {4} {1}_demultiplexed_NanoPlots {5}
    echo '-------------------------------------------------------------'
    """.format(scripthome, datasetID, myfastqfile, my_qcat_minscore, barcode_kit, toppath)

    command_list = commands.split('\n')
    for cmd in command_list:
        os.system(cmd)
        pipe_log_file.write(cmd)
        pipe_log_file.write('\n')

    print('Done demultiplexing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

def filter_demultiplexed_reads(demultiplexed_path, datasetID, samp_list_df, min_filter_quality, read_len_buffer):
    print('######################################################################')
    print('Filter demultiplexed reads with NanoFilt.')
    print('This step is to remove low quality reads and any adapters and reads')
    print('that got trimmed too short after indexes/primers removed')
    print('and any chimeric reads that are too long')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_list_df.index:
        myfastqfile = demultiplexed_path + datasetID + samp_list_df.at[i,'sampleID'] + '.fastq'
        filteredfilename = demultiplexed_path + datasetID + samp_list_df.at[i,'sampleID'] + '_filtered.fastq'

        gene_length = samp_list_df.at[i, 'gene_len'].item() # the .item() is to make numpy int a native py int to match type() of read_len_buffer
        min_filter_len = gene_length - int(read_len_buffer)
        max_filter_len = gene_length + int(read_len_buffer)

        log_name = demultiplexed_path + datasetID + samp_list_df.at[i,'sampleID'] + '.log'

        rawfq = myfastqfile # going to write over this file, because don't want to save it. but store the # reads here
        rawfq_counter = 0
        for line in open(rawfq, 'r'):
            rawfq_counter += 1
        raw_reads = rawfq_counter/4

        # note: renaming unk.fastq file so it works with script for NanoPlot (need the '_' because used as a delimiter)
        commands = """
        echo 'For demultiplexed files in: {0}'
        echo 'Filtering: {1}'
        echo 'Quality score: {3}'
        echo 'Min length: {4}'
        echo 'Max length: {5}'
        echo 'Log file name: {6}'
        echo '-------------------------'
        cat {1} | NanoFilt -q {3} -l {4} --maxlength {5} --logfile {6} > {2}
        echo ' avg base quality filter done '
        echo 'deleting un-filtered file.'
        rm {1}

        mv {0}{7}unk.fastq {0}{7}unk_notfiltered.fastq
        """.format(demultiplexed_path, myfastqfile, filteredfilename, min_filter_quality, min_filter_len, max_filter_len, log_name, datasetID)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)
            pipe_log_file.write(cmd)
            pipe_log_file.write('\n')

        # count reads in raw vs. filtered
        # calculate reads retained vs. lost after filtering
        print('How many reads were lost after filtering?')
        filteredfq = filteredfilename
        filteredfq_counter = 0
        for line in open(filteredfq, 'r'):
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

def demultiplexed_nanoplots(demultiplexed_path):
    print('######################################################################')
    print('Create NanoPlots for all demultiplexed sample fastq files.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for thefastqs in os.listdir(toppath+'/2b_Qcat_demultiplexed/'+datasetID+'_demultiplexouts/'):
        if 'fastq' in thefastqs:
            mysampname = thefastqs.split('_')[0]

            commands = """
            echo 'For demultiplexed files in: {0}'
            echo 'Plotting NanoPlot for sample: {2}.fastq'
            echo 'NanoPlot outputs: {1}'
            echo 'NanoPlot outputs ID: {2}_dem'
            echo '-------------------------------------------------------------'
            mv {0}/{3} {0}/{2}.fastq
            NanoPlot --fastq {0}/{2}.fastq -o {1} -p {2}_dem --plots kde
            """.format(demultiplexed_path, NanoPlot_demultiplexedout_path, mysampname, thefastqs.rstrip())

            command_list = commands.split('\n')
            for cmd in command_list:
                os.system(cmd)
                pipe_log_file.write(cmd)
                pipe_log_file.write('\n')

    print('Done plotting NanoPlots.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('Take a look at the read length, read quality distributions, and number of reads per sample before continuing.')
    sys.stdout.flush()
    time.sleep(0.5)
    print('######################################################################')

# TODO -- EDITING FROM HERE IN PROGRESS
def read_clstr(samp_list_df, scripthome, toppath, datasetID):
    print('######################################################################')
    print('Read clustering with isONclust.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_list_df.index:

        mysamp = datasetID + samp_list_df.at[i, 'sampleID']
        fastqfile = './2b_Qcat_demultiplexed/'+datasetID+'_demultiplexouts/'+datasetID+samp_list_df.at[i, 'sampleID']+'.fastq'


        # TODO
        # have to test - might not need to write cluster parser now, have to check what the output of write_fastq is
        # BUT, if you want a parser, copy/edit the clstr_parser_isonclust.py script
        isONclust --fastq roedeer_filt_1K.fastq --ont --outfolder roedeer_filt_1K.isonclust

        isONclust write_fastq —clusters final_clusters.csv --fastq ../roedeer_filtered.fastq --outfolder fastqs --N 1



        commands = """
        if [ ! -d '{1}/3_isONclust_readclustering/{2}_readclstrs' ]; \
        then mkdir {1}/3_isONclust_readclustering/{2}_readclstrs; fi
        echo 'Running script: {0}/clstr_parser_isonclust.py'
        echo 'Input fastq: {4}'
        echo 'Output rep seq fasta: {5}'
        echo '-------------------------------------------------------------'

        python {0}/clstr_parser_isonclust.py --sampname {3} \
        --input_fastq {4} --output_fasta {5} \
        --out_dir {1}/3_isONclust_readclustering/{2}_readclstrs/
        """.format(scripthome, toppath, datasetID, mysamp, fastqfile, output_name)


# TODO
        # add in read cluster counter




        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)
            pipe_log_file.write(cmd)
            pipe_log_file.write('\n')

    print('Done with read clustering.')
    print('######################################################################')

def consensus_blast(samp_list_df, scripthome, toppath, datasetID, theblastdb, seq_div):
    print('######################################################################')
    print('Build consensus with minimap2 and Racon, then conduct Blast search.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    for i in samp_list_df.index:
        mysamp = samp_list_df.at[i, 'sampleID']
        refdb = './3_isONclust_readclustering/'+datasetID+'_readclstrs/'+datasetID+samp_list_df.at[i, 'sampleID']+'_out/'+datasetID + samp_list_df.at[i, 'sampleID'] + '_repseq.fasta'

        commands = """

#TODO - add these steps
        # DOWNLOAD SPOA
        # Consensus generation using spoa
        spoa 0.fastq > cluster0_spoa.fasta

        # ADD PATH FOR cd-hit-est
        # Check for reverse/complement
        cat cluster0_spoa.fasta cluster1_spoa.fasta > cluster_all.fasta
        cd-hit-est -i cluster_all.fasta -o cluster_roedeer.fasta

        # DOWNLOAD MEDAKA
        # Error correction using Medaka
        medaka_consensus -i snowcytb_2k.fastq -d snow_siocon_spoa.fasta -o snow_isocon_spoa_medaka.fasta


        echo '-------'
        echo 'Blast search of consensus sequence to blast database...'
        echo 'Running script: {0}/blast_local_wrapper.sh'
        echo 'Consensus sequence: {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}.racon2.fasta'
        echo 'Output file: {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}_raconblast'
        bash {0}/blast_local_wrapper.sh \
        {1}/Blast_resources/{5} \
        {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}.racon2.fasta \
        {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}_raconblast
        """.format(scripthome, toppath, datasetID, mysamp, refdb, theblastdb, seq_div)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)
            pipe_log_file.write(cmd)
            pipe_log_file.write('\n')

    print('Done with consensus building and blast search.')
    print('Go check your blast results!!')
    print('######################################################################')

def parse_blast(scripthome, toppath, datasetID, theblastdb, samp_list_df, min_filter_quality):
    print('######################################################################')
    print('Parsing blast output.')
    print('######################################################################')
    sys.stdout.flush()
    time.sleep(1.0)

    header_commands = """
    echo 'Make blast db header file if does not exist'
    if [ ! -d '{0}/Blast_resources/{1}HEADERS.txt' ]; then grep '>' {0}/Blast_resources/{1} | bash {2}/blast_header.sh > {0}/Blast_resources/{1}HEADERS.txt; fi
    """.format(toppath, theblastdb, scripthome)

    header_list = header_commands.split('\n')
    for cmd in header_list:
        os.system(cmd)

    for i in samp_list_df.index:
        mysamp = samp_list_df.at[i, 'sampleID']
        filteredfq = datasetID + '_minqscore' + min_filter_quality + '.fastq'

        commands = """
        echo '-------------------------------------------------------------'
        echo 'Running script: {0}/blast_parser_isONclust.py'
        echo 'Blast db file: {4}'
        echo '-------------------------------------------------------------'
        echo 'Parsing data...'
        python {0}/blast_parser_isONclust.py \
        --sampID {3} \
        --blastout {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}_raconblast.sorted \
        --blastdbheaders {1}/Blast_resources/{4}HEADERS.txt \
        --rawfq {1}/1_Guppy_basecalled/{2}_guppybasecallouts/{2}.fastq \
        --filteredfq {1}/1_Guppy_basecalled/{2}_guppybasecallouts/{5} \
        --minibar_fasta {1}/2b_MiniBar_demultiplexed/{2}_demultiplexouts/{2}{3}.fasta \
        --repseq {1}/3_isONclust_readclustering/{2}_readclstrs/{2}{3}_out/{2}{3}_repseq.fasta \
        --minimap_paf1 {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}.mapped1.paf \
        --racon1 {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}.racon1.fasta \
        --minimap_paf2 {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}.mapped2.paf \
        --racon2 {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/{3}.racon2.fasta \
        --output_dir {1}/4_isONClstrMinimapRacon_consensusblast/{2}_raconblastouts/
        """.format(scripthome, toppath, datasetID, mysamp, theblastdb, filteredfq)

        command_list = commands.split('\n')
        for cmd in command_list:
            os.system(cmd)
            pipe_log_file.write(cmd)
            pipe_log_file.write('\n')

    # create a concatenated file for all the final_parsed_output files
    # this will be the single input with read count info to R script for
    # making the sequence run summary report with markdown
    filelist = []
    for parsed_out in os.listdir(toppath+'/4_isONClstrMinimapRacon_consensusblast/'+datasetID+'_raconblastouts/'):
        if '_finalparsed_output.txt' in parsed_out:
            df = pd.read_csv(toppath+'/4_isONClstrMinimapRacon_consensusblast/'+datasetID+'_raconblastouts/'+parsed_out, header=0, sep='\t')
            filelist.append(df)
    frame = pd.concat(filelist, axis=0, ignore_index=True, sort=False)
    frame.to_csv(toppath+'/4_isONClstrMinimapRacon_consensusblast/'+datasetID+'_raconblastouts/'+datasetID+'_allsamps_parsedout.txt', sep='\t')

    print('Done with blast parsing.')
    print('######################################################################')

# Run functions based on flag y/n
# first step for pipeline is setup of directories and input data
while True:
    setup_flag = input('Are you running this pipeline for the first time? (y/n): ')
    if setup_flag == 'y':
        print('Time to set up the pipeline!')
        setup(toppath)
        break
    elif setup_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

ts = time.time() #prevents overwriting log files by giving specific date/time stamp
log_time = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

# Start writing pipeline log file
pipe_log_file = open(toppath+'/Pipeline_logfiles/'+datasetID+'_'+log_time+'_pipelinelog.txt','w')
pipe_log_file.write('Pipeline path: %s  Dataset ID: %s' % (toppath, datasetID))
pipe_log_file.write('\n')
pipe_log_file.write('Flowcell: %s   Kit: %s' % (flowcell, kit))
pipe_log_file.write('\n')
pipe_log_file.write('Project description: %s' % project_description)
pipe_log_file.write('\n')
pipe_log_file.write('Pipeline name idea: %s' % pipe_name)
pipe_log_file.write('\n')

# Parameter setting table
param_dict = {'SequenceRun': datasetID,
'MinAvgqScore':int(min_filter_quality),
'QcatMinScore':int(my_qcat_minscore),
'ReadLenBuffer':int(read_len_buffer)}

param_df=pd.DataFrame(param_dict, index=[0])
param_df.to_csv('./Pipeline_logfiles/'+datasetID+'_'+log_time+'_parameterlog.txt', sep='\t')

print('---------------------------------------------------------------------')
print('Before we get going, please do the following:')
print('1. Move your MinKNOW fast5 directory to the 0_MinKNOW_rawdata directory.')
minknowdat=input('Enter the path to your fast5 data (e.g., 20180206_1431_1DNB_FISHCOI_6Feb2018/fast5): ')
while True:
    if os.path.isdir(toppath+'/0_MinKNOW_rawdata/'+minknowdat) == True and minknowdat != '':
        step1=input('Ready to move on? (y/n): ')
        if step1 == 'y':
            print('Ok, moving on...')
            break
        elif step1 == 'n':
            print('Ok, I will wait...')
        else:
            print('What? Try again.')
    elif minknowdat == '':
        minknowdat=input('Try again. Enter the path to your fast5 data (e.g., 20180206_1431_1DNB_FISHCOI_6Feb2018/fast5): ')
    elif os.path.isdir(toppath+'/0_MinKNOW_rawdata/'+minknowdat) == False:
        minknowdat=input('Try again. Enter the path to your fast5 data (e.g., 20180206_1431_1DNB_FISHCOI_6Feb2018/fast5): ')
pipe_log_file.write('Raw data: %s' % minknowdat)
pipe_log_file.write('\n')
print('---------------------------------------------------------------------')
print('2. Create a text file with sample names and place in 2a_samp_lists.')
samp_list = input('Enter the name of your sample list file (e.g., 20180206_sample_list.txt): ')
while True:
    if os.path.isfile(toppath+'/2a_samp_lists/'+samp_list) == True:
        print('Formatting sample file ...')
        samp_list_df = pd.read_csv(toppath+'/2a_samp_lists/'+samp_list, sep='\t', header=None)
        samp_list_df.columns=['sampleID', 'gene', 'gene_len']
        print('Check that your sample file looks correct ...')
        print(samp_list_df.head(5))
        step3=input('Ready to move on? (y/n): ')
        if step3 == 'y':
            print('Ok, moving on...')
            break
        elif step3 == 'n':
            print('Ok, I will wait...')
        else:
            print('What? Try again.')
    elif os.path.isfile(toppath+'/2a_samp_lists/'+samp_list) == False:
        samp_list = input('Try again. Enter the name of your sample list file (e.g., 20180206_sample_list.txt): ')
pipe_log_file.write('Sample list file: %s' % samp_list)
pipe_log_file.write('\n')
print('---------------------------------------------------------------------')
print('After the consensus sequences are generated, I will perform a nucleotide Blast search.')
theblastdb = input('Enter the path to Blast database (e.g., NCBI_voucher_elasmobranchii_WCS_seqs.fasta): ')
while True:
    if os.path.isfile(toppath+'/Blast_resources/'+theblastdb) == True:
        print('Ok, moving on...')
        break
    elif os.path.isfile(toppath+'/Blast_resources/'+theblastdb) == False:
        theblastdb = input('The file you entered does not exist. Try again. Enter the path to Blast database (e.g., NCBI_voucher_elasmobranchii_WCS_seqs.fasta): ')
pipe_log_file.write('Blast database file: %s' % theblastdb)
pipe_log_file.write('\n')
print('---------------------------------------------------------------------')

while True:
    basecall_flag = input('Do you want to do basecalling? (y/n): ')
    if basecall_flag == 'y':
        print ('Ok, starting basecalling...')
        basecall(scripthome, toppath, minknowdat, datasetID)
        break
    elif basecall_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

while True:
    rawreads_flag = input('Do you want to run NanoPlot for raw data? (y/n): ')
    if rawreads_flag == 'y':
        print ('Ok, starting plotting...')
        raw_read_nanoplots(scripthome, basecallout_path, NanoPlot_basecallout_path, datasetID)
        break
    elif rawreads_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

while True:
    demultiplex_flag = input('Do you want to do demultiplexing? (y/n): ')
    if demultiplex_flag == 'y':
        print('Ok, starting demultiplexing...')
        demultiplexing(scripthome, toppath, datasetID, barcode_kit, my_qcat_minscore)
        break
    elif demultiplex_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

while True:
    filter_flag = input('Do you want to filter demultiplexed reads by quality & length? (y/n): ')
    if filter_flag == 'y':
        print('Ok, now removing poor quality reads and reads that are less than minimum & greater than maximum read length you chose (with NanoFilt)')
        filter_demultiplexed_reads(demultiplexed_path, datasetID, samp_list_df, min_filter_quality, read_len_buffer)
        break
    elif filter_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

while True:
    demultiplex_plot_flag = input('Do you want to run NanoPlot for demultiplexed samples? (y/n): ')
    if demultiplex_plot_flag == 'y':
        print('Ok, starting plotting...')
        demultiplexed_nanoplots(demultiplexed_path)
        break
    elif demultiplex_plot_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')


# TODO: edit from here

while True:
    read_clstr_flag = input('Do you want to do read clustering? (y/n): ')
    if read_clstr_flag == 'y':
        print('Ok, starting contig assembly...')
        read_clstr(samp_list_df, scripthome, toppath, datasetID)
        break
    elif read_clstr_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

while True:
    consensus_blast_flag = input('Do you want to do consensus building and blast search? (y/n): ')
    if consensus_blast_flag == 'y':
        print('Ok, starting consensus building...')
        consensus_blast(samp_list_df, scripthome, toppath, datasetID, theblastdb, seq_div)
        break
    elif consensus_blast_flag == 'n':
        print('Ok, moving to next step...')
        break
    else:
        print('What? Try again.')

while True:
    parse_blast_flag = input('Do you want parse the blast results? (y/n): ')
    if parse_blast_flag == 'y':
        print('Ok, starting parsing...')
        parse_blast(scripthome, toppath, datasetID, theblastdb, samp_list_df, min_filter_quality)
        print('Congratulations!!! You made it to the end of the line!')
        print('What species did you fish out of the sea?')
        break
    elif parse_blast_flag == 'n':
        print('Ok, we all done here then!')
        break
    else:
        print('What? Try again.')

pipelog_dict = {
'PipelinePath': toppath,
'DatasetID': datasetID,
'Flowcell': flowcell,
'Kit': kit,
'ProjectDescription': project_description,
'RawData': minknowdat,
'SampleFile': samp_list,
'BlastDBFile': theblastdb
}
pipe_df=pd.DataFrame(pipelog_dict, index=[0])
pipe_df.to_csv('./Pipeline_logfiles/'+datasetID+'_'+log_time+'_pipelineINFO.txt', sep='\t')

print('Generating summary report...')
pipelog = toppath+'/Pipeline_logfiles/' + datasetID + '_' + log_time + '_pipelineINFO.txt'
paramdat =  toppath+'/Pipeline_logfiles/' + datasetID + '_' + log_time + '_parameterlog.txt'

report_commands = """
echo 'Running script: {0}/summary_report_generator.Rmd'
echo 'Parameter file path: {3}'
echo 'Pipe log path: {4}'
Rscript -e "rmarkdown::render(input='{0}/summary_report_generator.Rmd', output_file='{0}/Pipeline_logfiles/{1}_{2}_report.html', params=list(run_name='{1}', param_dat='{3}', pipe_log='{4}'))"
""".format(toppath, datasetID, log_time, paramdat, pipelog)

report_command_list = report_commands.split('\n')
for cmd in report_command_list:
    os.system(cmd)
    pipe_log_file.write(cmd)
    pipe_log_file.write('\n')

pipe_log_file.close()
