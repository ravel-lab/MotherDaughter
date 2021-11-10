#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=16G -P jravel-lab -q all.q -N MMOTH_pre -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-3

source /usr/local/packages/usepackage/share/usepackage/use.bsh

use python-2.7
cd /local/groupshare/ravel/mfrance/MMOTH/02_preprocess/

infile=`sed -n "$SGE_TASK_ID p" MD_barcodes2.txt`

./preprocessV2.sh $infile
