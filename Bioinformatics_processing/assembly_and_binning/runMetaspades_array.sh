#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=128G -P jravel-lab -q threaded.q -N MD_metaspades -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-47

source /usr/local/packages/usepackage/share/usepackage/use.bsh

use python-2.7

infile=`sed -n "$SGE_TASK_ID p" MD_barcodes_all.txt`

cd /local/groupshare/ravel/mfrance/MMOTH/04_assembly/metaspades/

mkdir ${infile}

datadir=/local/groupshare/ravel/mfrance/MMOTH/02_preprocess/1_fastq_pe

pe1=$datadir/${infile}.R1.fq.gz
pe2=$datadir/${infile}.R2.fq.gz
se=$datadir/${infile}.unpaired.fq.gz

/usr/local/bin/metaspades.py -o ${infile} -k 21,33,55,77,99,101,127 -1 $pe1 -2 $pe2 -s $se -t 16 -m 128
