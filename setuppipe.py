# create the directory structure

import os

toppath = os.getcwd() #this gets current working directory path

print('---------------------------------------------------')
print('Setting up output directories... ')

commands = """
echo 'Making directories'
cd {0}
if [ ! -d '{0}/0_MinKNOW_rawdata' ]; then mkdir {0}/0_MinKNOW_rawdata; fi
if [ ! -d '{0}/1_basecalled' ]; then mkdir {0}/1_basecalled; fi
if [ ! -d '{0}/2a_samp_lists' ]; then mkdir {0}/2a_samp_lists; fi
if [ ! -d '{0}/2b_demultiplexed' ]; then mkdir {0}/2b_demultiplexed; fi
if [ ! -d '{0}/3_readclustering' ]; then mkdir {0}/3_readclustering; fi
if [ ! -d '{0}/4_spID' ]; then mkdir {0}/4_spID; fi
if [ ! -d '{0}/Blast_resources' ]; then mkdir {0}/Blast_resources; fi
""".format(toppath)

command_list = commands.split('\n')
for cmd in command_list:
    os.system(cmd)

print('Move guppy basecalled files to 1_basecalled/')
print('Move sample input files to 2a_samp_lists/')
print('---------------------------------------------------')
