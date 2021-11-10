#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=32G -P jravel-lab -q threaded.q -pe thread 4 -N dRep_MMOTH -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 2-47

source /usr/local/packages/usepackage/share/usepackage/use.bsh
use python-3.5

cd /local/scratch/mfrance/MMOTH/08_inStrain

infile=`sed -n -e "$SGE_TASK_ID p" MMOTH.lst`

source /home/mfrance/software/inStrain/.venv/bin/activate
source /home/mfrance/.bashrc

map_dir=/local/scratch/mfrance/MMOTH/07_mapping

inStrain profile --use_full_fasta_header -p 4 -s $map_dir/MMOTH_mags.txt -o ${infile} $map_dir/${infile}.bam $map_dir/genomeDB/MMOTH_derep_MAGs.fasta 
