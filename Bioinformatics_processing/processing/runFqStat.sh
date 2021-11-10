#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=4G -P jravel-lab -q all.q -N MD_stat -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-44

source /usr/local/packages/usepackage/share/usepackage/use.bsh

use python-2.7
cd /local/groupshare/ravel/mfrance/MMOTH/02_preprocess/1_fastq_pe

infile=`sed -n "$SGE_TASK_ID p" MD_barcodes.txt`

./getFqStat.sh ${infile}.R1.fq
