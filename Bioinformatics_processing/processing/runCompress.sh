#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=4G -P jravel-lab -q all.q -N compress -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-47

cd /local/groupshare/ravel/mfrance/MMOTH/02_preprocess/1_fastq_pe/

infile=`sed -n -e "$SGE_TASK_ID p" MD_barcodes.txt`


gzip ${infile}.R1.fq
gzip ${infile}.R2.fq
gzip ${infile}.unpaired.fq
